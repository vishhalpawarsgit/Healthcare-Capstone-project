
from io import BytesIO
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any

import re
import faiss
import numpy as np
from PIL import Image, UnidentifiedImageError
import pytesseract

from app.chunking.text_chunker import chunk_text
from app.embeddings.embedding_model import EmbeddingModel
from app.ingestion.document_loader import load_document

MAX_FILE_SIZE_BYTES = 50 * 1024 * 1024  # 50 MiB per file


class UploadedDocumentIndex:
    """In-memory semantic index for documents uploaded in the current session."""

    def __init__(self, embedding_model: EmbeddingModel | None = None):
        self.embedding_model = embedding_model or EmbeddingModel()
        self.index = faiss.IndexFlatIP(self.embedding_model.dimensions)
        self.records: list[dict[str, Any]] = []

    def add_uploaded_file(self, filename: str, content: bytes) -> int:
        if len(content) > MAX_FILE_SIZE_BYTES:
            raise ValueError(
                f"{filename} exceeds the 50 MiB file-size limit."
            )

        suffix = Path(filename).suffix.lower()

        if suffix not in {".pdf", ".docx", ".txt", ".jpg", ".jpeg", ".png"}:
            raise ValueError(
                "Supported formats: PDF, DOCX, TXT, JPG, JPEG, and PNG."
            )

        if not content:
            raise ValueError(f"{filename} is empty.")

        if suffix in {".jpg", ".jpeg", ".png"}:
            try:
                with Image.open(BytesIO(content)) as image:
                    image.load()

                    if image.format not in {"JPEG", "PNG"}:
                        raise ValueError(
                            "Image content must be a valid JPEG or PNG file."
                        )

                    text = pytesseract.image_to_string(image).strip()

            except (UnidentifiedImageError, OSError) as exc:
                raise ValueError(
                    f"Could not read image {filename}. "
                    "Please upload a valid JPG, JPEG, or PNG image."
                ) from exc

            if not text:
                raise ValueError(
                    f"No text could be extracted from {filename}. "
                    "Try an image with clearer, readable text."
                )

            document = {
                "text": text,
                "file_type": suffix.lstrip("."),
            }

        else:
            with TemporaryDirectory() as temp_dir:
                temp_path = Path(temp_dir) / Path(filename).name
                temp_path.write_bytes(content)
                document = load_document(temp_path)

        chunks = chunk_text(document["text"])

        if not chunks:
            raise ValueError(
                f"No extractable text found in {filename}. "
                "Scanned PDFs may require OCR."
            )

        texts = [chunk["text"] for chunk in chunks]
        embeddings = np.asarray(
            self.embedding_model.encode_texts(texts),
            dtype=np.float32,
        )

        if embeddings.shape != (
            len(texts),
            self.embedding_model.dimensions,
        ):
            raise ValueError("Unexpected embedding dimensions.")

        metadata = [
            {
                "source": filename,
                "chunk_index": chunk["chunk_index"],
                "file_type": document["file_type"],
            }
            for chunk in chunks
        ]

        self.index.add(embeddings)
        self.records.extend(
            {"text": text, "metadata": meta}
            for text, meta in zip(texts, metadata)
        )

        return len(chunks)

    def search(self, question: str, top_k: int = 3) -> list[dict[str, Any]]:
        if not question or not question.strip():
            raise ValueError("Question cannot be empty.")

        if top_k <= 0:
            raise ValueError("top_k must be greater than zero.")

        if self.index.ntotal == 0:
            return []

        query = question.strip()
        query_embedding = np.asarray(
            self.embedding_model.encode_texts([query]),
            dtype=np.float32,
        )

        # Retrieve more candidates, then rerank them.
        candidate_k = min(max(top_k * 3, 10), self.index.ntotal)
        scores, indices = self.index.search(query_embedding, candidate_k)

        stop_words = {
            "what", "are", "the", "is", "a", "an", "of", "for",
            "to", "in", "on", "and", "or", "does", "do", "how",
            "where", "when", "why", "who", "which", "according",
            "must", "can", "could", "would", "should", "please",
            "hospital", "patient", "patients", "image", "document",
            "policy",
        }

        query_terms = {
            term.lower()
            for term in re.findall(r"\b[a-zA-Z]{3,}\b", query)
            if term.lower() not in stop_words
        }

        candidates = []

        for score, index_id in zip(scores[0], indices[0]):
            if index_id < 0:
                continue

            record = self.records[int(index_id)]
            text = record["text"]
            text_terms = {
                term.lower()
                for term in re.findall(r"\b[a-zA-Z]{3,}\b", text)
            }

            overlap = (
                len(query_terms & text_terms) / len(query_terms)
                if query_terms
                else 0.0
            )
            # Blend semantic similarity and keyword overlap.
            combined_score = 0.75 * float(score) + 0.25 * overlap

            candidates.append(
                {
                    "text": text,
                    "score": float(score),
                    "rerank_score": combined_score,
                    "keyword_overlap": overlap,
                    "citation": record["metadata"],
                }
            )

        candidates.sort(
            key=lambda result: result["rerank_score"],
            reverse=True,
        )

        # Require stronger semantic similarity and keyword overlap.
        MIN_SIMILARITY_SCORE = 0.40
        MIN_KEYWORD_OVERLAP = 0.50

        relevant_candidates = [
            result
            for result in candidates
            if (
                result["score"] >= MIN_SIMILARITY_SCORE
                and result["keyword_overlap"] >= MIN_KEYWORD_OVERLAP
            )
        ]

        return relevant_candidates[:top_k]

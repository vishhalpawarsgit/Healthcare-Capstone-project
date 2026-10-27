
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any

import re
import faiss
import numpy as np

from app.chunking.text_chunker import chunk_text
from app.embeddings.embedding_model import EmbeddingModel
from app.ingestion.document_loader import load_document


class UploadedDocumentIndex:
    """In-memory semantic index for documents uploaded in the current session."""

    def __init__(self, embedding_model: EmbeddingModel | None = None):
        self.embedding_model = embedding_model or EmbeddingModel()
        self.index = faiss.IndexFlatIP(self.embedding_model.dimensions)
        self.records: list[dict[str, Any]] = []

    def add_uploaded_file(self, filename: str, content: bytes) -> int:
        suffix = Path(filename).suffix.lower()

        if suffix not in {".pdf", ".docx", ".txt"}:
            raise ValueError("Only PDF, DOCX, and TXT files are supported.")

        if not content:
            raise ValueError(f"{filename} is empty.")

        # Use a temporary file because the existing loader accepts a file path.
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
            "patient", "patients",
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
                    "citation": record["metadata"],
                }
            )

        candidates.sort(
            key=lambda result: result["rerank_score"],
            reverse=True,
        )

        return candidates[:top_k]


from pathlib import Path
import json

import faiss
import numpy as np


class FAISSVectorStore:
    """FAISS vector store with text and source metadata."""

    def __init__(self, dimensions: int = 384):
        if dimensions <= 0:
            raise ValueError("Dimensions must be greater than zero.")

        self.dimensions = dimensions
        self.index = faiss.IndexFlatIP(dimensions)
        self.texts: list[str] = []
        self.metadata: list[dict] = []

    def add(
        self,
        embeddings: np.ndarray,
        texts: list[str],
        metadata: list[dict] | None = None,
    ) -> None:
        """Add embeddings, text chunks, and optional source metadata."""
        embeddings = np.asarray(embeddings, dtype=np.float32)

        if embeddings.ndim != 2 or embeddings.shape[1] != self.dimensions:
            raise ValueError(
                f"Expected embeddings with shape (n, {self.dimensions})."
            )

        if len(embeddings) != len(texts):
            raise ValueError("Each embedding must have one text chunk.")

        if metadata is None:
            metadata = [{} for _ in texts]

        if len(metadata) != len(texts):
            raise ValueError("Each text chunk must have one metadata record.")

        if not all(isinstance(item, dict) for item in metadata):
            raise ValueError("Each metadata record must be a dictionary.")

        if len(texts) == 0:
            return

        if not np.isfinite(embeddings).all():
            raise ValueError("Embeddings must contain only finite values.")

        self.index.add(embeddings)
        self.texts.extend(texts)
        self.metadata.extend(metadata)

    def search(
        self,
        query_embedding: np.ndarray,
        top_k: int = 3,
    ) -> list[dict]:
        """Return the most similar chunks with their source metadata."""
        if top_k <= 0:
            raise ValueError("top_k must be greater than zero.")

        query = np.asarray(query_embedding, dtype=np.float32)

        if query.ndim == 1:
            query = query.reshape(1, -1)

        if query.ndim != 2 or query.shape[1] != self.dimensions:
            raise ValueError(
                f"Expected query embeddings with {self.dimensions} dimensions."
            )

        if not np.isfinite(query).all():
            raise ValueError("Query embedding must contain only finite values.")

        if self.index.ntotal == 0:
            return []

        scores, ids = self.index.search(
            query, min(top_k, self.index.ntotal)
        )

        results = []

        for score, idx in zip(scores[0], ids[0]):
            if idx >= 0:
                position = int(idx)
                results.append(
                    {
                        "text": self.texts[position],
                        "score": float(score),
                        "id": position,
                        "metadata": self.metadata[position],
                    }
                )

        return results

    def save(self, directory: str | Path) -> None:
        """Save the FAISS index, text chunks, and metadata."""
        directory = Path(directory)
        directory.mkdir(parents=True, exist_ok=True)

        if not (
            self.index.ntotal == len(self.texts) == len(self.metadata)
        ):
            raise ValueError("Index, text, and metadata counts do not match.")

        faiss.write_index(self.index, str(directory / "faiss.index"))

        with (directory / "faiss_texts.json").open(
            "w", encoding="utf-8"
        ) as file:
            json.dump(self.texts, file, ensure_ascii=False, indent=2)

        with (directory / "faiss_metadata.json").open(
            "w", encoding="utf-8"
        ) as file:
            json.dump(self.metadata, file, ensure_ascii=False, indent=2)

    @classmethod
    def load(cls, directory: str | Path) -> "FAISSVectorStore":
        """Load a saved FAISS index, text chunks, and metadata."""
        directory = Path(directory)
        index_path = directory / "faiss.index"
        texts_path = directory / "faiss_texts.json"
        metadata_path = directory / "faiss_metadata.json"

        if not index_path.is_file() or not texts_path.is_file():
            raise FileNotFoundError(
                f"Expected faiss.index and faiss_texts.json in {directory}"
            )

        index = faiss.read_index(str(index_path))

        with texts_path.open("r", encoding="utf-8") as file:
            texts = json.load(file)

        if not isinstance(texts, list) or not all(
            isinstance(text, str) for text in texts
        ):
            raise ValueError("Saved text chunks must be a list of strings.")

        # Support older indexes that do not yet have metadata.
        if metadata_path.is_file():
            with metadata_path.open("r", encoding="utf-8") as file:
                metadata = json.load(file)
        else:
            metadata = [{} for _ in texts]

        if not isinstance(metadata, list) or not all(
            isinstance(item, dict) for item in metadata
        ):
            raise ValueError("Saved metadata must be a list of dictionaries.")

        if index.d <= 0:
            raise ValueError("Saved index dimensions must be positive.")

        if not (index.ntotal == len(texts) == len(metadata)):
            raise ValueError("Saved index, text, and metadata counts do not match.")

        store = cls(dimensions=index.d)
        store.index = index
        store.texts = texts
        store.metadata = metadata
        return store

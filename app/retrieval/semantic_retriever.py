
from pathlib import Path
from typing import Any

from app.embeddings.embedding_model import EmbeddingModel
from app.vector_store.faiss_store import FAISSVectorStore


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_INDEX_DIRECTORY = PROJECT_ROOT / "data" / "vector_store" / "faiss"


class SemanticRetriever:
    """Retrieve semantically relevant chunks with source citations."""

    def __init__(
        self,
        index_directory: str | Path = DEFAULT_INDEX_DIRECTORY,
        top_k: int = 3,
        embedding_model: EmbeddingModel | None = None,
    ):
        if top_k <= 0:
            raise ValueError("top_k must be greater than zero.")

        self.top_k = top_k
        self.embedding_model = embedding_model or EmbeddingModel()
        self.store = FAISSVectorStore.load(index_directory)

        if self.store.dimensions != self.embedding_model.dimensions:
            raise ValueError(
                "Index dimensions do not match the embedding model."
            )

    def retrieve(self, query: str) -> list[dict[str, Any]]:
        """Return ranked chunks and their source citation metadata."""
        if not query or not query.strip():
            raise ValueError("Query cannot be empty.")

        query_embedding = self.embedding_model.encode_texts(
            [query.strip()]
        )[0]

        results = self.store.search(
            query_embedding,
            top_k=self.top_k,
        )

        retrieved = []

        for rank, result in enumerate(results, start=1):
            metadata = result.get("metadata", {})

            retrieved.append(
                {
                    "rank": rank,
                    "text": result["text"],
                    "score": result["score"],
                    "citation": {
                        "source": metadata.get("source", "Unknown source"),
                        "chunk_index": metadata.get("chunk_index"),
                        "file_type": metadata.get("file_type"),
                    },
                }
            )

        return retrieved

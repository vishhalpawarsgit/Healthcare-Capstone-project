
from sentence_transformers import SentenceTransformer

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


class EmbeddingModel:
    """Generate text embeddings for the MediAssist AI RAG pipeline."""

    def __init__(self, model_name: str = MODEL_NAME):
        self.model = SentenceTransformer(model_name)

    def encode_texts(self, texts: list[str]):
        """Convert a list of text strings into numerical vectors."""
        if not texts:
            return self.model.encode([])

        return self.model.encode(
            texts,
            convert_to_numpy=True,
            normalize_embeddings=True,
        )

    @property
    def dimensions(self) -> int:
        return self.model.get_sentence_embedding_dimension()

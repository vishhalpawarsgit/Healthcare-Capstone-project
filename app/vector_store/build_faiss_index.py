
from pathlib import Path

from app.chunking.text_chunker import chunk_text
from app.embeddings.embedding_model import EmbeddingModel
from app.ingestion.document_loader import load_document
from app.vector_store.faiss_store import FAISSVectorStore


PROJECT_ROOT = Path(__file__).resolve().parents[2]
TEST_DOCUMENT = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "ingestion_tests"
    / "sample_hospital_sop.txt"
)
INDEX_DIRECTORY = PROJECT_ROOT / "data" / "vector_store" / "faiss"


def main() -> None:
    if not TEST_DOCUMENT.is_file():
        raise FileNotFoundError(
            f"Test document not found: {TEST_DOCUMENT}"
        )

    # 1. Load the source document.
    document = load_document(TEST_DOCUMENT)
    text = document["text"]

    if not text:
        raise ValueError("The test document contains no extractable text.")

    print("Document loaded:", document["source"])

    # 2. Create overlapping text chunks.
    chunks = chunk_text(text)

    if not chunks:
        raise ValueError("No text chunks were generated.")

    texts = [chunk["text"] for chunk in chunks]

    # 3. Attach citation metadata to every chunk.
    metadata = [
        {
            "source": document["source"],
            "chunk_index": chunk["chunk_index"],
            "file_type": document["file_type"],
        }
        for chunk in chunks
    ]

    print("Chunks created:", len(texts))

    # 4. Generate embeddings.
    embedding_model = EmbeddingModel()
    embeddings = embedding_model.encode_texts(texts)

    print("Embedding shape:", embeddings.shape)

    # 5. Build the vector store with citation metadata.
    store = FAISSVectorStore(
        dimensions=embedding_model.dimensions
    )
    store.add(embeddings, texts, metadata=metadata)

    # 6. Save vectors, text chunks, and metadata.
    store.save(INDEX_DIRECTORY)

    print("Vectors stored:", store.index.ntotal)
    print("Index saved to:", INDEX_DIRECTORY)

    # 7. Search using a sample query.
    query_embedding = embedding_model.encode_texts(
        ["How does the hospital admit a patient?"]
    )[0]

    results = store.search(query_embedding, top_k=3)

    print("\nSample search results:")
    for result in results:
        citation = result["metadata"]
        print(
            f"- Score: {result['score']:.4f} | "
            f"Source: {citation.get('source', 'Unknown')} | "
            f"Chunk: {citation.get('chunk_index', 'Unknown')}"
        )
        print(f"  Text: {result['text'][:150]}")

    print("\nFAISS indexing with citation metadata passed!")


if __name__ == "__main__":
    main()

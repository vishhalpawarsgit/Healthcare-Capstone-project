
from app.retrieval.semantic_retriever import SemanticRetriever


def test_semantic_retrieval():
    retriever = SemanticRetriever(top_k=3)

    query = "How does the hospital admit a patient?"
    results = retriever.retrieve(query)

    print("Query:", query)
    print("Results returned:", len(results))

    for result in results:
        citation = result["citation"]

        print(f"\nRank: {result['rank']}")
        print(f"Similarity score: {result['score']:.4f}")
        print(f"Source: {citation['source']}")
        print(f"Chunk index: {citation['chunk_index']}")
        print(f"Text: {result['text'][:150]}")

    assert len(results) <= 3

    if results:
        assert results[0]["rank"] == 1
        assert results[0]["citation"]["source"] != "Unknown source"
        assert results[0]["citation"]["chunk_index"] is not None

    print("\nSemantic retrieval test passed!")


if __name__ == "__main__":
    test_semantic_retrieval()


from app.retrieval.rag_engine import RAGEngine


def test_rag_engine():
    engine = RAGEngine(top_k=3)

    response = engine.answer(
        "How does the hospital admit a patient?"
    )

    print("Question:", response["question"])
    print("Answer:", response["answer"])
    print("Retrieved count:", response["retrieved_count"])
    print("Generation method:", response["generation_method"])
    print("Citations:", response["citations"])

    assert response["question"]
    assert response["retrieved_count"] > 0
    assert response["citations"]
    assert response["generation_method"] == "extractive"

    print("\nRAG engine test passed!")


if __name__ == "__main__":
    test_rag_engine()

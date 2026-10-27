
from app.retrieval.rag_context import format_rag_context


def test_rag_context_formatting():
    results = [
        {
            "rank": 1,
            "score": 0.5008,
            "text": (
                "Nursing staff should verify the assigned bed "
                "before a fictional patient admission."
            ),
            "citation": {
                "source": "sample_hospital_sop.txt",
                "chunk_index": 0,
                "file_type": "txt",
            },
        }
    ]

    context = format_rag_context(results)

    assert "sample_hospital_sop.txt" in context
    assert "Chunk: 0" in context
    assert "verify the assigned bed" in context

    print(context)
    print("\nRAG context formatting test passed!")


def test_empty_results():
    context = format_rag_context([])

    assert context == "No relevant source passages were retrieved."

    print("Empty retrieval handled correctly!")


if __name__ == "__main__":
    test_rag_context_formatting()
    test_empty_results()


from app.retrieval.rag_context import format_rag_context
from app.retrieval.semantic_retriever import SemanticRetriever


def test_rag_retrieval_pipeline():
    query = "How does the hospital admit a patient?"

    # 1. Retrieve relevant chunks from FAISS.
    retriever = SemanticRetriever(top_k=3)
    results = retriever.retrieve(query)

    # 2. Format retrieved chunks and citations as RAG context.
    context = format_rag_context(results)

    print("Query:", query)
    print("\nRetrieved chunks:", len(results))
    print("\nRAG context:")
    print(context)

    # 3. Verify the retrieval-to-context flow.
    if results:
        assert context != "No relevant source passages were retrieved."
        assert results[0]["citation"]["source"] != "Unknown source"
        assert results[0]["citation"]["chunk_index"] is not None

        for result in results:
            assert result["text"] in context

        print("\nRAG retrieval pipeline test passed!")
    else:
        assert context == "No relevant source passages were retrieved."
        print("\nRAG pipeline handled empty retrieval correctly!")


if __name__ == "__main__":
    test_rag_retrieval_pipeline()

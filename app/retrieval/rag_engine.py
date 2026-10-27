
from typing import Any

from app.retrieval.rag_context import format_rag_context
from app.retrieval.semantic_retriever import SemanticRetriever


class RAGEngine:
    """Coordinate retrieval, context preparation, and grounded responses."""

    def __init__(
        self,
        retriever: SemanticRetriever | None = None,
        top_k: int = 3,
    ):
        self.retriever = retriever or SemanticRetriever(top_k=top_k)

    def answer(self, question: str) -> dict[str, Any]:
        """
        Retrieve relevant passages and return a grounded response.

        This initial version is extractive; it does not call an LLM.
        """
        if not question or not question.strip():
            raise ValueError("Question cannot be empty.")

        results = self.retriever.retrieve(question.strip())
        context = format_rag_context(results)

        if not results:
            return {
                "question": question,
                "answer": (
                    "I could not find supporting information in the "
                    "available documents. Please consult an authorized "
                    "source or qualified professional."
                ),
                "citations": [],
                "context": context,
                "retrieved_count": 0,
                "generation_method": "no_supporting_context",
            }

        # Safe extractive baseline: use retrieved source text as the response.
        answer_parts = []
        citations = []

        for result in results:
            text = result["text"].strip()
            if text and text not in answer_parts:
                answer_parts.append(text)

            citation = result["citation"]
            citations.append(
                {
                    "source": citation["source"],
                    "chunk_index": citation["chunk_index"],
                    "rank": result["rank"],
                    "score": result["score"],
                }
            )

        return {
            "question": question,
            "answer": "\n\n".join(answer_parts),
            "citations": citations,
            "context": context,
            "retrieved_count": len(results),
            "generation_method": "extractive",
        }

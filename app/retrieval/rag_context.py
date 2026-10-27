
from typing import Any


def format_rag_context(results: list[dict[str, Any]]) -> str:
    """Format retrieved chunks with source citations for RAG."""

    if not results:
        return "No relevant source passages were retrieved."

    sections = []

    for result in results:
        citation = result.get("citation", {})
        source = citation.get("source", "Unknown source")
        chunk_index = citation.get("chunk_index", "Unknown")

        sections.append(
            f"[Source: {source} | Chunk: {chunk_index}]\n"
            f"{result['text']}"
        )

    return "\n\n".join(sections)

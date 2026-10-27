
from typing import Any


def chunk_text(
    text: str,
    chunk_size: int = 1000,
    chunk_overlap: int = 150,
) -> list[dict[str, Any]]:
    """
    Split text into overlapping character-based chunks.

    Args:
        text: Extracted source text.
        chunk_size: Maximum number of characters per chunk.
        chunk_overlap: Number of characters shared between chunks.

    Returns:
        A list of chunks with their index and text.
    """
    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than zero")

    if chunk_overlap < 0:
        raise ValueError("chunk_overlap cannot be negative")

    if chunk_overlap >= chunk_size:
        raise ValueError("chunk_overlap must be smaller than chunk_size")

    text = text.strip()

    if not text:
        return []

    chunks = []
    start = 0

    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunk = text[start:end].strip()

        if chunk:
            chunks.append({
                "chunk_index": len(chunks),
                "text": chunk,
            })

        if end == len(text):
            break

        start = end - chunk_overlap

    return chunks


from text_chunker import chunk_text


def test_basic_chunking():
    text = "ABCDEFGHIJKLMNOPQRSTUVWXYZ" * 10

    chunks = chunk_text(
        text,
        chunk_size=100,
        chunk_overlap=20,
    )

    assert len(chunks) > 1
    assert chunks[0]["chunk_index"] == 0
    assert chunks[1]["chunk_index"] == 1
    assert len(chunks[0]["text"]) <= 100

    # Confirm the overlap is preserved between adjacent chunks.
    assert chunks[0]["text"][-20:] == chunks[1]["text"][:20]

    # Confirm the chunks reconstruct the original text when
    # overlap is removed from each subsequent chunk.
    reconstructed = chunks[0]["text"] + "".join(
        chunk["text"][20:] for chunk in chunks[1:]
    )
    assert reconstructed == text

    print("✅ Basic chunking and overlap test passed!")


def test_empty_text():
    assert chunk_text("   ") == []
    print("✅ Empty text test passed!")


def test_invalid_settings():
    invalid_settings = [
        (0, 0),
        (100, -1),
        (100, 100),
    ]

    for size, overlap in invalid_settings:
        try:
            chunk_text("Some test text", size, overlap)
        except ValueError:
            continue
        raise AssertionError(
            f"Expected ValueError for size={size}, overlap={overlap}"
        )

    print("✅ Invalid settings tests passed!")


if __name__ == "__main__":
    test_basic_chunking()
    test_empty_text()
    test_invalid_settings()
    print("\n🎉 All chunking tests passed!")

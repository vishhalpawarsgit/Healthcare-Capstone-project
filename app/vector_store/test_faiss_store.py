
import tempfile

import numpy as np

from app.vector_store.faiss_store import FAISSVectorStore


def test_save_and_load():
    store = FAISSVectorStore(dimensions=3)

    embeddings = np.array(
        [
            [1.0, 0.0, 0.0],
            [0.0, 1.0, 0.0],
            [0.9, 0.1, 0.0],
        ],
        dtype=np.float32,
    )

    texts = [
        "Hospital admission procedure",
        "Patient discharge instructions",
        "Admission documentation process",
    ]

    store.add(embeddings, texts)

    with tempfile.TemporaryDirectory() as temp_dir:
        store.save(temp_dir)
        loaded_store = FAISSVectorStore.load(temp_dir)

        assert loaded_store.index.ntotal == 3
        assert loaded_store.texts == texts
        assert loaded_store.dimensions == 3

        results = loaded_store.search(embeddings[0], top_k=2)

        assert results[0]["text"] == "Hospital admission procedure"
        assert results[0]["id"] == 0

        print("Vectors restored:", loaded_store.index.ntotal)
        print("Top result after reload:", results[0]["text"])
        print("FAISS persistence test passed!")


if __name__ == "__main__":
    test_save_and_load()

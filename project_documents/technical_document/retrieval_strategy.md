# Retrieval Strategy for RAG

## 1. Purpose

This document describes the retrieval strategy for the MediAssist AI RAG (Retrieval-Augmented Generation) pipeline. The retrieval component searches the FAISS vector index for text chunks that are semantically similar to a user's query and returns them as context for downstream answer generation.

## 2. Retrieval Mechanism

The current prototype uses FAISS with an `IndexFlatIP` index.

The retrieval process is:

1. Receive a user query.
2. Convert the query into an embedding using the same `sentence-transformers/all-MiniLM-L6-v2` model used for document chunks.
3. Normalize the query embedding, as performed by the existing embedding model.
4. Search the FAISS index using inner-product similarity.
5. Retrieve the highest-scoring matching chunks.
6. Return the chunk text, similarity score, and index ID to the caller.

The document chunks and their embeddings must use the same embedding model and dimensionality.

## 3. Top-K Retrieval

The current `FAISSVectorStore.search()` method uses `top_k=3` by default.

- Default retrieval count: 3 results.
- Configurable: The caller can request a different positive value for `top_k`.
- Result limit: The number of returned results cannot exceed the number of vectors stored in the index.
- Empty index: An empty index returns an empty result list.

The default value of three is an initial prototype setting. It has not yet been established as the optimal value for hospital-document retrieval.

## 4. Ranking Mechanism

The index uses `faiss.IndexFlatIP`, which performs exact inner-product search.

Because the current embedding model returns normalized embeddings, the inner product between a query embedding and a document embedding corresponds to cosine similarity.

Results are ordered by decreasing similarity score:

- Higher score: Greater vector similarity to the query.
- Lower score: Lower vector similarity to the query.

The score measures embedding similarity; it does not guarantee factual correctness, clinical relevance, or completeness.

## 5. Returned Result Structure

Each search result contains:

- `text`: Retrieved text chunk.
- `score`: Similarity score returned by FAISS.
- `id`: Position of the vector in the FAISS index and its associated text list.

The current implementation uses the index position to associate each vector with its text chunk.

## 6. Current Limitations

The current prototype implements dense vector similarity search. It does not yet implement keyword search, hybrid retrieval, metadata filtering, reranking with a separate model, or diversity-based retrieval.

The current indexing and retrieval tests use fictional sample content. Retrieval quality has not yet been benchmarked on a representative document collection.

## 7. Future Evaluation

The retrieval strategy should be evaluated using representative, authorized, de-identified test documents and realistic queries.

Potential evaluation measures include:

- Whether relevant chunks appear in the top-K results.
- Whether the returned context supports the expected answer.
- Whether results contain redundant or irrelevant chunks.
- Retrieval latency as the indexed document collection grows.

The top-K value and retrieval method should be adjusted based on measured results rather than assumptions.

## 8. Summary

The current MediAssist AI prototype uses FAISS exact inner-product search with normalized 384-dimensional embeddings. It retrieves up to three results by default and ranks them by decreasing similarity score. This is the initial retrieval strategy and requires further evaluation before being considered suitable for clinical use.
# Phase 10 — Enterprise RAG Pipeline

## 1. Objective

Implement a Retrieval-Augmented Generation (RAG) pipeline that retrieves relevant document passages through semantic similarity search and preserves source citations.

## 2. Architecture

1. Receive a user's question.
2. Convert the question into an embedding using `sentence-transformers/all-MiniLM-L6-v2`.
3. Search the FAISS vector index using inner-product similarity.
4. Rank results by similarity score and return the configured top-K passages.
5. Preserve source filename, chunk index, and file type as citation metadata.
6. Format retrieved passages into a context string.
7. Return an extractive response with citation details.

## 3. Implementation

- **Vector store:** FAISS using `IndexFlatIP`.
- **Embedding model:** `sentence-transformers/all-MiniLM-L6-v2`.
- **Default top-K:** 3, limited by the number of indexed vectors.
- **Retrieval:** Semantic similarity search with normalized embeddings.
- **Citation fields:** Source, chunk index, rank, and similarity score.
- **RAG Engine:** `app/retrieval/rag_engine.py`.
- **Context formatter:** `app/retrieval/rag_context.py`.
- **Semantic retriever:** `app/retrieval/semantic_retriever.py`.

## 4. Validation

The following tests passed:

- `app.vector_store.test_faiss_store`
- `app.retrieval.test_semantic_retriever`
- `app.retrieval.test_rag_context`
- `app.retrieval.test_rag_pipeline`
- `app.retrieval.test_rag_engine`

The test index returned a relevant fictional SOP passage with its source filename and chunk index. Vector-store persistence and citation metadata restoration were also verified.

## 5. Current Limitations

- Validation uses a fictional test document, not the complete hospital document collection.
- The current answer method is extractive; it does not use an LLM to synthesize a new answer.
- Keyword search, hybrid retrieval, metadata filtering, reranking, and retrieval-quality benchmarking have not been implemented.
- A similarity score alone does not establish that a passage is authoritative or sufficient to answer a healthcare question.
- Production use requires appropriate access controls, data protection, and validation against authorized documents.

## 6. Phase 10 Outcome

The semantic retrieval and extractive RAG pipeline is implemented and passes the listed tests. LLM-backed answer generation and broader retrieval evaluation remain future enhancements.

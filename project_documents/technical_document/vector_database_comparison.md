# MediAssist AI — Vector Database Comparison

## 1. Objective

Compare ChromaDB, Pinecone, Weaviate, and FAISS for the MediAssist AI retrieval-augmented generation (RAG) pipeline.

The comparison evaluates indexing algorithms, keyword search, vector search, hybrid search, metadata filtering, operational complexity, and suitability for a dataset containing fewer than one million vectors.

## 2. Project Requirements

- Initial target: fewer than 1,000,000 vectors.
- Embedding model: `sentence-transformers/all-MiniLM-L6-v2`.
- Embedding dimensions: 384.
- Required retrieval: semantic vector search.
- Desired retrieval: keyword search, hybrid search, and metadata filtering.
- Development environment: local macOS development.
- Planned deployment: Azure Container Apps.
- Privacy: hospital documents must be handled according to project security requirements.
- The vector store must retain source identifiers and metadata for retrieved chunks.

## 3. Indexing Algorithms

### FAISS
FAISS is a vector similarity-search library rather than a complete document database.

Relevant index options include:
- `IndexFlatIP`: exhaustive inner-product search.
- `IndexFlatL2`: exhaustive squared-L2 search.
- `IndexHNSWFlat`: graph-based approximate nearest-neighbor search.
- IVF indexes: partition vectors into clusters to reduce the search space.

Flat indexes are straightforward for smaller datasets. HNSW and IVF are alternatives when search latency or resource usage becomes important.

FAISS does not independently provide a complete keyword-search engine or document-management workflow. The application must manage text, metadata, persistence, and any hybrid-ranking logic.

Official documentation: https://faiss.ai/

### ChromaDB
ChromaDB provides document, embedding, and metadata storage alongside retrieval functionality.

Its local indexing implementation uses HNSW for vector similarity search. Chroma also supports full-text search, metadata filtering, dense and sparse retrieval, and hybrid-search capabilities.

Chroma is suitable for a local RAG prototype because it reduces the amount of custom storage and retrieval code required.

Official documentation: https://docs.trychroma.com/

### Pinecone
Pinecone is a managed vector database with dense, sparse, and hybrid retrieval capabilities.

Its indexes are configured for supported vector types and similarity metrics. Sparse vectors can support lexical retrieval, while dense vectors support semantic retrieval. Hybrid search combines lexical and semantic signals.

Pinecone reduces the need to operate vector-storage infrastructure but introduces hosted-service configuration, cost, network, and data-governance considerations.

Official documentation: https://docs.pinecone.io/

### Weaviate
Weaviate provides vector storage, metadata filtering, and keyword retrieval.

Supported vector-index types include:
- HNSW: approximate nearest-neighbor graph search.
- Flat: exhaustive search for smaller collections.
- Dynamic: can transition from flat to HNSW as the collection grows.
- HFresh: a cluster-based index designed to improve memory efficiency.

Weaviate also supports inverted indexes for keyword search and filtering, plus hybrid retrieval that combines keyword and vector search.

Official documentation: https://docs.weaviate.io/weaviate/concepts/indexing

## 4. Search Capability Comparison

| Capability | FAISS | ChromaDB | Pinecone | Weaviate |
|---|---|---|---|---|
| Vector similarity search | Yes | Yes | Yes | Yes |
| Keyword search built in | No | Yes | Sparse-vector lexical retrieval | Yes |
| Hybrid search built in | No; application logic needed | Supported | Supported | Supported |
| Metadata filtering | Application-managed | Yes | Yes | Yes |
| Stores document text and metadata | Application-managed | Yes | Metadata supported | Yes |
| Local self-hosting | Yes, as a library | Yes | Managed service | Yes |
| Managed cloud offering | Not as a standalone FAISS service | Yes | Yes | Yes |

Note: Keyword search implementations and hybrid-search behavior differ between products. FAISS can participate in hybrid retrieval, but requires additional components and application logic.

## 5. Suitability for Fewer Than One Million Vectors

### FAISS
Advantages:
- No separate vector database service is required.
- Efficient similarity search.
- Good control over index selection and application behavior.

Limitations:
- The application must manage metadata, text, persistence, and hybrid retrieval.
- Operational responsibility remains with the application.

Suitability: Good for a lightweight prototype when custom retrieval logic is acceptable.

### ChromaDB
Advantages:
- Simple local development workflow.
- Stores embeddings, document text, and metadata together.
- Supports vector search, full-text search, and hybrid retrieval.
- Provides persistence options.

Limitations:
- Memory, storage, and latency depend on embedding dimensions, metadata, document size, hardware, and workload.
- Resource requirements must be tested using the actual dataset.

Suitability: Strong candidate for the MediAssist AI local RAG prototype.

### Pinecone
Advantages:
- Managed infrastructure.
- Supports dense and sparse vector retrieval.
- Reduces database-operation responsibilities.

Limitations:
- Requires external service access and configuration.
- Usage costs and data-governance requirements must be considered.
- Local development is more dependent on network access.

Suitability: Appropriate if managed infrastructure is preferred and external processing of the approved data is permitted.

### Weaviate
Advantages:
- Supports vector and keyword retrieval.
- Provides hybrid search and metadata filtering.
- Offers configurable index types and self-hosted deployment.

Limitations:
- More configuration and operational concepts than a minimal local library.
- Resource requirements depend on index choice and workload.

Suitability: Strong candidate when integrated keyword and vector retrieval and a more feature-rich database are priorities.

## 6. Preliminary Recommendation

For the initial MediAssist AI prototype, **ChromaDB is the recommended candidate to evaluate first** because it combines local persistence, document and metadata storage, vector retrieval, keyword search, and hybrid retrieval in one system.

FAISS remains a good alternative if minimal infrastructure and custom retrieval implementation are priorities.

Pinecone and Weaviate should remain comparison candidates until deployment, privacy, operational, and cost requirements are validated.

This is a preliminary engineering recommendation, not a measured performance result. The final selection should follow a small benchmark using representative hospital-document chunks and questions.

## 7. Proposed Evaluation Plan

Test the selected candidates using the same representative, approved dataset and embedding model.

Measure:
- Index creation and ingestion time.
- Query latency.
- Retrieval relevance and Recall@k.
- Keyword-search effectiveness for exact terms and policy identifiers.
- Hybrid-search effectiveness compared with vector-only search.
- Metadata-filter correctness.
- Persistence and reload behavior.
- Memory and storage consumption.
- Operational complexity and estimated service costs.

Do not claim that one database is faster or more accurate until these tests have been performed.

## 8. Security and Privacy

- Do not upload database credentials, API secrets, or environment files to GitHub.
- Keep real patient-identifying data out of public repositories.
- Use approved, fictional, or de-identified test material for retrieval experiments.
- Verify data-handling and deployment requirements before sending hospital documents to a hosted service.
- Preserve source identifiers and metadata so retrieved information can be traced to its approved source.

## 9. Decision Status

Status: Comparison documented; database selection not yet validated by benchmark.

The comparison supports the next tracker phase, where the vector database setup and retrieval behavior will be implemented and tested.

## 10. References

- FAISS: https://faiss.ai/
- ChromaDB: https://docs.trychroma.com/
- ChromaDB architecture: https://docs.trychroma.com/docs/overview/architecture
- Pinecone: https://docs.pinecone.io/
- Weaviate vector indexing: https://docs.weaviate.io/weaviate/concepts/indexing/vector-index
- Weaviate indexing: https://docs.weaviate.io/weaviate/concepts/indexing

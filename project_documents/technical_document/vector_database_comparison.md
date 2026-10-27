# Vector Database Comparison

## Objective
Compare vector storage options for the MediAssist AI retrieval-augmented generation (RAG) pipeline.

## Evaluation Criteria
- Semantic similarity search
- Integration with the selected embedding model
- Local development and deployment support
- Metadata filtering
- Persistence and data management
- Scalability and operational complexity
- Privacy and security requirements

## Candidate 1: FAISS
- Provides efficient similarity search over dense vectors.
- Supports local development.
- Requires separate handling for document metadata and associated text.
- Persistence and retrieval logic must be implemented by the application.
- Suitable for a lightweight initial prototype.

## Candidate 2: ChromaDB
- Provides vector storage and similarity search.
- Supports document text and metadata alongside embeddings.
- Offers local persistence options.
- Can simplify prototyping of a RAG pipeline.
- Requires evaluation for the intended deployment and workload.

## Candidate 3: Managed Vector Database
- Can reduce some infrastructure management responsibilities.
- May provide hosted scaling and operational features.
- Introduces external service, cost, network, and data-governance considerations.
- Must be assessed against the project's privacy and deployment requirements.

## Preliminary Recommendation
Use FAISS as the initial candidate for a local prototype because it supports efficient similarity search without requiring a separate vector database server.

This is a preliminary engineering recommendation. The final selection must be validated against the requirements in the project specification and the expected retrieval workflow.

## Integration Considerations
The embedding model currently produces 384-dimensional normalized vectors. The selected vector store must accept vectors of the correct dimension and reliably associate search results with their original text chunks and metadata.

The vector store is for document retrieval; it must not replace PostgreSQL as the system of record for structured application data.

## Security
Do not store database credentials, API secrets, or unnecessary patient-identifying information in the vector index. Use approved documents and follow the project's access-control and privacy requirements.

## Validation Plan
- Add representative document chunk vectors.
- Perform similarity searches using sample queries.
- Verify that retrieved results map to the correct source text.
- Test index persistence and reload behavior.
- Evaluate retrieval relevance before finalizing the choice.

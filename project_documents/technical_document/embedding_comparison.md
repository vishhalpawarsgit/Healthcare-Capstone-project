# Embedding Model Comparison

## Objective
Evaluate text embedding options for the MediAssist AI retrieval-augmented generation (RAG) pipeline.

## Evaluation Criteria
- Semantic retrieval quality for healthcare procedures and hospital policies
- Support for medical terminology
- Embedding dimensions and storage requirements
- Local execution and API availability
- Processing speed
- Cost and privacy considerations
- Integration with the selected vector database

## Candidate Models

### 1. sentence-transformers/all-MiniLM-L6-v2
- Runs locally.
- Produces 384-dimensional embeddings.
- Suitable for an initial lightweight semantic-search prototype.
- Requires testing against the project's actual hospital documents.

### 2. BAAI/bge-small-en-v1.5
- Runs locally.
- Produces 384-dimensional embeddings.
- Designed for English text retrieval tasks.
- Requires evaluation with the project's hospital documents.

### 3. OpenAI text-embedding-3-small
- Hosted embedding API.
- Supports configurable embedding dimensions.
- Requires API access and consideration of data-handling requirements and usage costs.
- Should only be used with approved, appropriately protected data.

## Preliminary Recommendation
Use `sentence-transformers/all-MiniLM-L6-v2` as the initial prototype candidate because it supports local embedding generation and keeps the first experiment simple.

This is a preliminary engineering choice, not a validated healthcare performance result. Compare the candidates using representative, fictional or de-identified hospital questions before making a final selection.

## Privacy and Safety
Do not embed database credentials, secrets, or unnecessary patient-identifying information. Use only approved documents and follow the project's data-access and privacy requirements.

## Validation Plan
- Generate embeddings from representative text chunks.
- Confirm embedding dimensions and successful processing.
- Evaluate retrieval relevance using a small set of test questions.
- Record latency and resource usage.
- Document the final model choice and its limitations.

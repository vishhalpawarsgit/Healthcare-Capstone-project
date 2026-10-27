# Embedding Pipeline

## Objective
Convert text chunks from hospital documents into numerical vectors for semantic retrieval in the MediAssist AI RAG pipeline.

## Selected Prototype Model
- Model: `sentence-transformers/all-MiniLM-L6-v2`
- Embedding dimensions: 384
- Execution: Local model inference
- Output: Normalized numerical vectors

## Implementation
The reusable embedding module is implemented in `app/embeddings/embedding_model.py`.

The `EmbeddingModel` class loads the selected model, encodes a list of text strings, and exposes the model's embedding dimension.

## Validation Results
- Package import: Passed
- Model loading: Passed
- Two-sentence embedding test: Passed
- Real hospital SOP test: Passed
- Admission SOP chunks created: 9
- Chunks embedded in the test: 5
- Vector dimensions: 384

## Limitations
The real-document test embedded only the first five chunks. The vectors were generated in memory and were not persisted to a vector database. Healthcare-specific retrieval quality has not yet been evaluated.

The PDF parser reported malformed object-reference warnings, so extracted text should be reviewed for completeness before production use.

## Outcome
The embedding component is implemented and its basic functionality has been validated. The model remains a prototype choice pending retrieval-quality evaluation.

## Full SOP Embedding Validation

The embedding pipeline was tested against the complete extracted text of `Admission Process- SOP.pdf`.

Results:
- Total text chunks created: 9
- Chunks embedded: 9
- Embedding dimensions: 384
- Output shape: `(9, 384)`
- Validation result: Passed

All chunks were embedded successfully, and the number of generated vectors matched the number of input chunks.

The embeddings were generated in memory. Persistent vector storage and retrieval evaluation remain separate tasks.

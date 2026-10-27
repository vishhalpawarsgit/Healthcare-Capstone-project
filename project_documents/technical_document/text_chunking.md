# Text Processing and Chunking

## Objective
Prepare extracted hospital document text for retrieval-augmented generation (RAG) by dividing it into smaller, manageable text chunks.

## Implementation
The chunking utility is implemented in `app/chunking/text_chunker.py`.

It accepts extracted text and configurable chunk settings, then returns a list of chunks containing a chunk index and text.

## Chunking Configuration
- Chunk size: 1,000 characters
- Chunk overlap: 150 characters

The overlap preserves some context between adjacent chunks.

## Validation
The following checks passed:
- Basic chunking and overlap test
- Empty text handling
- Invalid configuration handling
- Real hospital SOP chunking test using `Admission Process- SOP.pdf`

## Limitations
The current implementation splits text by character count. It does not yet preserve semantic boundaries such as paragraphs, headings, or complete sentences.

## Outcome
The text chunking utility is implemented and its basic behavior has been validated. It is ready for integration with the embedding and retrieval pipeline in later phases.

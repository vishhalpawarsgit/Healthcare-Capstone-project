# Text Cleaning and Chunking Strategies

## Objective
Prepare extracted hospital document text for embedding and retrieval in the MediAssist AI RAG pipeline.

## Text Cleaning
The current document loader strips leading and trailing whitespace from extracted text. Additional cleaning should preserve clinically and operationally meaningful information, including headings, dates, policy identifiers, and procedural steps.

Potential cleaning operations include:
- Normalize unnecessary whitespace.
- Remove repeated extraction artifacts when verified.
- Preserve meaningful paragraph and section boundaries.
- Inspect extracted text for PDF parsing errors.
- Avoid removing clinically significant values or policy details.

## Strategy 1: Fixed-Size Character Chunking
Split text into chunks with a configured maximum character count.

Advantages:
- Simple to implement.
- Predictable chunk size.
- Easy to test.

Limitations:
- May split sentences or headings.
- Chunk size is measured in characters, not tokens.

## Strategy 2: Overlapping Character Chunking
Create fixed-size chunks with a configurable overlap between adjacent chunks.

Advantages:
- Preserves some context across chunk boundaries.
- Straightforward to implement.

Limitations:
- Repeats some text.
- Can increase storage requirements.
- Does not guarantee complete semantic units.

Current implementation: `app/chunking/text_chunker.py`, using a prototype configuration of 1,000 characters and 150 characters of overlap.

## Strategy 3: Sentence-Based Chunking
Split text at sentence boundaries and group sentences until a target chunk size is reached.

Advantages:
- Better preserves complete sentences.
- Can improve readability of retrieved passages.

Limitations:
- Sentence boundary detection may be unreliable for abbreviations, tables, and medical notation.
- Requires additional implementation and testing.

## Strategy 4: Semantic or Section-Based Chunking
Use document headings, sections, paragraphs, or semantic similarity to define chunk boundaries.

Advantages:
- Can preserve the context of hospital procedures and policy sections.
- May improve retrieval of complete procedural instructions.

Limitations:
- Requires more processing and evaluation.
- Document formatting may be inconsistent.
- Semantic boundaries are not guaranteed to improve retrieval without testing.

## Current Status
Fixed-size overlapping character chunking is implemented and tested. Sentence-based and semantic or section-based approaches are documented as alternatives, but have not yet been implemented or benchmarked.

## Validation Plan
Compare strategies using approved hospital documents and representative test questions. Assess retrieval relevance, preservation of procedural context, chunk count, and processing cost before selecting a final strategy.

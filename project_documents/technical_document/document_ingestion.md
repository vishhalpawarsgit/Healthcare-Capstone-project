# MediAssist AI — Document Ingestion Pipeline

## 1. Objective

Implement an initial document loader for the MediAssist AI capstone that extracts text from supported source documents.

## 2. Supported Formats

- PDF
- DOCX
- TXT

## 3. Implementation

The loader is implemented in `app/ingestion/document_loader.py`.

It validates the file path and extension, extracts text using the appropriate reader, and returns the source filename, file type, extracted text, and basic metadata.

Libraries used:
- `pypdf` for PDF text extraction.
- `python-docx` for DOCX text extraction.
- Python's built-in file handling for TXT files.

## 4. Source Data Tested

The following five PDF documents were placed in `data/raw_data/`:

1. `Admission Process- SOP.pdf`
2. `Standard Operating Procedure.pdf`
3. `SAMPLE DISCHARGE SUMMARIES.pdf`
4. `HOSPITAL OPERATIONS .pdf`
5. `HOSPITAL COMPLIANCE.pdf`

## 5. Test Results

The test script `app/ingestion/test_document_loader.py` processed all five PDF files.

Observed result:
- Total PDFs: 5
- Failed or empty: 0
- Overall result: Passed

The test verified that each PDF produced extracted text and did not raise an exception.

## 6. Current Limitations

- Scanned PDFs may require OCR if they contain no extractable text.
- Complex tables and layouts may not retain their original structure after extraction.
- DOCX and TXT support is implemented but requires separate test cases.
- File-size limits and additional validation will be addressed where required by the application specification.

## 7. Next Tracker Phase

Phase 5: Text Processing and Chunking.

Chunk size, overlap, chunking strategy, and trade-offs will be documented and tested in the next phase.
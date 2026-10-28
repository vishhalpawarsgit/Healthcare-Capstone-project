# Phase 11: Streamlit Frontend

## Objective
Build a Streamlit-based chatbot interface for MediAssist AI.

## Implemented Features
- Chat interface for submitting questions and displaying answers.
- FIFO chat display limited to the latest five individual messages.
- PDF, DOCX, TXT, JPG, JPEG, and PNG upload support.
- Maximum upload size of 50 MiB per file.
- Text extraction, chunking, embedding generation, and temporary FAISS indexing for uploaded files.
- OCR-based text extraction from supported JPG, JPEG, and PNG images using Tesseract.
- Semantic retrieval with keyword-based reranking for uploaded documents.
- Source citations showing document filename, chunk index, and similarity score.
- Indexed-document section showing uploaded filenames and chunk counts.
- Integration with the Phase 10 RAG engine when uploaded-document retrieval returns no results.
- Safe fallback when retrieval does not find sufficiently relevant supporting information.
- Validation for empty files, unsupported formats, invalid images, and oversized files.

## Validation
- Streamlit application launched successfully.
- Questions submitted through the chat interface and answers displayed.
- Uploaded PDF processed into chunks and returned source citations.
- Fictional visitor-policy image OCR tested successfully; retrieval returned the image filename as its source.
- Fictional nursing-admission SOP retrieved with its source citation.
- Unsupported cafeteria-menu question returned the safe fallback after retrieval threshold tuning and app restart.
- Multiple document uploads and duplicate-processing behavior tested.
- Empty-file rejection tested.
- Unit tests cover supported uploads, OCR handling, invalid inputs, and the 50 MiB size limit.
- Browser upload test confirmed rejection of a file exceeding 50 MiB.
- FIFO code selects the latest five individual messages; a diagnostic counter confirmed five messages selected for display.

## Limitations
- This is a prototype, not a production clinical decision-support system.
- Retrieval similarity scores do not guarantee answer correctness.
- Thresholds require broader evaluation against relevant and irrelevant questions.
- OCR quality depends on image clarity and layout.
- Uploaded-document indexing is temporary and held in application session state.
- The database source category, authentication, and other remaining capstone requirements are not implemented by this phase alone.
- Production deployment and security require further testing.

## Outcome
The Streamlit frontend and uploaded-document retrieval workflow have been implemented and tested for the current prototype. Remaining capstone requirements must be completed and validated in their designated tracker phases.

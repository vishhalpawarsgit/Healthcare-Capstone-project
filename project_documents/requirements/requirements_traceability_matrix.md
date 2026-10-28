# MediAssist AI — Requirements Traceability Matrix

**Purpose:** Track the original capstone brief, Functional Specification Document (FSD), and Streamlit template against the project implementation.

**Scope reviewed:** Work completed through Phase 11, based on progress reported in this conversation.

## Status definitions

- **Implemented and tested** — implementation exists and a relevant test or observed working behaviour has been reported.
- **Partially implemented** — a prototype or part of the requirement exists, but full acceptance criteria are not verified.
- **Not implemented** — no implementation has been reported yet.
- **Needs verification** — code may exist, but the specific criterion has not been tested or evidenced.
- **Documented/planned** — design documentation exists, but that alone does not count as implementation.

Statuses are intentionally conservative. Installing a library or describing a component in architecture documentation does not prove that the requirement is implemented.

## A. Phase tracker mapping (Phases 1–11)

| Tracker phase | Requirement area | Evidence/status known so far | Status | Follow-up |
|---|---|---|---|---|
| 1. Requirements understanding | Requirements, users, use cases, acceptance criteria | `project_documents/requirements/requirements.md` created and expanded | Documented | Reconcile with all requirements in this matrix |
| 2. Solution architecture | System architecture and component flow | `architecture.md`, `high_level_design.md` | Documented/planned | Keep diagrams aligned with actual implementation |
| 3. Project setup & planning | Repository, folders, environment, dependencies | Git repository, `.venv`, `.gitignore`, project folders | Implemented and tested | Keep dependency setup reproducible |
| 4. Document ingestion | PDF/DOCX/TXT extraction | `app/ingestion/document_loader.py`; five supplied PDFs loaded; fictional DOCX/TXT tests | Implemented and tested for prototype | Add size, corrupt-file, unsupported-file and scanned-PDF tests |
| 5. Text chunking | Chunk creation and overlap | `app/chunking/text_chunker.py`; fixed-size overlapping chunks and tests | Implemented and tested | Evaluate section-aware chunking and quality |
| 6. Embeddings | Hugging Face embeddings | `app/embeddings/embedding_model.py`; all-MiniLM-L6-v2, 384 dimensions | Implemented and tested | Evaluate retrieval quality on representative data |
| 7. Vector DB comparison | FAISS/ChromaDB/Pinecone/Weaviate | `vector_database_comparison.md` | Documented | Comparison is not a performance benchmark |
| 8. Vector database setup | Vector indexing and persistence | FAISS `IndexFlatIP`, metadata, persistence and tests | Implemented and tested for prototype data | Test larger corpus and metadata integrity |
| 9. Retrieval strategy | Semantic top-k search | `retrieval_strategy.md`; query embeddings and ranked retrieval | Implemented and tested for prototype | Hybrid search, metadata filtering and retrieval evaluation remain |
| 10. Enterprise RAG | Retrieval, context, citations and response | Retriever, context formatter, RAG engine and tests | Partially implemented | Current response generation is extractive; LLM synthesis and robust grounding remain |
| 11. Streamlit frontend | Chat, uploads, citations, indexed files | `frontend/streamlit_app.py`; PDF/DOCX/TXT upload and citations; chunk count displayed | Partially implemented | Verify FIFO last-five-message rule, image upload, source categories, limits and errors |

## B. FSD functional requirements

The IDs below follow the supplied Functional Specification Document.

| FSD ID | Requirement | Current status | Evidence / gap | Acceptance evidence still needed |
|---|---|---|---|---|
| FR-001 | User authentication | Not implemented | Login not reported | Valid credentials allow access; invalid credentials show error |
| FR-002 | Conversational AI assistant | Partially implemented | Chat and citations work; 15-second target not measured | Measure latency and verify sources for supported questions |
| FR-003 | Document upload (PDF/DOCX/TXT; max 50 MB) | Partially implemented | Formats upload and index; 50 MB limit not verified | Test formats, size boundary, unsupported/corrupt files and errors |
| FR-004 | Image upload (JPG/JPEG/PNG) | Not implemented | Uploaded-document index accepts PDF/DOCX/TXT | Upload each image format and display extracted information |
| FR-005 | Ingestion pipeline | Partially implemented | Parsing → chunking → embeddings → FAISS indexing exists | Show new uploads are searchable; test edge cases |
| FR-006 | Enterprise RAG: semantic, hybrid and metadata filtering | Partially implemented | Semantic top-k and citations exist; hybrid search and metadata filters not implemented | Test top-k relevance, hybrid retrieval, filters and grounding |
| FR-007 | Planner Agent | Not implemented | LangGraph planner not reported | Demonstrate complex request decomposed into subtasks |
| FR-008 | Multimodal Agent: OCR, extraction, vision reasoning | Not implemented | Image pipeline and BLIP/LLaVA not reported | Test prescription/report images and extracted fields |
| FR-009 | MCP server for PostgreSQL | Not implemented | No working MCP server reported | Demonstrate database access occurs through MCP |
| FR-010 | MCP Agent dynamically invokes tools | Not implemented | Tool routing not reported | Demonstrate tool selection and invocation |
| FR-011 | PostgreSQL structured-data retrieval | Not implemented | Patient/appointment/billing/lab queries not reported | Test approved read-only queries against provided schema |
| FR-012 | Reasoning Agent synthesizes prompt, RAG, MCP and vision | Partially implemented at prototype level | Extractive RAG exists; multi-source synthesis does not | Show grounded multi-source response with attribution |
| FR-013 | Evaluation Agent | Not implemented | LLM-as-a-Judge not integrated | Evaluate faithfulness, relevance, grounding and hallucination risk |
| FR-014 | Session history and multi-turn context | Partially implemented | Chat history displayed | Verify context continuation and FIFO retention |
| FR-015 | Evaluation dashboard | Not implemented | Traces, latency, token usage and hallucination dashboard not reported | Display actual measurements |
| FR-016 | Azure deployment | Not implemented | Deployment not reported | Deploy required components and verify endpoint |

## C. Streamlit template requirements

| Template requirement | Current status | Gap / verification |
|---|---|---|
| Healthcare chatbot UI | Partially implemented | Existing MediAssist AI chat interface runs |
| Upload documents | Partially implemented | PDF/DOCX/TXT supported |
| Display uploaded document names | Implemented and observed | Filename appears in indexed-document section |
| Display indexed chunk count | Implemented and observed | Chunk count appears in UI |
| Show answer sources and citations | Implemented and observed for document RAG | Ensure cited passages support the answer |
| Upload images (PNG examples in template) | Not implemented | Add JPG/JPEG/PNG upload and image processing |
| Show sources from external RAG, images and database | Partially implemented | Document RAG exists; image/database sources remain |
| Retain only last five messages using FIFO | Needs verification | Test and implement if missing; clarify whether five individual messages or five user/assistant turns |
| Match reference layout and labels | Needs verification | Compare running UI with both template pages |

## D. Technology and architecture requirements

| Technology / capability | Current status | Next work |
|---|---|---|
| Python and virtual environment | Implemented and tested | Keep setup documented |
| Streamlit | Implemented | Complete template acceptance checks |
| pypdf and python-docx | Implemented and tested | Add error and size tests |
| Hugging Face Sentence Transformers | Implemented and tested | Evaluate retrieval quality |
| FAISS | Implemented and tested for prototype | Hybrid retrieval and metadata filters remain |
| FastAPI | Not implemented as of Phase 11 | Phase 12: API endpoints and tests |
| LangChain | Needs verification / not reported integrated | Decide its role; avoid adding without a clear purpose |
| LangGraph | Not implemented | Add agent orchestration in a later planned phase |
| OpenAI or Groq LLM | Not integrated | Select provider, configure secrets securely, implement generation |
| MCP Python SDK / MCP server | Not implemented | Build controlled tool server and tests |
| PostgreSQL connector and MCP tools | Not implemented | Integrate only through MCP with least privilege |
| Vision model (BLIP/LLaVA or selected equivalent) | Not implemented | Image extraction and multimodal reasoning |
| LLM-as-a-Judge | Not implemented | Evaluation criteria, test set, metrics and report |
| Docker / Docker Compose | Not implemented | Containerize and test services |
| Azure hosting | Not implemented | Deploy and verify endpoint |
| Logging, tracing and observability | Needs verification | Add structured logs, request IDs, timings and agent traces |
| Guardrails / prompt-injection protection | Not implemented / needs verification | Add input, tool and output controls with tests |
| Streaming responses | Needs verification | Capstone requires streaming; test UI/backend |
| Authentication and authorization | Not implemented | Define role-aware access and test denied access |

## E. Non-functional requirements

| Requirement | Current status | Acceptance evidence needed |
|---|---|---|
| NFR-001 Modular architecture | Partially implemented | Verify modules have clear interfaces and independent tests |
| NFR-002 Dockerized deployment | Not implemented | Build and run Docker/Compose |
| NFR-003 API-first design | Not implemented yet | FastAPI routes and frontend-backend calls |
| NFR-004 Logging and tracing | Needs verification | Logs capture request, outcome, errors and latency without sensitive data |
| NFR-005 Agent observability | Not implemented | Agent execution traces and timings |
| NFR-006 Config-driven architecture | Partially implemented / needs verification | Validated configuration; secrets excluded from source |
| NFR-007 Error handling and retries | Partially implemented / needs verification | Test invalid files, empty retrieval, API failures, timeouts and recovery |
| NFR-008 Scalable retrieval | Prototype only | Benchmark representative data volume and latency |

## F. Data, privacy and safety requirements

| Requirement | Current status | Follow-up |
|---|---|---|
| Provided healthcare documents | Ingestion tested with five PDFs; compliance PDF retrieval tested | Confirm authorization; do not commit private source data to public GitHub |
| Multimodal healthcare images | Not implemented | Use approved, fictional or de-identified images for development |
| PostgreSQL schema and sample data | Not integrated | Inspect approved schema without exposing credentials |
| Multi-branch reporting and analytics | Not implemented | Implement after MCP-backed structured retrieval |
| Secure credential handling | Needs verification | Rotate any previously exposed database credential; use environment variables/secrets and `.gitignore` |
| Privacy and access controls | Not implemented / needs verification | Avoid real patient data in public repositories/logs; implement required role-based access |
| Clinical safety and grounded answers | Partially implemented at RAG prototype level | Cite supporting passages, handle insufficient evidence and test hallucination risks |

## G. Proposed plan for remaining work

This mapping is a proposal, not a replacement for the Excel tracker. Reconcile it with the exact remaining tracker phases before changing the phase order.

| Planned work area | Requirements addressed |
|---|---|
| Phase 11 close-out | Streamlit template checks, FIFO history, upload limits/errors, source display and documentation |
| Phase 12: FastAPI backend | API routes, validation, errors, schemas and frontend-backend communication |
| Subsequent RAG improvements | Hybrid search, metadata filtering, retrieval evaluation and stronger grounding |
| Agent orchestration | LangGraph planner, retriever, reasoning and controlled workflow |
| MCP and PostgreSQL | MCP server, approved read-only tools, structured retrieval and MCP-agent invocation |
| Multimodal processing | Image uploads, OCR/vision extraction and report/prescription understanding |
| Evaluation and observability | LLM-as-a-Judge, metrics, traces, dashboard and evaluation report |
| Security and reliability | Authentication, authorization, guardrails, secrets, retries and edge cases |
| Deployment | Docker/Compose, Azure deployment, endpoint verification and documentation |
| Final acceptance testing | End-to-end user stories, latency, citations, multi-source answers and demo evidence |

## H. Evidence log template

| Date | Requirement ID | Test scenario | Expected result | Actual result | Evidence / file | Status |
|---|---|---|---|---|---|---|
| YYYY-MM-DD | FR-xxx / NFR-xxx | Describe test | Expected behaviour | Observed behaviour | Test file, screenshot or log reference | Status |

## I. Completion rule

Mark a requirement **Implemented and tested** only when:
1. Relevant code or configuration exists.
2. A test or reproducible manual verification exercises it.
3. The observed result meets the acceptance criterion.
4. Evidence is recorded.
5. Limitations are documented.

Do not claim the complete capstone is finished merely because Phases 1–11 are complete. The final system must satisfy the relevant FSD modules, template behaviours, security requirements, evaluation deliverables and deployment criteria.

# MediAssist AI — High-Level Design (HLD)

## 1. Purpose

This document describes the high-level design of MediAssist AI, an enterprise healthcare AI copilot.

## 2. System Components

### Frontend
**Technology:** Streamlit

Provides the chat interface, document and image uploads, source display, and evaluation dashboard.

### Backend
**Technology:** FastAPI

Provides API endpoints for document uploads, retrieval, chat requests, and health checks.

### Agent Orchestration
**Technology:** LangGraph

Coordinates the Planner, Retriever, MCP, Multimodal, Reasoning, and Evaluation agents.

### Document Retrieval
**Technologies under consideration:** Hugging Face embeddings and FAISS or ChromaDB

Processes documents into chunks, creates embeddings, indexes content, and retrieves relevant evidence for user queries.

### Structured Data
**Technology:** PostgreSQL accessed through MCP

Provides controlled access to structured healthcare records through approved tools.

### Multimodal Processing
**Technologies under consideration:** OCR and vision models such as BLIP or LLaVA

Extracts information from supported medical report images.

### Evaluation and Observability
Evaluates answer relevance, faithfulness, grounding, and hallucination risk. Logging and tracing support troubleshooting.

## 3. High-Level Request Flow

1. A user submits a question or uploads a file in Streamlit.
2. FastAPI receives the request.
3. LangGraph coordinates the appropriate workflow.
4. The Planner identifies which capabilities are needed.
5. Retrieval, MCP, or multimodal processing supplies relevant evidence.
6. The Reasoning Agent prepares an evidence-based answer.
7. The Evaluation Agent assesses response quality.
8. The response and available sources are returned to the frontend.

## 4. Data Flow

### Document data
Source documents → text extraction → chunking → embeddings → vector index → retrieval.

### Structured healthcare data
User question → MCP Agent → MCP tools → PostgreSQL → structured results → reasoning workflow.

### Image data
Uploaded image → OCR and/or vision processing → extracted evidence → reasoning workflow.

## 5. API Overview

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/upload-document` | Accept documents for ingestion |
| POST | `/retrieve` | Retrieve relevant document chunks |
| POST | `/chat` | Process a chat request |
| GET | `/health` | Check backend health |

These are planned endpoints; implementation details will be confirmed during Phase 12.

## 6. Security and Safety

- Agents access PostgreSQL through MCP tools, not direct database connections.
- Secrets are stored in environment configuration.
- Uploaded content is treated as untrusted input.
- Responses should be grounded in available evidence.
- The system must not invent medical recommendations.
- Sensitive healthcare information must be protected.

## 7. Deployment

The planned application will use Docker for containerization, with Azure Container Apps as the deployment target.

## 8. Decisions to Confirm

- Embedding model selection.
- Vector database selection.
- Language and vision model availability.
- Database schema and MCP tool parameters.
- Final API request and response formats.
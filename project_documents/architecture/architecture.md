# MediAssist AI — Solution Architecture

## 1. Architecture Overview

MediAssist AI is an enterprise healthcare AI copilot. The application uses a Streamlit frontend, FastAPI backend, LangGraph agent orchestration, a retrieval pipeline for hospital documents, MCP tools for structured healthcare data, and multimodal processing for medical report images.

## 2. High-Level Request Flow

1. The user submits a question or uploads a document or image through Streamlit.
2. Streamlit sends the request to the FastAPI backend.
3. FastAPI forwards the request into the LangGraph orchestration workflow.
4. The Planner Agent determines which capabilities are needed.
5. The workflow invokes the relevant retrieval, MCP, or multimodal components.
6. The Reasoning Agent combines the available evidence.
7. The Evaluation Agent checks the response for relevance, grounding, faithfulness, and hallucination risk.
8. The final response is returned to Streamlit with supporting sources where available.

## 3. Main Components

### 3.1 Frontend — Streamlit
Responsibilities:
- Conversational chat interface.
- PDF and other supported document uploads.
- Medical report image uploads.
- Display answers and supporting sources.
- Display evaluation results.

### 3.2 Backend — FastAPI
Responsibilities:
- Expose API endpoints.
- Accept document and image uploads.
- Handle chatbot requests.
- Provide retrieval endpoints.
- Provide a health-check endpoint.
- Connect frontend requests to the agent workflow.

### 3.3 Agent Orchestration — LangGraph
The planned workflow coordinates these agents:

- **Planner Agent:** determines the intended task and required capabilities.
- **Retriever Agent:** retrieves relevant content from the document index.
- **MCP Agent:** invokes approved tools for structured healthcare data.
- **Multimodal Agent:** processes medical report images and OCR output.
- **Reasoning Agent:** prepares an evidence-based response from available results.
- **Evaluation Agent:** evaluates response quality, grounding, and hallucination risk.

### 3.4 Document Ingestion and RAG
The document pipeline will:
1. Load supported documents.
2. Extract and normalize text.
3. Split text into chunks.
4. Generate embeddings.
5. Store vectors and associated metadata.
6. Embed incoming queries.
7. Retrieve relevant chunks using similarity search and, where implemented, hybrid retrieval and metadata filters.
8. Supply retrieved evidence to the response workflow.

FAISS and ChromaDB are candidates for the vector store. The final choice will be documented after comparison in the relevant tracker phase.

### 3.5 Structured Healthcare Data — MCP and PostgreSQL
PostgreSQL stores structured healthcare information supplied for the capstone. The MCP server exposes approved tools to retrieve relevant data.

Important design rule: agents must access PostgreSQL through MCP tools rather than connecting directly to the database.

Planned tool capabilities include patient history, appointments, lab results, billing, prescriptions, admissions, doctor schedules, insurance details, and department statistics, subject to the supplied schema and data.

### 3.6 Multimodal Processing
The multimodal workflow accepts supported medical report images and uses OCR and/or a vision model to extract relevant information. The response must be grounded in the available image evidence and must not invent medical recommendations.

### 3.7 Evaluation and Observability
The system will evaluate responses for:
- Relevance.
- Faithfulness to retrieved evidence.
- Grounding and citation support.
- Hallucination risk.

LLM-as-a-Judge is a required evaluation approach. Logging and tracing will support troubleshooting and agent observability.

## 4. Data Stores

- **Vector store:** indexed document chunks, embeddings, and metadata.
- **PostgreSQL:** structured healthcare records, accessed through MCP.
- **Source documents:** supplied hospital policies, procedures, reports, and related reference material.

## 5. API Responsibilities

The planned FastAPI interface includes:
- `POST /upload-document` — accept documents for ingestion.
- `POST /retrieve` — retrieve relevant document chunks.
- `POST /chat` — process a conversational request.
- `GET /health` — check backend health.

Exact request and response schemas will be defined during backend implementation.

## 6. Deployment Architecture

The application will be containerized using Docker. Azure Container Apps is the specified deployment target. Environment-specific configuration and credentials will be managed separately from source code.

## 7. Security and Safety Principles

- Route structured database access through MCP.
- Keep secrets in environment configuration rather than committing them to Git.
- Treat uploaded documents as untrusted input.
- Protect sensitive healthcare information.
- Ground answers in available evidence.
- Avoid unsupported diagnoses or invented treatment recommendations.
- Evaluate responses before presenting them where required by the workflow.

## 8. Implementation Scope

This architecture document supports Phases 1–12 of the Excel tracker. Later implementation phases are outside the current scope.

## 9. Architecture Decisions Pending Validation

- Final vector store: FAISS or ChromaDB.
- Final embedding model.
- Final language and vision models based on available credentials and requirements.
- Exact PostgreSQL schema and MCP tool parameters after the supplied database resources are available.
- Final API schemas and deployment configuration during implementation.



# MediAssist AI — Requirements Document

## 1. Purpose

MediAssist AI is an enterprise healthcare AI copilot that uses hospital documents, structured healthcare data, and medical report images to answer user questions with appropriate grounding and safeguards.

## 2. Functional Requirements

### FR-01: Document Upload
The system must support PDF, DOCX, and TXT documents.

### FR-02: Document Ingestion
The system must load documents, extract text, split text into chunks, generate embeddings, and prepare content for retrieval.

### FR-03: Enterprise RAG
The system must retrieve relevant document chunks using semantic or hybrid retrieval and metadata filters.

### FR-04: Conversational Assistant
The system must provide a conversational interface and answer questions using relevant retrieved information.

### FR-05: Structured Healthcare Data
The system must retrieve relevant healthcare information through MCP tools connected to PostgreSQL.

### FR-06: Multimodal Processing
The system must support medical report images and use OCR and/or vision models to extract relevant information.

### FR-07: Agent Orchestration
The system must coordinate specialized agents for planning, retrieval, database access, multimodal processing, reasoning, and evaluation.

### FR-08: Response Evaluation
The system must evaluate responses for relevance, faithfulness, grounding, and potential hallucinations, including LLM-as-a-Judge.

### FR-09: User Interface
The system must provide a Streamlit interface for chat, document uploads, image uploads, and evaluation results.

### FR-10: Backend APIs
The system must expose backend functionality through FastAPI endpoints, including document upload, retrieval, chatbot interaction, and health checks.

## 3. Non-Functional Requirements

- Modular and maintainable architecture.
- API-first backend design.
- Docker-based packaging.
- Logging, tracing, retries, and agent observability.
- Configuration managed through environment variables.
- Retrieval and responses must be evaluated.
- Sensitive healthcare information must be handled carefully.

## 4. Security and Safety

- Structured database access must go through MCP tools.
- Agents must not connect directly to PostgreSQL.
- Responses must be grounded in available evidence.
- The system must not invent medical recommendations.
- The system must account for prompt injection, sensitive information, hallucination, unsafe recommendations, and tool misuse.

## 5. Deployment Target

The planned deployment target is Azure Container Apps.

## 6. Scope

This working plan covers Phases 1–12 of the Excel project tracker only. Requirements that depend on supplied datasets, database schemas, or credentials will be confirmed when those resources are available.

## 7. Stakeholders and User Personas

### Hospital Operations Staff
Need to retrieve operational procedures, admission processes, duty rosters, and hospital policies from approved documents.

### Nursing Team
Need to find relevant operational procedures and coordinate tasks such as bed allocation and patient admission using approved hospital documentation.

### Hospital Administrators
Need access to operational policies, compliance requirements, and administrative procedures.

### Healthcare Support and Information Staff
Need to locate relevant information in hospital documents and approved structured data sources.

### Technical Administrators
Need to maintain the application, monitor system behavior, manage configuration, and investigate failures.

These personas are initial assumptions for the project and should be confirmed against the supplied specification and intended users.

## 8. Primary Use Cases and Workflows

### UC-01: Search Hospital Procedures
1. A user asks a question about a hospital procedure.
2. The system retrieves relevant document chunks.
3. The assistant generates an evidence-grounded answer.
4. The system identifies relevant source information where available.

### UC-02: Ingest Hospital Documents
1. An authorized user supplies a supported PDF, DOCX, or TXT document.
2. The ingestion pipeline extracts text.
3. The text is cleaned and divided into chunks.
4. The embedding pipeline generates vectors.
5. The content is prepared for retrieval.

### UC-03: Retrieve Structured Information
1. A user requests information available in an approved structured data source.
2. The system selects an authorized MCP tool.
3. The tool retrieves permitted information from PostgreSQL.
4. The assistant presents the result subject to access controls and applicable safeguards.

### UC-04: Process a Medical Report Image
1. A user supplies an approved medical report image.
2. The system extracts relevant information using OCR and/or a vision model.
3. The assistant summarizes the extracted information with appropriate limitations.
4. Unclear or unreadable content is identified rather than guessed.

### UC-05: Evaluate an Assistant Response
1. The system produces a response using available evidence.
2. Evaluation checks relevance, faithfulness, grounding, and potential hallucinations.
3. Evaluation results are recorded or displayed as supported by the implementation.

## 9. Dataset Inventory

The initial document collection contains:

- `Admission Process- SOP.pdf`
- `Standard Operating Procedure.pdf`
- `SAMPLE DISCHARGE SUMMARIES.pdf`
- `HOSPITAL OPERATIONS .pdf`
- `HOSPITAL COMPLIANCE.pdf`

These documents are intended for document ingestion and retrieval experiments.

The following items require separate confirmation before implementation:
- PostgreSQL schema and approved database access method.
- Availability and format of approved structured test data.
- Approved sample medical report images for multimodal testing.
- Any additional document formats or datasets required by the project specification.

Database credentials and other secrets must not be included in the document ingestion or version-control workflow.

## 10. Initial Acceptance Criteria

- Supported PDF, DOCX, and TXT files can be processed by the ingestion pipeline.
- Extracted text can be divided into non-empty chunks.
- The embedding pipeline generates vectors with the selected model's expected dimensions.
- Retrieval returns relevant source chunks for representative test questions.
- Structured database access is performed through authorized MCP tools rather than direct agent connections to PostgreSQL.
- Medical report image processing identifies extraction limitations rather than inventing unreadable content.
- Response evaluation checks grounding and faithfulness.
- The application exposes the planned Streamlit interface and FastAPI endpoints within the project scope.

These criteria are initial targets. Measurable quality thresholds and access-control details must be established before production readiness can be claimed.

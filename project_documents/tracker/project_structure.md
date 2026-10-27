# MediAssist AI — Project Structure

## Project Root

The project root contains application code, data directories, frontend and backend components, and project documentation.

## Directory Responsibilities

| Path | Purpose |
|---|---|
| `app/` | Core application modules and agent workflows |
| `backend/` | FastAPI backend application |
| `frontend/` | Streamlit user interface |
| `data/raw_data/` | Original source documents |
| `data/images/` | Uploaded medical report images |
| `data/processed/` | Processed document and text artifacts |
| `data/vector_store/` | Local vector index and related retrieval artifacts |
| `project_documents/requirements/` | Functional and non-functional requirements |
| `project_documents/architecture/` | Solution architecture documentation |
| `project_documents/tracker/` | Project tracker and planning documentation |
| `project_documents/technical_document/` | Technical design and implementation documentation |

## Root Documentation

- `README.md` provides the project overview.
- The requirements document defines the expected system behavior.
- The architecture document describes the planned components and request flow.

## Development Principles

- Keep modules organized by responsibility.
- Keep credentials and secrets out of source control.
- Use configuration for environment-specific settings.
- Access PostgreSQL through MCP tools.
- Keep the implementation within Phases 1–12 of the project tracker.
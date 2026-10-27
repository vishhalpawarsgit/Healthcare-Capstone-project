# Healthcare-Capstone-project

## MediAssist AI — Enterprise Healthcare Agentic AI Copilot

## 1. Project Overview

MediAssist AI is an enterprise healthcare AI copilot designed to answer questions using hospital documents, structured healthcare data, and medical report images.

## 2. Project Objectives

- Build a document ingestion and processing pipeline.
- Implement Enterprise Retrieval-Augmented Generation (RAG).
- Develop a conversational interface using Streamlit.
- Create backend APIs using FastAPI.
- Use LangGraph to coordinate specialized AI agents.
- Integrate PostgreSQL through a Model Context Protocol (MCP) server.
- Support image processing and OCR for medical reports.
- Evaluate responses for relevance, faithfulness, grounding, and hallucinations.
- Containerize the application and prepare for Azure Container Apps deployment.

## 3. Main Technologies

- Python
- Streamlit
- FastAPI
- LangChain and LangGraph
- OpenAI or Groq language models
- Hugging Face embeddings
- FAISS or ChromaDB
- PostgreSQL
- MCP Python SDK
- OCR and vision models
- Docker
- Azure Container Apps

## 4. Main Functional Modules

1. Requirements understanding
2. Solution architecture
3. Project setup and planning
4. Document ingestion pipeline
5. Text processing and chunking
6. Embedding pipeline
7. Vector database comparison
8. Vector database setup
9. Retrieval strategy
10. Enterprise RAG pipeline
11. Streamlit frontend
12. FastAPI backend

## 5. Healthcare Data and Safety

- Use the datasets and database schema supplied for the capstone.
- Access structured healthcare data through MCP tools rather than allowing agents to connect directly to PostgreSQL.
- Ground answers in retrieved documents or database results.
- Avoid inventing medical advice or recommendations.
- Protect sensitive information and handle unsafe or unsupported requests carefully.

## 6. Project Scope

This implementation covers Phases 1–12 of the project tracker. Later phases are outside the current scope unless explicitly requested.

## 7. Current Status

Project initialization is in progress. Requirements documentation is being prepared.

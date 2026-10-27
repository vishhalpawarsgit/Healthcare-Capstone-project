
import streamlit as st

from app.retrieval.rag_engine import RAGEngine
from app.retrieval.uploaded_document_index import UploadedDocumentIndex


# --------------------------------------------------
# Page configuration
# --------------------------------------------------
st.set_page_config(
    page_title="MediAssist AI",
    page_icon="🩺",
    layout="wide",
)

st.title("🩺 MediAssist AI")
st.caption("Healthcare Document Assistant | Prototype")

st.info(
    "This prototype retrieves passages from documents. "
    "It is not a substitute for clinical judgment or authorized hospital policy."
)


# --------------------------------------------------
# Session state
# --------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "Hello! I'm MediAssist AI. Upload a fictional or "
                "de-identified document, process it, and ask a question."
            ),
        }
    ]

if "uploaded_index" not in st.session_state:
    st.session_state.uploaded_index = UploadedDocumentIndex()

if "processed_uploads" not in st.session_state:
    st.session_state.processed_uploads = set()

if "rag_engine" not in st.session_state:
    st.session_state.rag_engine = None


# --------------------------------------------------
# Sidebar: Upload and process documents
# --------------------------------------------------
with st.sidebar:
    st.header("📎 Document Upload")

    uploaded_files = st.file_uploader(
        "Select healthcare documents",
        type=["pdf", "docx", "txt"],
        accept_multiple_files=True,
        help="Supported formats: PDF, DOCX, TXT.",
    )

    if st.button(
        "Process uploaded documents",
        disabled=not uploaded_files,
        use_container_width=True,
    ):
        progress = st.progress(0)
        successful_files = 0

        for position, uploaded_file in enumerate(uploaded_files):
            file_key = (
                uploaded_file.name,
                len(uploaded_file.getvalue()),
            )

            if file_key in st.session_state.processed_uploads:
                st.caption(f"Already processed: {uploaded_file.name}")
                progress.progress((position + 1) / len(uploaded_files))
                continue

            try:
                with st.spinner(f"Processing {uploaded_file.name}..."):
                    chunk_count = (
                        st.session_state.uploaded_index.add_uploaded_file(
                            uploaded_file.name,
                            uploaded_file.getvalue(),
                        )
                    )

                st.session_state.processed_uploads.add(file_key)
                successful_files += 1
                st.success(
                    f"{uploaded_file.name}: {chunk_count} chunks indexed."
                )

            except Exception as error:
                st.error(f"Could not process {uploaded_file.name}: {error}")

            progress.progress((position + 1) / len(uploaded_files))

        if successful_files:
            st.success("Document processing finished.")

    st.divider()
    st.subheader("Indexed documents")

    if st.session_state.uploaded_index.records:
        sources = sorted(
            {
                record["metadata"]["source"]
                for record in st.session_state.uploaded_index.records
            }
        )
        st.write(f"**Chunks indexed:** {len(st.session_state.uploaded_index.records)}")

        for source in sources:
            st.write(f"📄 {source}")
    else:
        st.caption("No uploaded documents have been indexed yet.")

    st.divider()
    st.caption(
        "Privacy: use fictional or de-identified test documents only. "
        "Uploads are held in memory for this app session and are not "
        "saved to the project's document folders by this app."
    )


# --------------------------------------------------
# Display chat history
# --------------------------------------------------
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# --------------------------------------------------
# Helpers
# --------------------------------------------------
def format_citations(citations):
    """Format citation metadata for display and chat history."""
    lines = []

    for citation in citations:
        source = citation.get("source", "Unknown source")
        chunk_index = citation.get("chunk_index", "Unknown")
        score = citation.get("score")

        line = f"- **Source:** {source} | **Chunk:** {chunk_index}"

        if score is not None:
            line += f" | **Similarity:** {score:.4f}"

        lines.append(line)

    return "\n".join(lines)


def answer_question(question):
    """Search uploaded documents first, then use the Phase 10 RAG index."""

    uploaded_results = st.session_state.uploaded_index.search(
        question,
        top_k=3,
    )

    if uploaded_results:
        # The first result has the highest similarity score.
        best_result = uploaded_results[0]
        answer = best_result["text"]

        citations = [
            {
                **result["citation"],
                "rank": rank,
                "score": result["score"],
            }
            for rank, result in enumerate(uploaded_results, start=1)
        ]

        return answer, citations, "uploaded_documents"

    # Lazy initialization avoids loading the embedding model twice at startup.
    if st.session_state.rag_engine is None:
        st.session_state.rag_engine = RAGEngine(top_k=3)

    response = st.session_state.rag_engine.answer(question)

    return (
        response["answer"],
        response.get("citations", []),
        response.get("generation_method", "extractive"),
    )


# --------------------------------------------------
# Chat input and retrieval
# --------------------------------------------------
question = st.chat_input("Ask a question about your indexed documents...")

if question:
    st.session_state.messages.append(
        {"role": "user", "content": question}
    )

    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("Searching indexed documents..."):
            try:
                answer, citations, answer_source = answer_question(question)

                st.markdown(answer)

                if citations:
                    with st.expander("📚 View source citations"):
                        st.markdown(format_citations(citations))

                if answer_source == "uploaded_documents":
                    st.caption("Answer source: uploaded documents")
                else:
                    st.caption("Answer source: existing Phase 10 RAG index")

                history_content = answer

                if citations:
                    history_content += "\n\n**Sources:**\n"
                    history_content += format_citations(citations)

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": history_content,
                    }
                )

            except Exception as error:
                st.error(
                    "I couldn't process that question. "
                    "Check that the vector index and embedding model "
                    "are available, then try again."
                )
                st.exception(error)

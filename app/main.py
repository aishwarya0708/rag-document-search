import streamlit as st
from app.rag_engine import AeroAssistRAG
import os
from app.config import settings

st.set_page_config(page_title="AeroAssist", page_icon="✈️", layout="wide")

st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #0033a0;
    }
    .sub-header {
        font-size: 1rem;
        color: #666;
    }
    .source-box {
        background-color: #f8f9fa;
        border-left: 4px solid #0033a0;
        padding: 10px;
        margin: 5px 0;
        border-radius: 0 5px 5px 0;
        font-size: 0.85rem;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-header">✈️ AeroAssist</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">AI-Powered Manufacturing Operations Assistant</p>', unsafe_allow_html=True)
st.divider()

if "rag_engine" not in st.session_state:
    st.session_state.rag_engine = AeroAssistRAG()

with st.sidebar:
    st.header("📁 Document Management")
    doc_count = st.session_state.rag_engine.get_document_count()
    st.metric("Documents Loaded", doc_count)
    
    uploaded_files = st.file_uploader(
        "Upload PDFs or TXT files",
        type=["pdf", "txt"],
        accept_multiple_files=True
    )
    
    if uploaded_files:
        if st.button("Process Documents", use_container_width=True):
            os.makedirs(settings.DOCUMENTS_DIR, exist_ok=True)
            for file in uploaded_files:
                filepath = os.path.join(settings.DOCUMENTS_DIR, file.name)
                with open(filepath, "wb") as f:
                    f.write(file.getbuffer())
            with st.spinner("Processing..."):
                chunks = st.session_state.rag_engine.ingest_documents()
                st.success(f"Processed {chunks} chunks!")
                st.rerun()

st.subheader("Ask a Question")
question = st.text_input("What would you like to know?", placeholder="e.g., What is the torque specification for wing bolt assembly?")

if st.button("Get Answer", type="primary") and question:
    with st.spinner("Searching..."):
        answer, sources = st.session_state.rag_engine.query(question)
    
    st.subheader("Answer")
    st.write(answer)
    
    if sources:
        st.subheader("Sources")
        for i, doc in enumerate(sources, 1):
            source_name = os.path.basename(doc.metadata.get("source", "Unknown"))
            st.markdown(f'<div class="source-box"><b>Source {i}:</b> {source_name}<br>{doc.page_content[:200]}...</div>', unsafe_allow_html=True)
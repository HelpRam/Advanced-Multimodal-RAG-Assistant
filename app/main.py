import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
from src.core.rag_pipeline import RAGPipeline
from config.settings import settings


st.set_page_config(layout="wide", page_title="Multimodal Research Assistant")

# Initialize RAG Pipeline (once per session)
@st.cache_resource
def get_rag_pipeline():
    pipeline = RAGPipeline()
    return pipeline

rag_pipeline = get_rag_pipeline()

# Streamlit UI
st.title("📚 Intelligent Research Assistant with Multimodal RAG")

# Sidebar for actions
st.sidebar.header("Actions")
uploaded_files = st.sidebar.file_uploader(
    "Upload Documents (PDF, DOCX, TXT, Images)",
    type=["pdf", "docx", "txt", "png", "jpg", "jpeg", "gif"],
    accept_multiple_files=True
)

if uploaded_files:
    if st.sidebar.button("Index Uploaded Documents"):
        with st.spinner("Processing and indexing documents... This may take a while for images."):
            # Save uploaded files to the data/raw directory
            for uploaded_file in uploaded_files:
                file_path = os.path.join(settings.DATA_DIR, uploaded_file.name)
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                st.sidebar.success(f"Saved: {uploaded_file.name}")
            
            rag_pipeline.index_documents(settings.DATA_DIR)
            st.sidebar.success("Documents indexed successfully!")

if st.sidebar.button("Reset Knowledge Base"):
    if os.path.exists(settings.VECTOR_DB_PATH):
        import shutil
        shutil.rmtree(settings.VECTOR_DB_PATH)
        st.sidebar.info("Old vector database removed.")
    rag_pipeline.reset()
    st.sidebar.success("Knowledge base reset!")


st.sidebar.markdown("---")
st.sidebar.info("Upload documents to the 'data/raw' folder and click 'Index Uploaded Documents'. Then, ask your questions in the main chat.")


# Main chat interface
st.header("Ask your questions!")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What do you want to know?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Searching and generating answer..."):
            response = rag_pipeline.query(prompt)
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
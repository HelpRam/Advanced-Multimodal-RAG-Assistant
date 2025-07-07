from typing import List, Dict, Any
from langchain.text_splitter import RecursiveCharacterTextSplitter
from config.settings import settings

def chunk_text(text_content: str, metadata: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Splits long text content into smaller, overlapping chunks.
    Each chunk gets associated metadata.
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.CHUNK_SIZE,
        chunk_overlap=settings.CHUNK_OVERLAP,
        length_function=len,
        is_separator_regex=False,
    )
    chunks = text_splitter.create_documents([text_content])
    chunked_data = []
    for i, chunk in enumerate(chunks):
        chunk_metadata = {**metadata, "chunk_id": f"{metadata['file_name']}_chunk_{i}"}
        chunked_data.append({"content": chunk.page_content, "type": "text_chunk", "metadata": chunk_metadata})
    return chunked_data
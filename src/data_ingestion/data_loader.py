import os
from typing import List, Dict, Any
from pypdf import PdfReader
from docx import Document as DocxDocument
from PIL import Image

def load_text_from_pdf(file_path: str) -> str:
    """Loads text from a PDF file."""
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

def load_text_from_docx(file_path: str) -> str:
    """Loads text from a DOCX file."""
    doc = DocxDocument(file_path)
    text = []
    for paragraph in doc.paragraphs:
        text.append(paragraph.text)
    return "\n".join(text)

def load_text_from_txt(file_path: str) -> str:
    """Loads text from a plain text file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def load_image(file_path: str) -> Image.Image:
    """Loads an image file."""
    return Image.open(file_path).convert("RGB")

def load_documents(directory: str) -> List[Dict[str, Any]]:
    """
    Loads all supported documents (PDF, DOCX, TXT, images) from a directory.
    Returns a list of dictionaries with 'content', 'type', and 'metadata'.
    """
    documents = []
    for root, _, files in os.walk(directory):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            file_extension = os.path.splitext(file_name)[1].lower()
            metadata = {"source": file_path, "file_name": file_name}

            try:
                if file_extension == ".pdf":
                    text_content = load_text_from_pdf(file_path)
                    documents.append({"content": text_content, "type": "text", "metadata": metadata})
                elif file_extension == ".docx":
                    text_content = load_text_from_docx(file_path)
                    documents.append({"content": text_content, "type": "text", "metadata": metadata})
                elif file_extension == ".txt":
                    text_content = load_text_from_txt(file_path)
                    documents.append({"content": text_content, "type": "text", "metadata": metadata})
                elif file_extension in [".png", ".jpg", ".jpeg", ".gif"]:
                    # For now, we just store the image path. Multimodal processing will happen later.
                    documents.append({"content": file_path, "type": "image", "metadata": metadata})
                else:
                    print(f"Skipping unsupported file: {file_path}")
            except Exception as e:
                print(f"Error loading {file_path}: {e}")
    return documents
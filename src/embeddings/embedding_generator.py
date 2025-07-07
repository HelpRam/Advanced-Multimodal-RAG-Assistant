from typing import List, Dict, Any
import google.generativeai as genai
from config.settings import settings

# Configure Gemini API
genai.configure(api_key=settings.GEMINI_API_KEY)

def get_gemini_embedding(text: str) -> List[float]:
    """Generates an embedding for a given text using Gemini's embedding model."""
    try:
        model = settings.GEMINI_EMBEDDING_MODEL
        response = genai.embed_content(model=model, content=text)
        return response['embedding']
    except Exception as e:
        print(f"Error generating embedding: {e}")
        return []

def generate_embeddings_for_chunks(chunks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Generates embeddings for a list of text chunks.
    Adds 'embedding' key to each chunk dictionary.
    """
    for chunk in chunks:
        if chunk["type"] in ["text_chunk", "image_description"]:
            embedding = get_gemini_embedding(chunk["content"])
            if embedding:
                chunk["embedding"] = embedding
            else:
                print(f"Could not generate embedding for chunk: {chunk['metadata'].get('chunk_id', 'N/A')}")
        else:
            print(f"Skipping embedding for unsupported chunk type: {chunk['type']}")
    return chunks
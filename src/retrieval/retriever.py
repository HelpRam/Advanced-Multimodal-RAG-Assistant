from typing import List, Dict, Any
from src.vector_db.vector_store_manager import VectorStoreManager
from src.embeddings.embedding_generator import get_gemini_embedding
from config.settings import settings

class Retriever:
    def __init__(self, vector_store_manager: VectorStoreManager):
        self.vector_store_manager = vector_store_manager

    def retrieve_relevant_documents(self, query: str, top_k: int = settings.TOP_K_RETRIEVAL) -> List[Dict[str, Any]]:
        """
        Retrieves top_k most relevant document chunks based on a user query.
        """
        query_embedding = get_gemini_embedding(query)
        if not query_embedding:
            print("Failed to generate embedding for the query.")
            return []

        # Query the vector store
        retrieved_chunks = self.vector_store_manager.query_documents(
            query_embedding=query_embedding,
            top_k=top_k
        )
        return retrieved_chunks

  
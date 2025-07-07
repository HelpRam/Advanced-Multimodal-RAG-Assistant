import chromadb
from chromadb.utils import embedding_functions
from typing import List, Dict, Any
from config.settings import settings

class VectorStoreManager:
    def __init__(self, collection_name: str = "research_assistant_collection"):
        self.client = chromadb.PersistentClient(path=settings.VECTOR_DB_PATH)
        # Using Gemini embedding function directly. Ensure this aligns with your embedding model.
        # For 'models/embedding-001' it's usually `text-embedding-004` from the genai client.
        # Chromadb has a built-in GoogleGenerativeAiEmbeddingFunction, but let's integrate ours for control.
        self.embedding_function = self._get_gemini_embedding_function()
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            embedding_function=self.embedding_function # Pass the embedding function
        )
        print(f"ChromaDB initialized at: {settings.VECTOR_DB_PATH}")

    def _get_gemini_embedding_function(self):
        """Helper to get a custom embedding function for ChromaDB using Gemini."""
        class GeminiEmbeddingFunction(embedding_functions.EmbeddingFunction):
            def __call__(self, texts: embedding_functions.Documents) -> embedding_functions.Embeddings:
                embeddings = [
                    genai.embed_content(model=settings.GEMINI_EMBEDDING_MODEL, content=text)['embedding']
                    for text in texts
                ]
                return embeddings
        import google.generativeai as genai
        genai.configure(api_key=settings.GEMINI_API_KEY)
        return GeminiEmbeddingFunction()

    def add_documents(self, documents: List[Dict[str, Any]]):
        """Adds documents (chunks with embeddings) to the ChromaDB collection."""
        ids = []
        metadatas = []
        documents_to_add = [] # This will hold the actual text content for Chroma
        embeddings_to_add = []

        for doc in documents:
            if "embedding" in doc and doc["embedding"] and doc["content"]:
                ids.append(doc["metadata"]["chunk_id"])
                metadatas.append(doc["metadata"])
                documents_to_add.append(doc["content"])
                embeddings_to_add.append(doc["embedding"])
            else:
                print(f"Skipping document due to missing embedding or content: {doc['metadata'].get('chunk_id', 'N/A')}")

        if ids:
            # ChromaDB expects `documents` for the text content and `embeddings` for the vectors
            self.collection.add(
                embeddings=embeddings_to_add,
                documents=documents_to_add,
                metadatas=metadatas,
                ids=ids
            )
            print(f"Added {len(ids)} documents to ChromaDB.")
        else:
            print("No documents with embeddings to add.")

    def query_documents(self, query_embedding: List[float], top_k: int = settings.TOP_K_RETRIEVAL) -> List[Dict[str, Any]]:
        """Queries the ChromaDB collection with an embedding and returns top_k results."""
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            include=['documents', 'metadatas', 'distances'] # Include content, metadata, and distance
        )
        # Reformat results for easier consumption
        retrieved_docs = []
        if results and results['documents'] and results['metadatas']:
            for i in range(len(results['documents'][0])):
                retrieved_docs.append({
                    "content": results['documents'][0][i],
                    "metadata": results['metadatas'][0][i],
                    "distance": results['distances'][0][i]
                })
        return retrieved_docs

    def reset_collection(self):
        """Deletes and recreates the collection, effectively clearing it."""
        try:
            self.client.delete_collection(name=self.collection.name)
            self.collection = self.client.get_or_create_collection(
                name=self.collection.name,
                embedding_function=self.embedding_function
            )
            print(f"Collection '{self.collection.name}' reset.")
        except Exception as e:
            print(f"Error resetting collection: {e}")
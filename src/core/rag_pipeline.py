from src.data_ingestion.data_loader import load_documents
from src.data_ingestion.text_chunker import chunk_text
from src.data_ingestion.multimodal_parser import process_multimodal_documents, analyze_image_with_gemini
from src.embeddings.embedding_generator import generate_embeddings_for_chunks, get_gemini_embedding
from src.vector_db.vector_store_manager import VectorStoreManager
from src.retrieval.retriever import Retriever
from src.generation.generator import Generator
from config.settings import settings
import os
from typing import List, Dict, Any

class RAGPipeline:
    def __init__(self):
        self.vector_store_manager = VectorStoreManager()
        self.retriever = Retriever(self.vector_store_manager)
        self.generator = Generator()

    def index_documents(self, data_directory: str = settings.DATA_DIR):
        """
        Ingests, processes, embeds, and indexes documents into the vector store.
        """
        print(f"Starting document indexing from {data_directory}...")
        # 1. Load documents
        raw_documents = load_documents(data_directory)
        print(f"Loaded {len(raw_documents)} raw documents.")

        # 2. Process multimodal content (e.g., image descriptions)
        multimodal_processed_documents = process_multimodal_documents(raw_documents)
        print(f"Processed {len(multimodal_processed_documents)} documents for multimodal content.")

        all_chunks_to_embed = []
        for doc in multimodal_processed_documents:
            if doc["type"] == "text" or doc["type"] == "image_description":
                chunks = chunk_text(doc["content"], doc["metadata"])
                all_chunks_to_embed.extend(chunks)
            else:
                # If you have raw image paths, you might want to index them directly
                # For now, we only embed the generated descriptions.
                print(f"Skipping direct embedding for type: {doc['type']} (handled by description).")

        # 3. Generate embeddings for all text chunks and image descriptions
        documents_with_embeddings = generate_embeddings_for_chunks(all_chunks_to_embed)
        print(f"Generated embeddings for {len(documents_with_embeddings)} chunks/descriptions.")

        # 4. Add to vector store
        self.vector_store_manager.add_documents(documents_with_embeddings)
        print("Documents indexed successfully.")

    def query(self, user_query: str) -> str:
        """
        Executes the RAG pipeline for a given user query.
        """
        print(f"\nProcessing query: '{user_query}'")
        # 1. Retrieve relevant documents
        retrieved_docs = self.retriever.retrieve_relevant_documents(user_query)
        if not retrieved_docs:
            return "I couldn't find any relevant information for your query."

        print(f"Retrieved {len(retrieved_docs)} relevant documents/chunks.")

        # 2. Generate answer
        answer = self.generator.generate_answer(user_query, retrieved_docs)

        # 3. Add sources (optional, but good for research assistant)
        sources = "\nSources:\n"
        unique_sources = set()
        for doc in retrieved_docs:
            source_info = doc["metadata"].get("source", "Unknown Source")
            if source_info not in unique_sources:
                sources += f"- {source_info}\n"
                unique_sources.add(source_info)
            if doc["metadata"].get("original_type") == "image":
                 sources += f" (Image description from {doc['metadata'].get('file_name', 'N/A')})\n"


        return answer + sources

    def reset(self):
        """Resets the vector database."""
        self.vector_store_manager.reset_collection()
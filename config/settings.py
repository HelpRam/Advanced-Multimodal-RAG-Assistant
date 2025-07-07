import os
from dotenv import load_dotenv

load_dotenv() # Load environment variables from .env file

class Settings:
    # Gemini API settings
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY")
    # Set both text and vision models to 'gemini-2.5-flash'
    GEMINI_TEXT_MODEL: str = "gemini-2.5-flash" # For text generation and potentially text-based multimodal understanding
    GEMINI_VISION_MODEL: str = "gemini-2.5-flash" # For image analysis (gemini-2.5-flash supports vision)
    GEMINI_EMBEDDING_MODEL: str = "models/embedding-001" # This remains the dedicated embedding model

    # Data Ingestion settings
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200
    DATA_DIR: str = "data/raw"
    PROCESSED_DATA_DIR: str = "data/processed"

    # Vector Database settings
    VECTOR_DB_PATH: str = "vector_db/chroma_db" # Path for ChromaDB persistence

    # Retrieval settings
    TOP_K_RETRIEVAL: int = 5

    # Evaluation settings 
    RAGAS_EVAL_LLM: str = "gemini-2.5-flash" # Ragas can also use gemini-2.5-flash
    # Or 'gemini-1.5-pro' if you prefer a more capable model for evaluation which might be more robust for complex reasoning needed for Ragas metrics, though 2.5-flash should work.

settings = Settings()
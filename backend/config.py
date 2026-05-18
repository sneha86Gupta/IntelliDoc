"""
Application configuration using environment variables
"""

from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    """
    Central configuration class
    Loads values from .env file or system environment
    """

    # -----------------------------
    # App Info
    # -----------------------------
    APP_NAME: str = "RAG Learning Platform"
    VERSION: str = "1.0.0"

    # -----------------------------
    # API
    # -----------------------------
    API_PREFIX: str = "/api"

    # -----------------------------
    # CORS
    # -----------------------------
    ALLOWED_ORIGINS: List[str] = ["*"]

    # -----------------------------
    # Base Paths
    # -----------------------------
    BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATA_DIR: str = os.path.join(BASE_DIR, "..", "data")

    # -----------------------------
    # Storage Directories
    # -----------------------------
    UPLOAD_DIR: str = os.path.join(DATA_DIR, "uploads")
    PROCESSED_DIR: str = os.path.join(DATA_DIR, "processed")
    CHROMA_DB_DIR: str = os.path.join(DATA_DIR, "chroma_db")

    # -----------------------------
    # Embedding Model
    # -----------------------------
    EMBEDDING_MODEL_NAME: str = "all-MiniLM-L6-v2"

    # -----------------------------
    # Chunking
    # -----------------------------
    CHUNK_SIZE: int = 500
    CHUNK_OVERLAP: int = 50

    # -----------------------------
    # Clustering
    # -----------------------------
    NUM_CLUSTERS: int = 8

    # -----------------------------
    # Gemini API
    # -----------------------------
    GEMINI_API_KEY: str = ""

    # -----------------------------
    # Pydantic Config (v2)
    # -----------------------------
    model_config = {
        "env_file": ".env",
        "case_sensitive": True
    }


# Initialize settings instance
settings = Settings()


def ensure_directories():
    """
    Ensure required directories exist
    """
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    os.makedirs(settings.PROCESSED_DIR, exist_ok=True)
    os.makedirs(settings.CHROMA_DB_DIR, exist_ok=True)


# Create directories at import time
ensure_directories()
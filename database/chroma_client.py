"""
Chroma Client
Initializes and provides a reusable ChromaDB client instance
"""

import chromadb
from chromadb.config import Settings as ChromaSettings

from backend.config import settings


class ChromaClient:
    """
    Singleton-style ChromaDB client wrapper
    """

    _client = None

    @classmethod
    def get_client(cls):
        """
        Get or initialize ChromaDB client
        """
        if cls._client is None:
            cls._client = chromadb.Client(
                ChromaSettings(
                    persist_directory=settings.CHROMA_DB_DIR,
                    anonymized_telemetry=False
                )
            )
        return cls._client

    @classmethod
    def get_collection(cls, name: str):
        """
        Get or create a collection
        """
        client = cls.get_client()
        return client.get_or_create_collection(name=name)
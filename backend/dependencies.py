"""
Dependency injection utilities for FastAPI
Provides reusable services across endpoints
"""

from functools import lru_cache

from backend.config import settings

# Services
from backend.services.pdf_service import PDFService
from backend.services.heading_service import HeadingService
from backend.services.chunk_service import ChunkService
from backend.services.embedding_service import EmbeddingService
from backend.services.vector_service import VectorService
from backend.services.topic_service import TopicService
from backend.services.retrieval_service import RetrievalService
from backend.services.rag_service import RAGService
from backend.services.llm_service import LLMService


@lru_cache()
def get_settings():
    """
    Cached settings instance
    """
    return settings


@lru_cache()
def get_pdf_service() -> PDFService:
    """
    PDF processing service
    """
    return PDFService()


@lru_cache()
def get_heading_service() -> HeadingService:
    """
    Heading detection service
    """
    return HeadingService()


@lru_cache()
def get_chunk_service() -> ChunkService:
    """
    Text chunking service
    """
    return ChunkService(
        chunk_size=settings.CHUNK_SIZE,
        chunk_overlap=settings.CHUNK_OVERLAP,
    )


@lru_cache()
def get_embedding_service() -> EmbeddingService:
    """
    Embedding generation service
    """
    return EmbeddingService(model_name=settings.EMBEDDING_MODEL_NAME)


@lru_cache()
def get_vector_service() -> VectorService:
    """
    ChromaDB vector service
    """
    return VectorService(persist_directory=settings.CHROMA_DB_DIR)


@lru_cache()
def get_topic_service() -> TopicService:
    """
    Topic extraction service (heading + clustering)
    """
    return TopicService(num_clusters=settings.NUM_CLUSTERS)


@lru_cache()
def get_llm_service() -> LLMService:
    """
    Gemini LLM service
    """
    return LLMService(api_key=settings.GEMINI_API_KEY)


@lru_cache()
def get_retrieval_service() -> RetrievalService:
    """
    Retrieval service (vector search)
    """
    vector_service = get_vector_service()
    embedding_service = get_embedding_service()
    return RetrievalService(
        vector_service=vector_service,
        embedding_service=embedding_service,
    )


@lru_cache()
def get_rag_service() -> RAGService:
    """
    RAG pipeline service (retrieval + generation)
    """
    retrieval_service = get_retrieval_service()
    llm_service = get_llm_service()
    return RAGService(
        retrieval_service=retrieval_service,
        llm_service=llm_service,
    )
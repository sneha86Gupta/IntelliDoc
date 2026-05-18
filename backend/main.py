"""
Main entry point for FastAPI application
Initializes app, middleware, and includes all routers
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.api import upload, topics, questions, export
from backend.config import settings


def create_app() -> FastAPI:
    """
    Create and configure FastAPI application
    """
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.VERSION,
        description="AI-powered RAG-based Learning Platform",
    )

    # CORS configuration (allow frontend access)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include API routers
    app.include_router(upload.router, prefix="/upload", tags=["Upload"])
    app.include_router(topics.router, prefix="/topics", tags=["Topics"])
    app.include_router(questions.router, prefix="/questions", tags=["Questions"])
    app.include_router(export.router, prefix="/export", tags=["Export"])

    @app.get("/")
    async def root():
        """
        Health check endpoint
        """
        return {
            "message": "RAG Learning Platform API is running",
            "version": settings.VERSION
        }

    return app


# Create app instance
app = create_app()


# http://localhost:5500/index.html
"""
Upload API
Handles file upload and preprocessing pipeline:
Upload → Extract Text → Detect Headings → Chunk → Embedding → Clustering → Store
"""

import os
import uuid
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends

from backend.dependencies import (
    get_pdf_service,
    get_heading_service,
    get_chunk_service,
    get_embedding_service,
    get_vector_service,
    get_topic_service,
)
from backend.config import settings

router = APIRouter()


@router.post("/")
async def upload_file(
    file: UploadFile = File(...),
    pdf_service=Depends(get_pdf_service),
    heading_service=Depends(get_heading_service),
    chunk_service=Depends(get_chunk_service),
    embedding_service=Depends(get_embedding_service),
    vector_service=Depends(get_vector_service),
    topic_service=Depends(get_topic_service),
):
    """
    Upload and process a document
    """

    # Validate file type
    if not file.filename.endswith((".pdf", ".docx")):
        raise HTTPException(status_code=400, detail="Only PDF and DOCX files are supported")

    # Generate unique document ID
    doc_id = str(uuid.uuid4())

    file_path = os.path.join(settings.UPLOAD_DIR, f"{doc_id}_{file.filename}")

    # Save file
    with open(file_path, "wb") as f:
        f.write(await file.read())

    try:
        # 1. Extract text
        raw_text, metadata = pdf_service.extract_text(file_path)

        # 2. Detect headings
        headings = heading_service.detect_headings(raw_text, metadata)

        # 3. Chunk text with heading association
        chunks = chunk_service.create_chunks(raw_text, headings)

        # 4. Generate embeddings
        texts = [chunk["text"] for chunk in chunks]
        embeddings = embedding_service.generate_embeddings(texts)

        # 5. Topic extraction (heading + clustering)
        topics = topic_service.extract_topics(chunks, embeddings)

        # 6. Store in vector DB
        vector_service.store_embeddings(
            doc_id=doc_id,
            chunks=chunks,
            embeddings=embeddings,
            topics=topics,
        )

        return {
            "message": "File processed successfully",
            "doc_id": doc_id,
            "num_chunks": len(chunks),
            "num_topics": len(topics),
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
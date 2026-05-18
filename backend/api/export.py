"""
Export API
Handles exporting generated questions and answers to PDF
"""

from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import FileResponse

from backend.models.schemas import ExportRequest
from backend.dependencies import get_rag_service
from backend.exports.pdf_export import PDFExportService

import os
import uuid

router = APIRouter()


@router.post("/")
async def export_pdf(
    request: ExportRequest,
    rag_service=Depends(get_rag_service),
):
    """
    Export questions and answers to PDF

    Body:
        ExportRequest:
            - doc_id: str
            - topic: str
            - num_questions: int
            - question_types: list

    Returns:
        PDF file
    """
    try:
        # 1. Generate questions using RAG
        result = await rag_service.generate_questions(
            doc_id=request.doc_id,
            topic=request.topic,
            num_questions=request.num_questions,
            question_types=request.question_types,
        )

        questions = result["questions"]

        # 2. Generate PDF file
        export_service = PDFExportService()

        file_name = f"{uuid.uuid4()}.pdf"
        file_path = os.path.join("project/data/processed", file_name)

        export_service.generate_pdf(
            file_path=file_path,
            topic=request.topic,
            questions=questions,
        )

        # 3. Return file response
        return FileResponse(
            path=file_path,
            filename="questions.pdf",
            media_type="application/pdf"
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
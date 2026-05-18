"""
Questions API
Handles question generation using RAG pipeline
"""

from fastapi import APIRouter, HTTPException, Depends

from backend.dependencies import get_rag_service
from backend.models.schemas import QuestionRequest
from backend.models.response_models import QuestionResponse

router = APIRouter()


@router.post("/", response_model=QuestionResponse)
async def generate_questions(
    request: QuestionRequest,
    rag_service=Depends(get_rag_service),
):
    """
    Generate questions based on selected topic using RAG

    Body:
        QuestionRequest:
            - doc_id: str
            - topic: str
            - num_questions: int
            - question_types: list (mcq, short, long)

    Returns:
        QuestionResponse
    """
    try:
        result = await rag_service.generate_questions(
            doc_id=request.doc_id,
            topic=request.topic,
            num_questions=request.num_questions,
            question_types=request.question_types,
        )

        return QuestionResponse(
            doc_id=request.doc_id,
            topic=request.topic,
            questions=result["questions"],
            total_questions=len(result["questions"]),
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
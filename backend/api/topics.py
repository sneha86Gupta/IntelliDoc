"""
Topics API
Returns extracted topics for a given document
"""

from fastapi import APIRouter, HTTPException, Depends

from backend.dependencies import get_vector_service
from backend.models.response_models import TopicsResponse

router = APIRouter()


@router.get("/{doc_id}", response_model=TopicsResponse)
async def get_topics(
    doc_id: str,
    vector_service=Depends(get_vector_service),
):
    """
    Get topics for a processed document

    Args:
        doc_id (str): Document ID

    Returns:
        TopicsResponse: List of topics
    """
    try:
        # Fetch topics from vector DB metadata
        topics = vector_service.get_topics(doc_id)

        if not topics:
            raise HTTPException(status_code=404, detail="No topics found for this document")

        return TopicsResponse(
            doc_id=doc_id,
            topics=topics,
            total_topics=len(topics),
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
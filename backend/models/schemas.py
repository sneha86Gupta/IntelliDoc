"""
Request Schemas
Defines input data models for API endpoints
"""

from typing import List
from pydantic import BaseModel, Field


class QuestionRequest(BaseModel):
    """
    Request schema for generating questions
    """
    doc_id: str = Field(..., description="Document ID")
    topic: str = Field(..., description="Selected topic")
    num_questions: int = Field(
        default=5,
        ge=1,
        le=50,
        description="Number of questions to generate"
    )
    question_types: List[str] = Field(
        default=["mcq", "short"],
        description="Types of questions (mcq, short, long)"
    )


class ExportRequest(BaseModel):
    """
    Request schema for exporting questions to PDF
    """
    doc_id: str = Field(..., description="Document ID")
    topic: str = Field(..., description="Selected topic")
    num_questions: int = Field(
        default=5,
        ge=1,
        le=50,
        description="Number of questions"
    )
    question_types: List[str] = Field(
        default=["mcq", "short"],
        description="Types of questions (mcq, short, long)"
    )
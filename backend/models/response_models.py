"""
Response Models
Defines structured API responses
"""

from typing import List, Optional
from pydantic import BaseModel, Field


class TopicItem(BaseModel):
    """
    Single topic item
    """
    name: str = Field(..., description="Topic name")


class TopicsResponse(BaseModel):
    """
    Response model for topics endpoint
    """
    doc_id: str = Field(..., description="Document ID")
    topics: List[str] = Field(..., description="List of topic names")
    total_topics: int = Field(..., description="Total number of topics")


class QuestionItem(BaseModel):
    """
    Single question structure
    """
    type: str = Field(..., description="Question type (mcq, short, long)")
    question: str = Field(..., description="Question text")
    options: Optional[List[str]] = Field(default=[], description="Options for MCQ")
    answer: str = Field(..., description="Correct answer")
    explanation: str = Field(..., description="Explanation of the answer")


class QuestionResponse(BaseModel):
    """
    Response model for question generation
    """
    doc_id: str = Field(..., description="Document ID")
    topic: str = Field(..., description="Topic used for generation")
    questions: List[QuestionItem] = Field(..., description="Generated questions")
    total_questions: int = Field(..., description="Total number of questions")
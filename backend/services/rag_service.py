"""
RAG Service
Combines retrieval + LLM generation
"""

from typing import List, Dict


class RAGService:
    """
    Service for running full RAG pipeline:
    Retrieve → Build Context → Generate via LLM
    """

    def __init__(self, retrieval_service, llm_service):
        """
        Args:
            retrieval_service: RetrievalService instance
            llm_service: LLMService instance
        """
        self.retrieval_service = retrieval_service
        self.llm_service = llm_service

    async def generate_questions(
        self,
        doc_id: str,
        topic: str,
        num_questions: int,
        question_types: List[str],
    ) -> Dict:
        """
        Generate questions using RAG pipeline

        Args:
            doc_id (str): Document ID
            topic (str): Selected topic
            num_questions (int): Number of questions
            question_types (List[str]): Types of questions (mcq, short, long)

        Returns:
            Dict with generated questions
        """

        # Step 1: Retrieve relevant chunks
        retrieved_chunks = self.retrieval_service.retrieve(
            doc_id=doc_id,
            query=topic,
            top_k=10,
            topic=topic,
        )

        if not retrieved_chunks:
            return {"questions": []}

        # Step 2: Build context
        context = self._build_context(retrieved_chunks)

        # Step 3: Generate questions using LLM
        questions = await self.llm_service.generate_questions(
            context=context,
            topic=topic,
            num_questions=num_questions,
            question_types=question_types,
        )

        return {"questions": questions}

    def _build_context(self, chunks: List[Dict]) -> str:
        """
        Combine retrieved chunks into a single context string
        """
        context_parts = []

        for chunk in chunks:
            text = chunk.get("text")
            if text:
                context_parts.append(text.strip())

        # Limit context size (basic safeguard)
        context = "\n\n".join(context_parts)

        # Optional truncation (to avoid overly long prompts)
        max_chars = 5000
        return context[:max_chars]
"""
Retrieval Service
Handles semantic retrieval of relevant chunks from vector DB
"""

from typing import List, Dict, Optional


class RetrievalService:
    """
    Service responsible for retrieving relevant chunks using embeddings + vector search
    """

    def __init__(self, vector_service, embedding_service):
        """
        Args:
            vector_service: VectorService instance
            embedding_service: EmbeddingService instance
        """
        self.vector_service = vector_service
        self.embedding_service = embedding_service

    def retrieve(
        self,
        doc_id: str,
        query: str,
        top_k: int = 5,
        topic: Optional[str] = None,
    ) -> List[Dict]:
        """
        Retrieve relevant chunks for a query

        Args:
            doc_id (str): Document ID
            query (str): User query or topic
            top_k (int): Number of chunks to retrieve
            topic (str, optional): Filter by topic

        Returns:
            List[Dict]: Retrieved chunks with metadata
        """

        if not query:
            return []

        # Step 1: Generate query embedding
        query_embedding = self.embedding_service.generate_embeddings([query])[0]

        # Step 2: Query vector DB
        results = self.vector_service.query(
            doc_id=doc_id,
            query_embedding=query_embedding,
            n_results=top_k,
            topic=topic,
        )

        # Step 3: Post-process results
        processed_results = self._post_process(results)

        return processed_results

    def _post_process(self, results: List[Dict]) -> List[Dict]:
        """
        Clean and structure retrieved results
        """
        cleaned = []

        for item in results:
            cleaned.append({
                "text": item.get("text"),
                "heading": item.get("metadata", {}).get("heading"),
                "topic": item.get("metadata", {}).get("topic"),
                "score": self._convert_distance_to_score(item.get("distance")),
            })

        return cleaned

    def _convert_distance_to_score(self, distance: Optional[float]) -> Optional[float]:
        """
        Convert vector distance to similarity score
        Lower distance → higher score
        """
        if distance is None:
            return None

        # Simple inverse scaling
        return 1 / (1 + distance)
"""
Vector Service
Handles storage and retrieval using ChromaDB
"""

from typing import List, Dict, Any
import uuid

import chromadb
from chromadb.config import Settings as ChromaSettings


class VectorService:
    """
    Service for interacting with ChromaDB
    """

    def __init__(self, persist_directory: str):
        """
        Initialize ChromaDB client
        """
        self.client = chromadb.Client(
            ChromaSettings(
                persist_directory=persist_directory,
                anonymized_telemetry=False
            )
        )

    def _get_collection(self, doc_id: str):
        """
        Get or create a collection for a document
        """
        return self.client.get_or_create_collection(name=doc_id)

    def store_embeddings(
        self,
        doc_id: str,
        chunks: List[Dict],
        embeddings: List[List[float]],
        topics: List[Dict],
    ) -> None:
        """
        Store embeddings along with metadata in ChromaDB
        """

        collection = self._get_collection(doc_id)

        ids = []
        documents = []
        metadatas = []

        for i, chunk in enumerate(chunks):
            chunk_id = str(uuid.uuid4())

            ids.append(chunk_id)
            documents.append(chunk["text"])

            # Attach topic to each chunk (based on heading or clustering)
            topic = self._map_topic(chunk, topics)

            metadatas.append({
                "doc_id": doc_id,
                "heading": chunk.get("heading"),
                "topic": topic,
                "start_index": chunk.get("start_index"),
            })

        collection.add(
            ids=ids,
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas,
        )

    def _map_topic(self, chunk: Dict, topics: List[Dict]) -> str:
        """
        Map chunk to a topic using heading match or fallback
        """
        chunk_heading = chunk.get("heading")

        for topic in topics:
            if topic.get("heading") == chunk_heading:
                return topic.get("topic")

        return "General"

    def query(
        self,
        doc_id: str,
        query_embedding: List[float],
        n_results: int = 5,
        topic: str = None,
    ) -> List[Dict]:
        """
        Query similar chunks from ChromaDB
        """

        collection = self._get_collection(doc_id)

        where_filter = {"topic": topic} if topic else None

        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            where=where_filter,
        )

        output = []

        for i in range(len(results["documents"][0])):
            output.append({
                "text": results["documents"][0][i],
                "metadata": results["metadatas"][0][i],
                "distance": results["distances"][0][i] if "distances" in results else None,
            })

        return output

    def get_topics(self, doc_id: str) -> List[str]:
        """
        Retrieve unique topics for a document
        """

        collection = self._get_collection(doc_id)

        # Fetch all metadata
        data = collection.get(include=["metadatas"])

        topics = set()

        for meta in data.get("metadatas", []):
            topic = meta.get("topic")
            if topic:
                topics.add(topic)

        return list(topics)
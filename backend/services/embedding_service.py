"""
Embedding Service
Generates embeddings using sentence-transformers (all-MiniLM-L6-v2)
"""

from typing import List
from sentence_transformers import SentenceTransformer


class EmbeddingService:
    """
    Service for generating text embeddings
    """

    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """
        Initialize embedding model

        Args:
            model_name (str): HuggingFace model name
        """
        self.model_name = model_name
        self.model = SentenceTransformer(self.model_name)

    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for a list of texts

        Args:
            texts (List[str]): Input texts

        Returns:
            List[List[float]]: Embedding vectors
        """

        if not texts:
            return []

        # Generate embeddings
        embeddings = self.model.encode(
            texts,
            convert_to_numpy=True,
            show_progress_bar=False
        )

        # Convert numpy array to list for JSON compatibility
        return embeddings.tolist()
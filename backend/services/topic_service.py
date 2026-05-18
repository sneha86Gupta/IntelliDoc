"""
Topic Service
Extracts topics using heading grouping + clustering (NO LLM)
"""

from typing import List, Dict
from collections import defaultdict

import numpy as np
from sklearn.cluster import KMeans


class TopicService:
    """
    Service for extracting topics from chunks using:
    1. Heading grouping
    2. Embedding clustering
    """

    def __init__(self, num_clusters: int = 8):
        self.num_clusters = num_clusters

    def extract_topics(
        self,
        chunks: List[Dict],
        embeddings: List[List[float]],
    ) -> List[Dict]:
        """
        Extract topics from chunks using hybrid approach

        Args:
            chunks (List[Dict]): chunked text with heading info
            embeddings (List[List[float]]): embeddings of chunks

        Returns:
            List[Dict]: topics with mapping
        """

        if not chunks or not embeddings:
            return []

        # Step 1: Group by headings
        heading_groups = self._group_by_heading(chunks)

        # Step 2: Run clustering on embeddings
        cluster_labels = self._cluster_embeddings(embeddings)

        # Step 3: Combine heading + cluster to form topics
        topics = self._build_topics(chunks, heading_groups, cluster_labels)

        return topics

    def _group_by_heading(self, chunks: List[Dict]) -> Dict[str, List[int]]:
        """
        Group chunk indices by heading
        """
        groups = defaultdict(list)

        for idx, chunk in enumerate(chunks):
            heading = chunk.get("heading", "General")
            groups[heading].append(idx)

        return groups

    def _cluster_embeddings(self, embeddings: List[List[float]]) -> List[int]:
        """
        Perform KMeans clustering on embeddings
        """
        X = np.array(embeddings)

        # Handle small dataset edge case
        n_clusters = min(self.num_clusters, len(X))
        if n_clusters <= 1:
            return [0] * len(X)

        kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        labels = kmeans.fit_predict(X)

        return labels.tolist()

    def _build_topics(
        self,
        chunks: List[Dict],
        heading_groups: Dict[str, List[int]],
        cluster_labels: List[int],
    ) -> List[Dict]:
        """
        Combine heading + cluster labels into final topics
        """
        topic_map = {}

        for heading, indices in heading_groups.items():
            # Collect cluster distribution within this heading
            cluster_count = defaultdict(int)

            for idx in indices:
                cluster_id = cluster_labels[idx]
                cluster_count[cluster_id] += 1

            # Pick dominant cluster for this heading
            dominant_cluster = max(cluster_count, key=cluster_count.get)

            topic_name = f"{heading} (Cluster {dominant_cluster})"

            topic_map[heading] = {
                "heading": heading,
                "topic": topic_name,
                "cluster": dominant_cluster,
                "num_chunks": len(indices),
            }

        return list(topic_map.values())
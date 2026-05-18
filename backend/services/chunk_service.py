"""
Chunk Service
Splits text into chunks and assigns nearest heading context
Uses LangChain text splitter
"""

from typing import List, Dict, Optional
from langchain_text_splitters import RecursiveCharacterTextSplitter


class ChunkService:
    """
    Service for chunking text and attaching heading metadata
    """

    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 50):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            separators=["\n\n", "\n", ".", " ", ""],
        )

    def create_chunks(self, full_text: str, headings: List[Dict]) -> List[Dict]:
        """
        Split text into chunks and assign headings

        Args:
            full_text (str): Entire document text
            headings (List[Dict]): Detected headings with indices

        Returns:
            List[Dict]: Chunk objects with text + heading
        """

        # Split full text into chunks
        raw_chunks = self.splitter.split_text(full_text)

        # Map heading indices to text positions
        heading_map = self._build_heading_map(full_text, headings)

        chunks = []
        cursor = 0  # Track approximate position in text

        for chunk_text in raw_chunks:
            # Estimate position of chunk in full_text
            start_index = full_text.find(chunk_text, cursor)
            if start_index == -1:
                start_index = cursor

            # Get nearest heading for this position
            heading = self._get_nearest_heading(start_index, heading_map)

            chunks.append({
                "text": chunk_text,
                "heading": heading.get("text") if heading else "General",
                "heading_index": heading.get("index") if heading else None,
                "start_index": start_index,
            })

            cursor = start_index + len(chunk_text)

        return chunks

    def _build_heading_map(self, full_text: str, headings: List[Dict]) -> List[Dict]:
        """
        Build heading positions mapped to character index
        """
        heading_map = []

        for heading in headings:
            text = heading["text"]

            # Find position of heading in text
            index = full_text.find(text)
            if index == -1:
                continue

            heading_map.append({
                "text": text,
                "index": index,
                "meta_index": heading.get("index"),
            })

        # Sort by position
        heading_map.sort(key=lambda x: x["index"])

        return heading_map

    def _get_nearest_heading(self, position: int, heading_map: List[Dict]) -> Optional[Dict]:
        """
        Find nearest previous heading for a given position
        """
        nearest = None

        for heading in heading_map:
            if heading["index"] <= position:
                nearest = heading
            else:
                break

        return nearest
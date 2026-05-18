"""
Heading Service
Detects headings using font size heuristics and text rules (NO LLM)
"""

from typing import List, Dict
import statistics


class HeadingService:
    """
    Service for detecting headings based on font size and rules
    """

    def detect_headings(self, full_text: str, metadata: List[Dict]) -> List[Dict]:
        """
        Detect headings from extracted metadata

        Args:
            full_text (str): Entire document text
            metadata (List[Dict]): Line-wise metadata with font sizes

        Returns:
            List[Dict]: Detected headings with position info
        """

        if not metadata:
            return []

        # Collect font sizes
        font_sizes = [item["font_size"] for item in metadata if item.get("font_size")]

        if not font_sizes:
            return []

        # Determine threshold dynamically (large fonts are likely headings)
        avg_size = statistics.mean(font_sizes)
        std_dev = statistics.pstdev(font_sizes)

        # Heading threshold
        threshold = avg_size + std_dev * 0.5

        headings = []

        for idx, item in enumerate(metadata):
            text = item.get("text", "").strip()
            font_size = item.get("font_size", 0)

            if not text:
                continue

            # Rule 1: Large font
            is_large_font = font_size >= threshold

            # Rule 2: Short text (headings usually short)
            is_short = len(text.split()) <= 12

            # Rule 3: Formatting cues
            is_upper = text.isupper()
            is_title_case = text.istitle()

            # Rule 4: Avoid sentence-like text
            ends_like_sentence = text.endswith(".") or text.endswith(":")

            # Final decision
            if (
                is_large_font
                and is_short
                and (is_upper or is_title_case)
                and not ends_like_sentence
            ):
                headings.append({
                    "text": text,
                    "index": idx,
                    "font_size": font_size,
                    "page": item.get("page"),
                })

        return headings
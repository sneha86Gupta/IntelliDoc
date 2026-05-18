"""
PDF Service
Handles extraction of text and metadata from PDF/DOCX files
Uses PyMuPDF for PDFs
"""

import fitz  # PyMuPDF
from typing import Tuple, List, Dict


class PDFService:
    """
    Service for extracting structured text from documents
    """

    def extract_text(self, file_path: str) -> Tuple[str, List[Dict]]:
        """
        Extract text and metadata from a document

        Args:
            file_path (str): Path to the file

        Returns:
            Tuple:
                - full_text (str)
                - metadata (List[Dict]) → includes font size, flags, block info
        """
        if file_path.lower().endswith(".pdf"):
            return self._extract_from_pdf(file_path)
        elif file_path.lower().endswith(".docx"):
            return self._extract_from_docx(file_path)
        else:
            raise ValueError("Unsupported file format")

    def _extract_from_pdf(self, file_path: str) -> Tuple[str, List[Dict]]:
        """
        Extract text and metadata from PDF using PyMuPDF
        """
        doc = fitz.open(file_path)

        full_text = []
        metadata = []

        for page_num, page in enumerate(doc):
            blocks = page.get_text("dict")["blocks"]

            for block in blocks:
                if "lines" not in block:
                    continue

                for line in block["lines"]:
                    line_text = ""
                    max_font_size = 0

                    for span in line["spans"]:
                        text = span["text"].strip()
                        if not text:
                            continue

                        line_text += text + " "
                        max_font_size = max(max_font_size, span["size"])

                    cleaned_line = line_text.strip()

                    if cleaned_line:
                        full_text.append(cleaned_line)

                        metadata.append({
                            "text": cleaned_line,
                            "font_size": max_font_size,
                            "page": page_num + 1,
                        })

        doc.close()

        return "\n".join(full_text), metadata

    def _extract_from_docx(self, file_path: str) -> Tuple[str, List[Dict]]:
        """
        Extract text from DOCX (basic fallback, no font metadata)
        """
        try:
            from docx import Document
        except ImportError:
            raise ImportError("python-docx is required for DOCX support")

        doc = Document(file_path)

        full_text = []
        metadata = []

        for i, para in enumerate(doc.paragraphs):
            text = para.text.strip()
            if not text:
                continue

            full_text.append(text)

            metadata.append({
                "text": text,
                "font_size": 12,  # default fallback
                "page": None,
                "paragraph_index": i,
            })

        return "\n".join(full_text), metadata
"""
PDF Export Service
Generates PDF files for questions and answers using ReportLab
"""

from typing import List, Dict
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, ListFlowable
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4


class PDFExportService:
    """
    Service for exporting questions into a structured PDF
    """

    def __init__(self):
        self.styles = getSampleStyleSheet()

    def generate_pdf(
        self,
        file_path: str,
        topic: str,
        questions: List[Dict],
    ) -> None:
        """
        Generate a PDF file

        Args:
            file_path (str): Output file path
            topic (str): Topic name
            questions (List[Dict]): Questions data
        """

        doc = SimpleDocTemplate(file_path, pagesize=A4)

        elements = []

        # Title
        elements.append(Paragraph(f"<b>Topic:</b> {topic}", self.styles["Title"]))
        elements.append(Spacer(1, 12))

        for idx, q in enumerate(questions, start=1):
            # Question
            elements.append(
                Paragraph(f"<b>Q{idx}. ({q.get('type').upper()})</b> {q.get('question')}", self.styles["Heading3"])
            )
            elements.append(Spacer(1, 8))

            # Options (if MCQ)
            if q.get("type") == "mcq" and q.get("options"):
                option_list = []
                for opt in q["options"]:
                    option_list.append(Paragraph(opt, self.styles["Normal"]))

                elements.append(ListFlowable(option_list, bulletType="bullet"))
                elements.append(Spacer(1, 8))

            # Answer
            elements.append(
                Paragraph(f"<b>Answer:</b> {q.get('answer')}", self.styles["Normal"])
            )
            elements.append(Spacer(1, 6))

            # Explanation
            elements.append(
                Paragraph(f"<b>Explanation:</b> {q.get('explanation')}", self.styles["Normal"])
            )
            elements.append(Spacer(1, 16))

        # Build PDF
        doc.build(elements)
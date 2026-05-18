"""
LLM Service
Handles Gemini API calls for question generation
"""

from typing import List, Dict
import google.generativeai as genai

from backend.constants.prompts import QUESTION_GENERATION_PROMPT


class LLMService:
    """
    Service for interacting with Gemini API
    """

    def __init__(self, api_key: str):
        """
        Initialize Gemini client
        """
        if not api_key:
            raise ValueError("GEMINI_API_KEY is not set")

        genai.configure(api_key=api_key)

        # Use fast + cost-efficient model
        self.model = genai.GenerativeModel("gemini-2.5-flash")

    async def generate_questions(
        self,
        context: str,
        topic: str,
        num_questions: int,
        question_types: List[str],
    ) -> List[Dict]:
        """
        Generate questions using Gemini

        Args:
            context (str): Retrieved context
            topic (str): Topic name
            num_questions (int): Number of questions
            question_types (List[str]): Types (mcq, short, long)

        Returns:
            List[Dict]: Structured questions
        """

        prompt = QUESTION_GENERATION_PROMPT.format(
            context=context,
            topic=topic,
            num_questions=num_questions,
            question_types=", ".join(question_types),
        )

        try:
            response = await self.model.generate_content_async(prompt)

            raw_text = response.text

            # Convert to structured JSON
            parsed = self._parse_response(raw_text)

            return parsed

        except Exception as e:
            raise RuntimeError(f"LLM generation failed: {str(e)}")

    def _parse_response(self, text: str) -> List[Dict]:
        """
        Parse LLM response into structured format

        Expected format (strict JSON preferred):
        [
          {
            "type": "mcq",
            "question": "...",
            "options": ["A", "B", "C", "D"],
            "answer": "...",
            "explanation": "..."
          }
        ]
        """

        import json

        try:
            # Try direct JSON parse
            return json.loads(text)
        except Exception:
            # Fallback: attempt to extract JSON block
            try:
                start = text.find("[")
                end = text.rfind("]") + 1
                json_str = text[start:end]
                return json.loads(json_str)
            except Exception:
                # Final fallback: return raw
                return [{
                    "type": "unknown",
                    "question": text,
                    "options": [],
                    "answer": "",
                    "explanation": ""
                }]
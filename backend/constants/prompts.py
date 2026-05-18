"""
Prompts
Contains all prompt templates used for LLM generation
"""

QUESTION_GENERATION_PROMPT = """
You are an expert educator.

Using the context below, generate {num_questions} questions on the topic: "{topic}".

Context:
---------
{context}
---------

Requirements:
- Question types: {question_types}
- Maintain conceptual clarity and correctness
- Avoid repetition
- Questions should vary in difficulty

Output format (STRICT JSON ONLY):
[
  {{
    "type": "mcq",
    "question": "Question text",
    "options": ["A", "B", "C", "D"],
    "answer": "Correct option",
    "explanation": "Explanation"
  }},
  {{
    "type": "short",
    "question": "Question text",
    "options": [],
    "answer": "Answer",
    "explanation": "Explanation"
  }},
  {{
    "type": "long",
    "question": "Question text",
    "options": [],
    "answer": "Detailed answer",
    "explanation": "Explanation"
  }}
]

IMPORTANT:
- Output MUST be valid JSON
- Do not include any extra text outside JSON
"""
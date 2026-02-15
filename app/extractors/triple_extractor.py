import requests
import json

OLLAMA_URL = "http://localhost:11434/api/generate"

MODEL = "qwen2.5:3b-instruct-q4_K_M"


def extract_triples(text: str):

    prompt = f"""
You are an elite information extraction system.

Extract ONLY high-value strategic knowledge.

IGNORE:
- founding year
- revenue
- headquarters
- slogans
- generic descriptions
- employee counts

FOCUS ON:
- strategy
- AI initiatives
- partnerships
- acquisitions
- competition
- capabilities
- platforms
- transformation efforts

Return STRICT JSON.

Format example (values are dynamic, do NOT copy):

[
 {{
   "subject": "<real entity from text>",
   "predicate": "<RELATIONSHIP_IN_UPPERCASE>",
   "object": "<real entity from text>",
   "confidence": 0.0-1.0
 }}
]

RULES:
- Subject and object MUST be real named entities from the text
- NEVER output generic terms like "company", "entity", "organization"
- Predicate MUST be uppercase with underscores
- Avoid vague objects like "innovation" or "growth"
- No duplicate triples
- No explanations

Prefer these predicates when possible:
PARTNERS_WITH, ACQUIRES, COMPETES_WITH, INVESTS_IN,
USES_TECH, BUILDS_PLATFORM, FOCUSES_ON, OFFERS,
EXPANDS_TO, LEADS_IN

Only include triples with confidence >= 0.6.

TEXT:
{text}
"""


    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0,
                "top_p": 0.9
            }
        }
    )

    output = response.json()["response"]

    try:
        triples = json.loads(output)
        return triples
    except:
        return []

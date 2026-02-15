import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "qwen2.5:3b-instruct-q4_K_M"


def fallback_summary(query: str):

    prompt = f"""
You are a senior strategy consultant.

Provide a sharp executive summary.

Focus on:
- competitive positioning
- AI strategy
- partnerships
- strengths
- market direction

Be concise but insightful.

QUERY:
{query}
"""

    try:

        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.2
                }
            },
            timeout=120
        )

        data = response.json().get("response", "")

        if not data:
            return "No insight could be generated."

        return data

    except Exception as e:

        print("Fallback LLM error:", e)

        return "Strategic insight unavailable at the moment."

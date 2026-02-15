import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "qwen2.5:3b-instruct-q4_K_M"


def generate_answer(query, context):

    prompt = f"""
You are a senior enterprise strategy analyst.

Use ONLY the knowledge graph relationships below.

Do NOT hallucinate.

If data is limited, say so.

Provide:

• competitive insight  
• strategic positioning  
• capability differences  
• ecosystem signals  

GRAPH RELATIONSHIPS:
{context}


QUESTION:
{query}
"""


    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False
        }
    )

    data = response.json().get("response", "")

    if not data:
        return "No strategic insight could be generated from the current graph."

    return data


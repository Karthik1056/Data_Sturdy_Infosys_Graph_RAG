import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "qwen2.5:3b-instruct-q4_K_M"


def generate_answer(query, context):
    prompt = f"""
    Act as a Senior Enterprise Strategy Analyst specializing in AI-driven competitive intelligence.
    Analyze the provided Knowledge Graph context to generate a high-density strategic report.
    
    RULES:
    - RETURN ONLY VALID JSON. No conversational text.
    - Ground all insights in the provided Graph Data.
    - If data is sparse, prioritize "Ecosystem Signals" based on available triples.

    OUTPUT SCHEMA:
    {{
      "executive_summary": "A 50-sentence synthesis of the competitive landscape.",
      "market_sentiment": "Accelerating | Correcting | Consolidated",
      "entities": [
        {{
          "name": "Full Entity Name",
          "core_strategy": "Primary strategic objective",
          "capabilities": ["List specific technical/operational strengths"],
          "weakness_gap": "Potential vulnerability identified",
          "ecosystem_signals": "Upcoming moves, hiring trends, or patent focus",
          "swot": {{ "strengths": [], "threats": [] }}
        }}
      ],
      "strategic_differences": [
        {{
          "dimension": "e.g., Pricing, AI Maturity, GTM Strategy",
          "entity_a_status": "...",
          "entity_b_status": "..."
        }}
      ],
      "recommended_actions": ["3-5 high-impact strategic pivots based on the gaps"]
    }}

    GRAPH DATA:
    {context}

    QUESTION:
    {query}
    """
    # ... rest of your existing requests logic
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False
        }
    )

    data = response.json().get("response", "")
    print("Raw LLM Output:", data)

    if not data:
        return "No strategic insight could be generated from the current graph."

    return data


# import requests

# OLLAMA_URL = "http://localhost:11434/api/generate"
# MODEL = "qwen2.5:3b-instruct-q4_K_M"


# def extract_intent(query: str):

#     prompt = f"""
# You are an enterprise query analyzer.

# Extract:

# 1. intent_type (compare, discovery, partnership, strategy, competition, leadership)
# 2. focus_area (AI, cloud, GenAI, partnerships, acquisitions etc)
# 3. companies (ONLY if explicitly mentioned)

# Return STRICT JSON:

# {{
#  "intent_type": "",
#  "focus_area": "",
#  "companies": []
# }}

# QUERY:
# {query}
# """

#     response = requests.post(
#         OLLAMA_URL,
#         json={
#             "model": MODEL,
#             "prompt": prompt,
#             "stream": False
#         }
#     )

#     data = response.json()["response"]

#     import json
#     return json.loads(data)


import requests
import json

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "qwen2.5:3b-instruct-q4_K_M"


def extract_intent(query: str):

    prompt = f"""
Return ONLY valid JSON.

No explanation.
No markdown.
No thinking.

FORMAT:

{{
 "intent_type": "",
 "focus_area": "",
 "companies": []
}}

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
                    "temperature": 0.1
                }
            },
            timeout=60
        )

        data = response.json().get("response", "").strip()

        # ⭐ GUARD 1 → empty response
        if not data:
            raise ValueError("LLM returned empty response")

        # ⭐ GUARD 2 → extract JSON if model added text
        start = data.find("{")
        end = data.rfind("}") + 1

        clean_json = data[start:end]

        intent = json.loads(clean_json)

        # ⭐ GUARD 3 → ensure keys exist
        return {
            "intent_type": intent.get("intent_type", "discovery"),
            "focus_area": intent.get("focus_area", ""),
            "companies": intent.get("companies", [])
        }

    except Exception as e:

        print("⚠️ Intent extraction failed:", e)

        # ⭐ FAILSAFE MODE (VERY IMPORTANT)

        return {
            "intent_type": "discovery",
            "focus_area": query,
            "companies": []
        }

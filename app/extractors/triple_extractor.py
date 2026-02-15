import requests
import json

OLLAMA_URL = "http://localhost:11434/api/generate"

MODEL = "qwen2.5:3b-instruct-q4_K_M"


def extract_triples(text: str):

    prompt = f"""
You are an elite knowledge graph extraction system.

Extract ONLY strategic, boardroom-level knowledge.

IGNORE:
- founding year
- headquarters
- slogans
- employee counts
- generic descriptions

FOCUS ON:
- AI strategy
- digital transformation
- platforms
- partnerships
- acquisitions
- capabilities
- competitive positioning

RETURN STRICT JSON.

FORMAT:

[
 {{
   "subject": "Infosys",
   "predicate": "INVESTS_IN",
   "object": "Generative AI",
   "object_type": "Technology",
   "confidence": 0.82
 }}
]

RULES:

- predicate MUST be uppercase with underscores
- object_type MUST be one of:

Company  
Technology  
Platform  
Sector  
Strategy  
Partnership  
Acquisition  
Capability  

- MAXIMUM 5 triples
- confidence must be 0–1
- ignore anything below 0.65
- no explanations
- no extra text

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

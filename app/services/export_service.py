# from typing import Dict, List


# CATEGORY_KEYWORDS = {
#     "AI Brand": ["ai", "genai", "llm", "copilot", "assistant", "intelligence"],
#     "Cloud Brand": ["cloud", "platform", "infrastructure", "migration", "kubernetes"],
# }


# def _company_brand_signals(company: str) -> List[dict]:
#     from app.graph.neo4j_client import get_session

#     cypher = """
#     MATCH (c:Company {name: $company})-[r]->(o)
#     RETURN type(r) AS relation, o.name AS object
#     LIMIT 200
#     """

#     with get_session() as session:
#         result = session.run(cypher, company=company)
#         return [dict(row) for row in result]


# def _pick_best_signal(signals: List[dict], keywords: List[str]) -> str:
#     best_value = ""
#     best_score = 0

#     for signal in signals:
#         relation = str(signal.get("relation", "")).lower()
#         obj = str(signal.get("object", "")).strip()
#         haystack = f"{relation} {obj.lower()}"
#         score = sum(1 for kw in keywords if kw in haystack)

#         if score > best_score and obj:
#             best_score = score
#             best_value = obj

#     return best_value or "N/A"


# def service_mapping(companies: List[str]) -> Dict:
#     normalized = [c.strip() for c in companies if c and c.strip()]
#     if not normalized:
#         normalized = ["Infosys", "TCS", "Accenture"]

#     categories = list(CATEGORY_KEYWORDS.keys())
#     company_signals: Dict[str, List[dict]] = {}

#     for company in normalized:
#         try:
#             company_signals[company] = _company_brand_signals(company)
#         except Exception:
#             company_signals[company] = []

#     rows = []

#     for category in categories:
#         row = {"Category": category}
#         for company in normalized:
#             value = _pick_best_signal(
#                 company_signals.get(company, []),
#                 CATEGORY_KEYWORDS[category],
#             )
#             row[company] = value
#         rows.append(row)

#     return {
#         "companies": normalized,
#         "rows": rows,
#     }


# def service_mapping_markdown(companies: List[str]) -> str:
#     payload = service_mapping(companies)
#     companies = payload["companies"]
#     rows = payload["rows"]

#     header = "| Category | " + " | ".join(companies) + " |"
#     divider = "| :--- | " + " | ".join([":---"] * len(companies)) + " |"

#     body = []
#     for row in rows:
#         values = [row.get(company, "N/A") for company in companies]
#         body.append(f"| {row['Category']} | " + " | ".join(values) + " |")

#     return "\n".join([header, divider, *body])


from typing import Dict, List

# Updated keywords to match your specific Graph Data nodes
CATEGORY_KEYWORDS = {
    "AI Brand": [
        "ai", "genai", "llm", "copilot", "assistant", "intelligence", 
        "topaz", "navigator", "gpt", "foundation model"
    ],
    "Cloud Brand": [
        "cloud", "platform", "infrastructure", "migration", "kubernetes", 
        "cobalt", "cloudex", "first", "aws", "azure"
    ],
}


def _company_brand_signals(company: str) -> List[dict]:
    from app.graph.neo4j_client import get_session

    # Fetch ANY relationship to ANY node (Offerings, Strategies, Tools)
    cypher = """
    MATCH (c:Company {name: $company})-[r]->(o)
    RETURN type(r) AS relation, o.name AS object
    LIMIT 200
    """

    with get_session() as session:
        result = session.run(cypher, company=company)
        records = [dict(row) for row in result]

        # --- DEBUG PRINTING ---
        print(f"\n[FR4 DEBUG] Scanning Graph for: {company}")
        if not records:
            print(f"   -> No signals found (Check if node '{company}' exists)")
        else:
            for i, row in enumerate(records):
                # Print first few signals to verify data flow
                if i < 8: 
                    print(f"   -> Found: ({company}) -[{row['relation']}]-> ({row['object']})")
        print("------------------------------------------------")
        # ----------------------

        return records


def _pick_best_signal(signals: List[dict], keywords: List[str]) -> str:
    """
    Scans the signals and picks the one that matches the keywords best.
    Example: 'Infosys Topaz AI' matches 'ai' and 'topaz' -> High Score.
    """
    best_value = ""
    best_score = 0

    for signal in signals:
        relation = str(signal.get("relation", "")).lower()
        obj = str(signal.get("object", "")).strip()
        
        # We search in both the relationship name and the object name
        haystack = f"{relation} {obj.lower()}"
        
        # Count how many keywords appear in the string
        score = sum(1 for kw in keywords if kw in haystack)

        if score > best_score and obj:
            best_score = score
            best_value = obj

    return best_value or "N/A"


def service_mapping(companies: List[str]) -> Dict:
    normalized = [c.strip() for c in companies if c and c.strip()]
    if not normalized:
        # Default columns if none provided
        normalized = ["Infosys", "TCS", "Accenture"]

    categories = list(CATEGORY_KEYWORDS.keys())
    company_signals: Dict[str, List[dict]] = {}

    # 1. Fetch raw data for all companies
    for company in normalized:
        try:
            company_signals[company] = _company_brand_signals(company)
        except Exception as e:
            print(f"[GRAPH ERROR] {e}")
            company_signals[company] = []

    rows = []

    # 2. Process data into rows
    for category in categories:
        row = {"Category": category}
        for company in normalized:
            # Find the best match for this specific category (AI or Cloud)
            value = _pick_best_signal(
                company_signals.get(company, []),
                CATEGORY_KEYWORDS[category],
            )
            row[company] = value
        rows.append(row)

    return {
        "companies": normalized,
        "rows": rows,
    }


def service_mapping_markdown(companies: List[str]) -> str:
    """Helper to generate a Markdown table for the UI"""
    payload = service_mapping(companies)
    companies = payload["companies"]
    rows = payload["rows"]

    header = "| Category | " + " | ".join(companies) + " |"
    divider = "| :--- | " + " | ".join([":---"] * len(companies)) + " |"

    body = []
    for row in rows:
        values = [row.get(company, "N/A") for company in companies]
        body.append(f"| {row['Category']} | " + " | ".join(values) + " |")

    return "\n".join([header, divider, *body])
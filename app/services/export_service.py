from typing import Dict, List


CATEGORY_KEYWORDS = {
    "AI Brand": ["ai", "genai", "llm", "copilot", "assistant", "intelligence"],
    "Cloud Brand": ["cloud", "platform", "infrastructure", "migration", "kubernetes"],
}


def _company_brand_signals(company: str) -> List[dict]:
    from app.graph.neo4j_client import get_session

    cypher = """
    MATCH (c:Company {name: $company})-[r]->(o)
    RETURN type(r) AS relation, o.name AS object
    LIMIT 200
    """

    with get_session() as session:
        result = session.run(cypher, company=company)
        return [dict(row) for row in result]


def _pick_best_signal(signals: List[dict], keywords: List[str]) -> str:
    best_value = ""
    best_score = 0

    for signal in signals:
        relation = str(signal.get("relation", "")).lower()
        obj = str(signal.get("object", "")).strip()
        haystack = f"{relation} {obj.lower()}"
        score = sum(1 for kw in keywords if kw in haystack)

        if score > best_score and obj:
            best_score = score
            best_value = obj

    return best_value or "N/A"


def service_mapping(companies: List[str]) -> Dict:
    normalized = [c.strip() for c in companies if c and c.strip()]
    if not normalized:
        normalized = ["Infosys", "TCS", "Accenture"]

    categories = list(CATEGORY_KEYWORDS.keys())
    company_signals: Dict[str, List[dict]] = {}

    for company in normalized:
        try:
            company_signals[company] = _company_brand_signals(company)
        except Exception:
            # Keep endpoint available when graph is unreachable.
            company_signals[company] = []

    rows = []

    for category in categories:
        row = {"Category": category}
        for company in normalized:
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

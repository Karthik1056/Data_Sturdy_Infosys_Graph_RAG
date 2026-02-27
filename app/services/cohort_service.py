# from typing import List


# DEFAULT_COHORT = [
#     "Infosys",
#     "TCS",
#     "Wipro",
#     "HCLTech",
#     "Accenture",
# ]


# def _graph_ranked_peers(subject: str, limit: int) -> List[str]:
#     from app.graph.neo4j_client import get_session

#     cypher = """
#     MATCH (target:Company {name: $subject})-[]-(shared)<-[]-(peer:Company)
#     WHERE peer.name <> $subject
#     WITH peer.name AS peer, count(DISTINCT shared) AS overlap
#     ORDER BY overlap DESC, peer ASC
#     LIMIT $limit
#     RETURN peer
#     """

#     with get_session() as session:
#         result = session.run(cypher, subject=subject, limit=max(limit * 3, 15))
#         return [record["peer"] for record in result if record.get("peer")]


# def build_competitive_cohort(subject: str = "Infosys", limit: int = 5) -> List[str]:
#     subject = (subject or "").strip() or DEFAULT_COHORT[0]
#     limit = max(limit, 1)

#     cohort = [subject]

#     try:
#         for peer in _graph_ranked_peers(subject, limit):
#             if peer not in cohort:
#                 cohort.append(peer)
#             if len(cohort) >= limit:
#                 return cohort
#     except Exception:
#         # Keep endpoint stable even when graph is unavailable.
#         pass

#     for company in DEFAULT_COHORT:
#         if company not in cohort:
#             cohort.append(company)
#         if len(cohort) >= limit:
#             break

#     return cohort


import json
from typing import Any, Dict, List

from app.llm.ollama import ask_ollama

def _graph_ranked_peers(subject: str, limit: int) -> List[str]:
    from app.graph.neo4j_client import get_session

    # Query to find peers and count shared connections
    cypher = """
    MATCH (target:Company {name: $subject})-[]-(shared)<-[]-(peer:Company)
    WHERE peer.name <> $subject
    WITH peer.name AS peer, count(DISTINCT shared) AS overlap
    ORDER BY overlap DESC, peer ASC
    LIMIT $limit
    RETURN peer, overlap
    """

    with get_session() as session:
        result = session.run(cypher, subject=subject, limit=max(limit * 3, 15))
        records = list(result)
        return [record["peer"] for record in records if record.get("peer")]


def build_competitive_cohort(subject: str = "Infosys", limit: int = 5) -> List[str]:
    """
    STRICT MODE: Returns ONLY competitors found in the Knowledge Graph.
    If the graph is empty or the company is not found, returns an empty list.
    """
    subject = (subject or "").strip()
    if not subject:
        return []

    cohort = [subject]

    try:
        graph_peers = _graph_ranked_peers(subject, limit)
        
        for peer in graph_peers:
            if peer not in cohort:
                cohort.append(peer)
            if len(cohort) >= limit:
                break
                
    except Exception as e:
        print(f"[GRAPH ERROR] Could not connect to Neo4j: {e}")

        pass

    return cohort


def _extract_json_payload(raw_response: str) -> Dict[str, Any]:
    if not raw_response:
        return {}

    cleaned = raw_response.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.strip("`")
        if cleaned.startswith("json"):
            cleaned = cleaned[4:].strip()

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        start = cleaned.find("{")
        end = cleaned.rfind("}")
        if start != -1 and end != -1 and end > start:
            try:
                return json.loads(cleaned[start : end + 1])
            except json.JSONDecodeError:
                return {}
        return {}


def build_llm_cohort_comparison(subject: str = "Infosys", limit: int = 5) -> Dict[str, Any]:
    normalized_subject = (subject or "").strip() or "Infosys"
    normalized_limit = max(2, int(limit or 5))

    cohort = build_competitive_cohort(normalized_subject, normalized_limit)
    peers = [peer for peer in cohort if peer.lower() != normalized_subject.lower()]

    if len(peers) < normalized_limit - 1:
        peers = peers[: normalized_limit - 1]

    peers_hint = ", ".join(peers) if peers else "TCS, Wipro, HCLTech, Accenture"

    prompt = f"""
You are a competitive intelligence analyst.
Create equivalent company comparisons for {normalized_subject}.

Return ONLY valid JSON with this exact schema:
{{
  "subject": "{normalized_subject}",
  "summary": "1-2 sentence high-level comparison summary",
  "comparisons": [
    {{"company": "peer company name", "comparison": "one concise sentence comparing with {normalized_subject}"}}
  ]
}}

Rules:
- Include exactly {normalized_limit - 1} peers.
- Prefer these likely peers if relevant: {peers_hint}.
- Companies must be direct market equivalents of {normalized_subject}.
- Keep each comparison under 30 words.
- No markdown, no extra keys, no prose outside JSON.
""".strip()

    try:
        llm_text = ask_ollama(prompt)
        payload = _extract_json_payload(llm_text)
    except Exception:
        payload = {}

    raw_comparisons = payload.get("comparisons", []) if isinstance(payload, dict) else []
    comparisons: List[Dict[str, str]] = []

    if isinstance(raw_comparisons, list):
        for item in raw_comparisons:
            if not isinstance(item, dict):
                continue
            company = str(item.get("company", "")).strip()
            comparison = str(item.get("comparison", "")).strip()
            if company and comparison and company.lower() != normalized_subject.lower():
                comparisons.append({"company": company, "comparison": comparison})

    seen = {c["company"].lower() for c in comparisons}
    for peer in peers:
        if len(comparisons) >= normalized_limit - 1:
            break
        key = peer.lower()
        if key in seen:
            continue
        comparisons.append(
            {
                "company": peer,
                "comparison": f"{peer} is a comparable enterprise-services competitor to {normalized_subject} with overlapping offerings and target segments.",
            }
        )
        seen.add(key)

    summary = ""
    if isinstance(payload, dict):
        summary = str(payload.get("summary", "")).strip()
    if not summary:
        summary = (
            f"{normalized_subject} competes with similar IT and digital-services firms that overlap in enterprise transformation, outsourcing, and consulting engagements."
        )

    final_cohort = [normalized_subject] + [item["company"] for item in comparisons]
    return {
        "subject": normalized_subject,
        "cohort": final_cohort[:normalized_limit],
        "summary": summary,
        "comparisons": comparisons[: normalized_limit - 1],
        "source": "llm",
    }
from typing import List


DEFAULT_COHORT = [
    "Infosys",
    "TCS",
    "Wipro",
    "HCLTech",
    "Accenture",
]


def _graph_ranked_peers(subject: str, limit: int) -> List[str]:
    from app.graph.neo4j_client import get_session

    cypher = """
    MATCH (target:Company {name: $subject})-[]-(shared)<-[]-(peer:Company)
    WHERE peer.name <> $subject
    WITH peer.name AS peer, count(DISTINCT shared) AS overlap
    ORDER BY overlap DESC, peer ASC
    LIMIT $limit
    RETURN peer
    """

    with get_session() as session:
        result = session.run(cypher, subject=subject, limit=max(limit * 3, 15))
        return [record["peer"] for record in result if record.get("peer")]


def build_competitive_cohort(subject: str = "Infosys", limit: int = 5) -> List[str]:
    subject = (subject or "").strip() or DEFAULT_COHORT[0]
    limit = max(limit, 1)

    cohort = [subject]

    try:
        for peer in _graph_ranked_peers(subject, limit):
            if peer not in cohort:
                cohort.append(peer)
            if len(cohort) >= limit:
                return cohort
    except Exception:
        # Keep endpoint stable even when graph is unavailable.
        pass

    for company in DEFAULT_COHORT:
        if company not in cohort:
            cohort.append(company)
        if len(cohort) >= limit:
            break

    return cohort

from typing import Dict, List

from app.graph.neo4j_client import get_session


def threat_assessment(company: str, competitor: str, partner: str) -> Dict:
    
    company = (company or "").strip()
    competitor = (competitor or "").strip()
    partner = (partner or "").strip()

    cypher = """
    MATCH (comp:Company {name: $company})-[r1]->(p {name: $partner})<-[r2]-(peer:Company {name: $competitor})
    RETURN
      comp.name AS company,
      type(r1) AS company_relation,
      p.name AS partner,
      type(r2) AS competitor_relation,
      peer.name AS competitor
    LIMIT 25
    """

    overlaps: List[dict] = []

    with get_session() as session:
        result = session.run(
            cypher,
            company=company,
            competitor=competitor,
            partner=partner,
        )
        overlaps = [dict(r) for r in result]

    threat_level = "LOW"
    if len(overlaps) >= 3:
        threat_level = "HIGH"
    elif len(overlaps) >= 1:
        threat_level = "MEDIUM"

    return {
        "company": company,
        "competitor": competitor,
        "partner": partner,
        "shared_paths": overlaps,
        "threat_level": threat_level,
        "summary": (
            f"{competitor} has {len(overlaps)} shared {partner}-linked relationship path(s) "
            f"with {company}; estimated pressure is {threat_level}."
        ),
    }
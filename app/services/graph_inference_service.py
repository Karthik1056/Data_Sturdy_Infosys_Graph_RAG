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
    
    # Gather additional graph context
    context_cypher = """
    MATCH (comp:Company {name: $company})-[r]-(n)
    RETURN type(r) as relation, labels(n) as labels, n.name as name
    LIMIT 20
    """
    
    company_context = []
    with get_session() as session:
        result = session.run(context_cypher, company=company)
        company_context = [dict(r) for r in result]
    
    # Generate comprehensive LLM analysis with graph context
    from app.llm.ollama import ask_ollama
    
    graph_context_str = "\n".join([f"- {c['name']} ({c['labels'][0] if c['labels'] else 'Unknown'}): {c['relation']}" for c in company_context[:10]])
    
    analysis_prompt = f"""You are a competitive intelligence analyst. Analyze the competitive threat between {company} and {competitor} regarding {partner}.

**Graph Intelligence Data:**
- Shared connection paths: {len(overlaps)}
- Initial threat level: {threat_level}
- {company}'s known relationships:
{graph_context_str if graph_context_str else '  Limited graph data available'}

**Required Analysis:**
Provide a comprehensive strategic assessment with these sections:

1. **Competitive Risk Score**: Rate 0-100 with justification

2. **Strengths of {company}**: 
   - Core competitive advantages
   - Market positioning strengths
   - Strategic assets

3. **Weaknesses of {company}**:
   - Vulnerabilities vs {competitor}
   - Areas needing improvement
   - Potential exposure points

4. **Strategic Threats from {competitor}**:
   - Immediate competitive risks
   - Long-term strategic concerns
   - Market share implications

5. **Recommended Counter-Strategies**:
   - Defensive tactics
   - Offensive opportunities
   - Partnership leverage with {partner}

6. **Market Position Impact**:
   - How this affects {company}'s standing
   - Industry implications

Be specific, actionable, and strategic. Use your knowledge of these companies even if graph data is limited."""
    
    try:
        llm_analysis = ask_ollama(analysis_prompt)
    except Exception as e:
        llm_analysis = f"Analysis unavailable. {competitor} has {len(overlaps)} shared {partner}-linked paths with {company}. Threat level: {threat_level}."

    return {
        "company": company,
        "competitor": competitor,
        "partner": partner,
        "shared_paths": overlaps,
        "threat_level": threat_level,
        "summary": f"{competitor} has {len(overlaps)} shared {partner}-linked relationship path(s) with {company}; estimated pressure is {threat_level}.",
        "analysis": llm_analysis,
        "graph_context": company_context[:10]
    }


def get_graph_visualization(center_node: str = "Infosys"):
    from app.graph.neo4j_client import get_session
    
    cypher = """
    MATCH (c:Company {name: $center})-[r]-(neighbor)
    RETURN c, r, neighbor
    LIMIT 50
    """
    
    nodes = {}
    links = []
    
    with get_session() as session:
        result = session.run(cypher, center=center_node)
        
        for record in result:
            source = record["c"]
            target = record["neighbor"]
            rel = record["r"]
            
            nodes[source.element_id] = {
                "id": source.element_id, 
                "name": source.get("name", "Unknown"), 
                "label": list(source.labels)[0] if source.labels else "Node",
                "type": "center"
            }
            nodes[target.element_id] = {
                "id": target.element_id, 
                "name": target.get("name", "Unknown"),
                "label": list(target.labels)[0] if target.labels else "Node",
                "type": "neighbor"
            }
            
            links.append({
                "source": source.element_id,
                "target": target.element_id,
                "type": rel.type
            })

    return {
        "nodes": list(nodes.values()),
        "links": links
    }


def get_battlecard_data(center_node: str = "Infosys"):
    """Get battlecard visualization data with center company and competitors plus LLM summary"""
    from app.graph.neo4j_client import get_session
    from app.llm.ollama import ask_ollama
    
    cypher = """
    MATCH (c:Company {name: $center})-[r]-(other)
    WHERE other:Company OR other:Organization
    RETURN DISTINCT other.name AS competitor
    LIMIT 10
    """
    
    competitors = []
    
    with get_session() as session:
        result = session.run(cypher, center=center_node)
        competitors = [record["competitor"] for record in result if record["competitor"] and record["competitor"] != center_node]
    
    if not competitors:
        from app.services.cohort_service import build_competitive_cohort
        competitors = build_competitive_cohort(center_node)
    
    # Generate LLM summary
    summary_prompt = f"""Provide a brief competitive analysis summary for {center_node} in relation to these competitors: {', '.join(competitors[:5])}. Focus on market position and key differentiators. Keep it under 100 words."""
    
    try:
        summary = ask_ollama(summary_prompt)
    except:
        summary = f"{center_node} operates in a competitive landscape with {len(competitors)} key players."
    
    return {
        "center": center_node,
        "competitors": competitors[:10],
        "summary": summary
    }


def get_battlecard_comparison(company1: str, company2: str = ""):
    """Get battlecard comparison between two companies"""
    from app.graph.neo4j_client import get_session
    from app.llm.ollama import ask_ollama
    
    if not company2:
        # Fallback to single company mode
        return get_battlecard_data(company1)
    
    # Get shared connections between two companies
    cypher = """
    MATCH (c1:Company {name: $company1})-[r1]-(shared)-[r2]-(c2:Company {name: $company2})
    RETURN DISTINCT shared.name AS connection, type(r1) AS rel1, type(r2) AS rel2
    LIMIT 20
    """
    
    connections = []
    with get_session() as session:
        result = session.run(cypher, company1=company1, company2=company2)
        connections = [dict(r) for r in result]
    
    # Generate LLM comparison
    comparison_prompt = f"""Compare {company1} vs {company2} in terms of competitive positioning, strengths, and market strategy. 
They have {len(connections)} shared connections in the market. Provide a brief analysis under 150 words."""
    
    try:
        summary = ask_ollama(comparison_prompt)
    except:
        summary = f"Competitive comparison between {company1} and {company2} with {len(connections)} shared market connections."
    
    return {
        "company1": company1,
        "company2": company2,
        "connections": [c["connection"] for c in connections],
        "connection_details": connections,
        "summary": summary
    }

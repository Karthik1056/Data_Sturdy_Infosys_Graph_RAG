from typing import Dict, List

from app.crawlers.research_engine import dynamic_research


SECTION_QUERY_SUFFIX = {
    "insights": "insights",
    "press": "press release newsroom",
    "investor": "investor relations quarterly results",
}


def _allowed_domains(company: str) -> List[str]:
    company_key = (company or "").strip().lower()

    domain_map = {
        "infosys": ["infosys.com"],
        "tcs": ["tcs.com"],
        "accenture": ["accenture.com"],
        "wipro": ["wipro.com"],
        "hcltech": ["hcltech.com"],
    }

    return domain_map.get(company_key, [f"{company_key}.com"] if company_key else [])


def crawl_company_sections(company: str, sections: List[str]) -> Dict[str, List[dict]]:
    """
    Runs targeted crawl queries and retains only results from company-owned domains.
    """
    company = (company or "").strip()
    selected_sections = sections or ["insights", "press", "investor"]
    allowed_domains = _allowed_domains(company)

    section_results: Dict[str, List[dict]] = {}

    for section in selected_sections:
        suffix = SECTION_QUERY_SUFFIX.get(section.lower(), section)
        query = f"{company} {suffix}".strip()

        results = dynamic_research(query)

        if allowed_domains:
            results = [
                r
                for r in results
                if any(domain in (r.get("url") or "") for domain in allowed_domains)
            ]

        section_results[section] = results

    return section_results


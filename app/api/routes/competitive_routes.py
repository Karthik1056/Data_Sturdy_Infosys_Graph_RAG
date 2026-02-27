from typing import List

from fastapi import APIRouter, Query

from app.services.cohort_service import build_llm_cohort_comparison
from app.services.export_service import service_mapping, service_mapping_markdown

from app.services.graph_inference_service import threat_assessment
from app.services.targeted_crawl_service import crawl_company_sections
from app.services.graph_inference_service import get_graph_visualization

router = APIRouter(prefix="/competitive", tags=["competitive-intelligence"])


@router.get("/cohort")
def get_cohort(subject: str = "Infosys", limit: int = 5):
    return build_llm_cohort_comparison(subject=subject, limit=limit)


@router.get("/export/service-map")
def export_service_map(
    companies: List[str] = Query(default=["Infosys", "TCS", "Accenture"]),
    format: str = "json",
):
    """FR4: Export Service Comparison Table"""
    if format.lower() == "markdown":
        table = service_mapping_markdown(companies)
        return {"format": "markdown", "table": table}

    return {"format": "json", **service_mapping(companies)}


@router.get("/crawl/sections")
def crawl_sections(
    company: str = "Infosys",
    sections: List[str] = Query(default=["insights", "press", "investor"]),
):
    results = crawl_company_sections(company, sections)
    return {
        "company": company,
        "sections": sections,
        "results": results,
    }

@router.get("/intel/threat")
def threat_intel(company: str = "", competitor: str = "", partner: str = ""):
    return threat_assessment(company=company, competitor=competitor, partner=partner)


@router.get("/graph/visualize")
def visualize_graph(subject: str = "Infosys"):
    return get_graph_visualization(subject)


@router.get("/battlecard")
def get_battlecard(company1: str, company2: str = ""):
    """Get battlecard data showing two companies in competitive comparison"""
    from app.services.graph_inference_service import get_battlecard_comparison
    return get_battlecard_comparison(company1, company2)
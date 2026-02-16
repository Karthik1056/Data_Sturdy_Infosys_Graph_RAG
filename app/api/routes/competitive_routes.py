from typing import List

from fastapi import APIRouter, Query

from app.services.cohort_service import build_competitive_cohort
from app.services.export_service import service_mapping, service_mapping_markdown
from app.services.graph_inference_service import threat_assessment
from app.services.targeted_crawl_service import crawl_company_sections

router = APIRouter(prefix="/competitive", tags=["competitive-intelligence"])


@router.get("/cohort")
def get_cohort(subject: str = "Infosys"):
    cohort = build_competitive_cohort(subject)
    return {"subject": subject, "cohort": cohort}


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
def threat_intel(company: str = "Infosys", competitor: str = "Accenture", partner: str = "NVIDIA"):
    return threat_assessment(company=company, competitor=competitor, partner=partner)


@router.get("/export/service-map")
def export_service_map(
    companies: List[str] = Query(default=["Infosys", "TCS", "Accenture"]),
    format: str = "json",
):
    if format.lower() == "markdown":
        table = service_mapping_markdown(companies)
        return {"format": "markdown", "table": table}

    return {"format": "json", **service_mapping(companies)}
from fastapi import APIRouter
from app.pipeline.graph_reasoning_pipeline import run_reasoning_pipeline

router = APIRouter()


@router.get("/intel")
def company_intelligence(query: str):

    return run_reasoning_pipeline(query)

from typing import Dict

from app.pipeline.graph_pipeline import run_graph_pipeline
from app.pipeline.graph_reasoning_pipeline import run_reasoning_pipeline


def run_research_cycle(query: str) -> Dict:
    """
    LangGraph-ready orchestration shim.

    This function keeps the state shape explicit so it can be migrated into
    a true LangGraph DAG with minimal refactor.
    """
    state = {
        "query": query,
        "research": None,
        "reasoning": None,
    }

    state["research"] = run_graph_pipeline(query)
    state["reasoning"] = run_reasoning_pipeline(query)

    return state
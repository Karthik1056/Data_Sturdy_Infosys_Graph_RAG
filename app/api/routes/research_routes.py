# from fastapi import APIRouter
# from app.crawlers.research_planner import plan_research
# from app.pipeline.graph_pipeline import run_graph_pipeline

# router = APIRouter()


# # Phase 1 ONLY
# @router.get("/research")
# def research(query: str):
#     return plan_research(query)


# @router.get("/build-graph")
# def build_graph(query: str):

#     run_graph_pipeline(query)

#     return {"message": "Graph build completed"}


from fastapi import APIRouter
from app.pipeline.graph_pipeline import run_graph_pipeline

router = APIRouter()


# @router.get("/research")
# def research(query: str):

#     result = run_graph_pipeline(query)

#     return {
#         "message": "Research completed and stored in Neo4j",
#         "query": query,
#         "triples_written": result
#     }

@router.get("/research")
def research(query: str):

    result = run_graph_pipeline(query)

    return result


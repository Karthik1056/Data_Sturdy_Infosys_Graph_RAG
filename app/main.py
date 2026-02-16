from fastapi import FastAPI
from app.api.routes.research_routes import router as research_router
from app.graph.neo4j_client import close_driver
from app.api.routes.source_routes import router as source_router
from app.api.routes.competitive_routes import router as competitive_router
app = FastAPI(title="Intelligence Research Engine")


from app.api.routes.intel_route import router as intel_router

app.include_router(intel_router)

app.include_router(research_router)
app.include_router(source_router)
app.include_router(competitive_router)

@app.on_event("shutdown")
def shutdown_db():
    close_driver()
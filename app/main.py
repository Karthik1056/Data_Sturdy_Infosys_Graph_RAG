from fastapi import FastAPI
from app.api.routes.research_routes import router as research_router
from app.graph.neo4j_client import close_driver
app = FastAPI(title="Intelligence Research Engine")

app.include_router(research_router)


@app.on_event("shutdown")
def shutdown_db():
    close_driver()
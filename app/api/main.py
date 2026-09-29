"""
SIH26143 — Main FastAPI Application.
Exposes clean REST and OpenAPI endpoints for the Maritime Forensic Intelligence Engine
and serves the interactive React + Leaflet frontend workstation.
"""

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
import uvicorn

from app.api.routes import health, incidents, investigation, falsification, evidence_selection, evaluation

app = FastAPI(
    title="SIH26143 Maritime Forensic Intelligence Engine",
    description=(
        "Scientific decision-support system that reconstructs spaceborne oil spill incidents, "
        "correlates them with historical AIS tracks, tests competing source hypotheses, "
        "executes adversarial falsification challenges, quantifies uncertainty, and recommends active sensing."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS for local development and frontend workstation
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount Modular Endpoint Routers
app.include_router(health.router, prefix="/api/v1")
app.include_router(incidents.router, prefix="/api/v1")
app.include_router(investigation.router, prefix="/api/v1")
app.include_router(falsification.router, prefix="/api/v1")
app.include_router(evidence_selection.router, prefix="/api/v1")
app.include_router(evaluation.router, prefix="/api/v1")


@app.get("/api/overview", tags=["Root"])
def root_overview():
    """API overview and service index."""
    return {
        "service": "SIH26143 Maritime Forensic Intelligence Engine API",
        "version": "1.0.0",
        "docs_url": "/docs",
        "health_check": "/api/v1/health",
        "demo_mode": True,
        "signature_endpoints": {
            "run_investigation": "POST /api/v1/investigation/run",
            "attack_hypothesis": "POST /api/v1/falsification/attack",
            "next_best_evidence": "GET /api/v1/evidence-selection/recommendations",
            "geospatial_layers": "GET /api/v1/investigation/layers/{case_id}",
            "compare_baseline": "GET /api/v1/evaluation/compare"
        }
    }


# Mount Static Assets and Frontend Workstation if compiled
frontend_dist = os.path.join(os.path.dirname(__file__), "..", "frontend", "dist")
frontend_assets = os.path.join(frontend_dist, "assets")

if os.path.exists(frontend_assets):
    app.mount("/assets", StaticFiles(directory=frontend_assets), name="assets")

@app.get("/", tags=["Workstation UI"])
def serve_workstation():
    """Serves the interactive Maritime Forensic Intelligence Workstation."""
    index_html = os.path.join(frontend_dist, "index.html")
    if os.path.exists(index_html):
        return FileResponse(index_html)
    return root_overview()


if __name__ == "__main__":
    uvicorn.run("app.api.main:app", host="0.0.0.0", port=8000, reload=True)

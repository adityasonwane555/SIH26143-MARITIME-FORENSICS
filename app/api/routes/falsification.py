"""Adversarial falsification endpoint router."""
from fastapi import APIRouter, HTTPException, Query
from typing import Dict, Any

from app.api.routes.investigation import get_dossier, _ENGINE
from src.config.schemas import FalsificationResult

router = APIRouter(prefix="/falsification", tags=["Adversarial Falsification"])

@router.post("/attack", response_model=FalsificationResult)
def attack_hypothesis_endpoint(
    case_id: str = Query("CASE_005_SYNTHETIC_CHALLENGE"),
    hypothesis_id: str = Query(..., description="ID of hypothesis to challenge (e.g. H_VESSEL_419000111)")
):
    """
    Executes real-time adversarial self-attack challenges against a specific candidate hypothesis:
    1. Spatial Overlap Challenge
    2. Temporal Feasibility Challenge
    3. Hydrodynamic Drift Direction Challenge
    4. Counterfactual Plume Simulation Challenge
    5. AIS Data Continuity Challenge
    """
    dossier = get_dossier(case_id)
    hyp = next((h for h in dossier.hypotheses if h.hypothesis_id == hypothesis_id), None)
    if not hyp:
        raise HTTPException(status_code=404, detail=f"Hypothesis {hypothesis_id} not found in dossier.")

    if not hyp.falsification:
        raise HTTPException(status_code=500, detail="Falsification result not evaluated.")

    return hyp.falsification

"""Active sensing and evidence selection endpoint router."""
from fastapi import APIRouter, HTTPException, Query
from typing import List

from app.api.routes.investigation import get_dossier
from src.config.schemas import NextEvidenceRecommendation

router = APIRouter(prefix="/evidence-selection", tags=["Active Sensing & Information Gain"])

@router.get("/recommendations", response_model=List[NextEvidenceRecommendation])
def get_recommendations(case_id: str = Query("CASE_005_SYNTHETIC_CHALLENGE")):
    """
    Returns mathematically ranked next-best-evidence actions
    based on Expected Information Gain (Entropy Reduction E[ΔH]).
    """
    dossier = get_dossier(case_id)
    return dossier.recommended_evidence

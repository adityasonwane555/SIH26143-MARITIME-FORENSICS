"""Incidents and case catalog router."""
from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
from src.ingestion.loader import ForensicDataLoader

router = APIRouter(prefix="/incidents", tags=["Incidents & Benchmark Cases"])

@router.get("", response_model=List[Dict[str, Any]])
def list_incidents():
    """Returns the catalog of historical and synthetic benchmark cases."""
    try:
        return ForensicDataLoader.load_case_catalog("data/metadata/cases.csv")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load case catalog: {str(e)}")

@router.get("/{incident_id}")
def get_incident_details(incident_id: str):
    """Retrieves metadata for a specific incident."""
    catalog = ForensicDataLoader.load_case_catalog("data/metadata/cases.csv")
    match = next((c for c in catalog if c["case_id"] == incident_id), None)
    if not match:
        raise HTTPException(status_code=404, detail=f"Incident {incident_id} not found in catalog.")
    return match

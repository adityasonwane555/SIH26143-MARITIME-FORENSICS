"""Investigation execution and geospatial layers router."""
from fastapi import APIRouter, HTTPException, Query
from typing import Dict, Any, Optional
import os
import json

from src.ingestion.loader import ForensicDataLoader
from src.attribution.engine import ForensicAttributionEngine
from src.config.schemas import ForensicDossier

router = APIRouter(prefix="/investigation", tags=["Forensic Investigation"])

# Cache for latest investigation dossier
_INVESTIGATION_CACHE: Dict[str, ForensicDossier] = {}
_ENGINE = ForensicAttributionEngine(dt_seconds=300.0)


def get_case_paths(case_id: str):
    """Resolves local data asset paths for a given incident case."""
    case_dir = os.path.join("data", "cases", case_id)
    if os.path.exists(case_dir):
        return (
            os.path.join(case_dir, "detected_slick.geojson"),
            os.path.join(case_dir, "metocean.json"),
            os.path.join(case_dir, "vessel_traffic.csv")
        )
    return (
        "data/synthetic/detected_slick.geojson",
        "data/synthetic/metocean.json",
        "data/synthetic/vessel_traffic.csv"
    )


@router.post("/run", response_model=ForensicDossier)
def run_investigation(
    case_id: str = Query("CASE_005_SYNTHETIC_CHALLENGE", description="ID of incident to analyze"),
    hindcast_hours: float = Query(6.0, ge=1.0, le=72.0, description="Backward simulation duration in hours")
):
    """Executes the closed-loop forensic investigation pipeline."""
    try:
        slick_path, metocean_path, ais_path = get_case_paths(case_id)

        if not os.path.exists(slick_path) or not os.path.exists(metocean_path) or not os.path.exists(ais_path):
            raise HTTPException(status_code=400, detail=f"Scenario assets for {case_id} not found.")

        catalog = ForensicDataLoader.load_case_catalog("data/metadata/cases.csv")
        case_meta = next((c for c in catalog if c["case_id"] == case_id), None)
        title = case_meta["incident_name"] if case_meta else f"Incident {case_id}"

        spill = ForensicDataLoader.load_slick_geojson(slick_path)
        metocean = ForensicDataLoader.load_metocean_json(metocean_path)
        tracks = ForensicDataLoader.load_ais_csv(ais_path)

        dossier = _ENGINE.run_investigation(
            incident_id=case_id,
            title=title,
            spill=spill,
            metocean=metocean,
            tracks=tracks,
            hindcast_hours=hindcast_hours
        )

        _INVESTIGATION_CACHE[case_id] = dossier
        return dossier

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Investigation failed: {str(e)}")



@router.get("/dossier/{case_id}", response_model=ForensicDossier)
def get_dossier(case_id: str):
    """Retrieves the latest cached investigation dossier for a case."""
    if case_id not in _INVESTIGATION_CACHE:
        # Auto-run if not cached yet
        return run_investigation(case_id=case_id)
    return _INVESTIGATION_CACHE[case_id]


@router.get("/layers/{case_id}")
def get_geospatial_layers(case_id: str):
    """
    Returns unified GeoJSON feature collection containing:
    - Observed satellite slick polygon
    - Origin probability surface contours (50%, 80%, 95%)
    - Vessel historical tracks
    - Candidate vessel closest approaches
    """
    dossier = get_dossier(case_id)

    features = []

    # 1. Observed Slick Polygon Feature
    if dossier.detected_slick:
        features.append({
            "type": "Feature",
            "properties": {
                "layer_type": "DETECTED_SLICK",
                "spill_id": dossier.detected_slick.spill_id,
                "area_km2": dossier.detected_slick.area_km2,
                "perimeter_km": dossier.detected_slick.perimeter_km,
                "confidence": dossier.detected_slick.confidence,
                "orientation_deg": dossier.detected_slick.orientation_deg
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": dossier.detected_slick.coordinates[0] if isinstance(dossier.detected_slick.coordinates[0][0], list) else dossier.detected_slick.coordinates
            }
        })

    # 2. Origin Probability Surface Contours
    if dossier.origin_estimate and dossier.origin_estimate.contour_geojson:
        for c_feat in dossier.origin_estimate.contour_geojson.get("features", []):
            c_feat["properties"]["layer_type"] = "ORIGIN_PROBABILITY_CONTOUR"
            features.append(c_feat)

    # 3. AIS Vessel Tracks
    _, _, ais_path = get_case_paths(case_id)
    tracks = ForensicDataLoader.load_ais_csv(ais_path)
    for t in tracks:

        line_coords = [[p.longitude, p.latitude] for p in t.points]
        features.append({
            "type": "Feature",
            "properties": {
                "layer_type": "AIS_TRACK",
                "mmsi": t.mmsi,
                "vessel_name": t.vessel_name,
                "vessel_type": t.vessel_type,
                "has_gaps": t.has_gaps,
                "max_gap_minutes": t.max_gap_minutes,
                "quality_score": t.quality_score
            },
            "geometry": {
                "type": "LineString",
                "coordinates": line_coords
            }
        })

    return {
        "type": "FeatureCollection",
        "case_id": case_id,
        "features": features
    }


@router.get("/export/{case_id}")
def export_investigation_report(
    case_id: str,
    format: str = Query("markdown", description="Export format: markdown, html, or json")
):
    """
    Exports complete forensic investigation dossier in archival/presentation format.
    Satisfies SIH26143 Master Build Specification Sections 75 and 76.
    """
    from fastapi.responses import HTMLResponse, PlainTextResponse, JSONResponse
    from src.attribution.report_exporter import ForensicReportExporter

    dossier = get_dossier(case_id)

    fmt = format.lower().strip()
    if fmt == "html":
        return HTMLResponse(content=ForensicReportExporter.to_html(dossier))
    elif fmt == "json":
        return JSONResponse(content=json.loads(ForensicReportExporter.to_json(dossier)))
    else:
        return PlainTextResponse(content=ForensicReportExporter.to_markdown(dossier), media_type="text/markdown")


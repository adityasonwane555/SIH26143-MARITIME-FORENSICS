"""
Integration tests for FastAPI endpoints (Gate 7).
"""

import pytest
from fastapi.testclient import TestClient
from app.api.main import app

client = TestClient(app)


def test_api_root():
    response = client.get("/api/overview")
    assert response.status_code == 200
    data = response.json()
    assert "service" in data
    assert data["version"] == "1.0.0"


def test_api_workstation():
    response = client.get("/")
    assert response.status_code == 200


def test_api_health():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


def test_api_incidents():
    response = client.get("/api/v1/incidents")
    assert response.status_code == 200
    cases = response.json()
    assert len(cases) >= 5
    case_ids = [c["case_id"] for c in cases]
    assert "CASE_005_SYNTHETIC_CHALLENGE" in case_ids


def test_api_run_investigation():
    response = client.post("/api/v1/investigation/run?case_id=CASE_005_SYNTHETIC_CHALLENGE&hindcast_hours=6.0")
    assert response.status_code == 200
    dossier = response.json()
    assert dossier["incident_id"] == "CASE_005_SYNTHETIC_CHALLENGE"
    assert dossier["decision"] == "attributed"
    assert dossier["leading_subject_name"] == "MV Ocean Pioneer"
    assert len(dossier["hypotheses"]) >= 5


def test_api_geospatial_layers():
    response = client.get("/api/v1/investigation/layers/CASE_005_SYNTHETIC_CHALLENGE")
    assert response.status_code == 200
    geojson = response.json()
    assert geojson["type"] == "FeatureCollection"
    layer_types = [f["properties"].get("layer_type") for f in geojson["features"]]
    assert "DETECTED_SLICK" in layer_types
    assert "ORIGIN_PROBABILITY_CONTOUR" in layer_types
    assert "AIS_TRACK" in layer_types


def test_api_attack_hypothesis():
    # Attack MV Arabian Star -> should return falsified result
    response = client.post("/api/v1/falsification/attack?case_id=CASE_005_SYNTHETIC_CHALLENGE&hypothesis_id=H_VESSEL_419000333")
    assert response.status_code == 200
    falsif = response.json()
    assert falsif["survives"] is False
    assert falsif["challenges_failed"] >= 1
    assert any("HYDRODYNAMIC_FAILURE" in r for r in falsif["contradicting_reasons"])


def test_api_evidence_recommendations():
    response = client.get("/api/v1/evidence-selection/recommendations?case_id=CASE_005_SYNTHETIC_CHALLENGE")
    assert response.status_code == 200
    recs = response.json()
    assert len(recs) >= 1
    assert recs[0]["expected_information_gain_bits"] >= 0.0


def test_api_evaluation_compare():
    response = client.get("/api/v1/evaluation/compare?case_id=CASE_005_SYNTHETIC_CHALLENGE")
    assert response.status_code == 200
    data = response.json()
    assert "baseline" in data
    assert "proposed_engine" in data
    assert data["improvements"]["candidate_separation_margin_expansion_pct"] > 0.0


def test_api_export_report():
    # Test Markdown export
    res_md = client.get("/api/v1/investigation/export/CASE_005_SYNTHETIC_CHALLENGE?format=markdown")
    assert res_md.status_code == 200
    assert "MARITIME FORENSIC INTELLIGENCE DOSSIER" in res_md.text

    # Test HTML export
    res_html = client.get("/api/v1/investigation/export/CASE_005_SYNTHETIC_CHALLENGE?format=html")
    assert res_html.status_code == 200
    assert "<html" in res_html.text
    assert "Maritime Forensic Intelligence Dossier" in res_html.text

    # Test JSON export
    res_json = client.get("/api/v1/investigation/export/CASE_005_SYNTHETIC_CHALLENGE?format=json")
    assert res_json.status_code == 200
    data = res_json.json()
    assert data["incident_id"] == "CASE_005_SYNTHETIC_CHALLENGE"


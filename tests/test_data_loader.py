"""
Unit tests for data loaders and schema validators (Gate 2).
"""

import os
import pytest
from src.ingestion.loader import ForensicDataLoader
from src.config.schemas import SpillPolygon, MetoceanObservation, AISTrack


def test_load_case_catalog():
    catalog = ForensicDataLoader.load_case_catalog("data/metadata/cases.csv")
    assert len(catalog) >= 5
    case_ids = [c["case_id"] for c in catalog]
    assert "CASE_001_WAKASHIO" in case_ids
    assert "CASE_005_SYNTHETIC_CHALLENGE" in case_ids
    for c in catalog:
        assert "incident_name" in c
        assert "latitude" in c
        assert "longitude" in c


def test_load_slick_geojson():
    slick_path = "data/synthetic/detected_slick.geojson"
    assert os.path.exists(slick_path)
    slick = ForensicDataLoader.load_slick_geojson(slick_path)
    assert isinstance(slick, SpillPolygon)
    assert slick.spill_id == "SYNTH_SPILL_001"
    assert slick.area_km2 > 0.0
    assert slick.perimeter_km > 0.0
    assert slick.elongation >= 1.0
    assert 0.0 <= slick.confidence <= 1.0
    assert len(slick.coordinates[0]) >= 30


def test_load_metocean_json():
    metocean_path = "data/synthetic/metocean.json"
    assert os.path.exists(metocean_path)
    met = ForensicDataLoader.load_metocean_json(metocean_path)
    assert isinstance(met, MetoceanObservation)
    assert met.u_current_ms == 0.25
    assert met.v_current_ms == -0.15
    assert met.u_wind10_ms == 4.0
    assert met.v_wind10_ms == -3.0


def test_load_ais_csv():
    ais_path = "data/synthetic/vessel_traffic.csv"
    assert os.path.exists(ais_path)
    tracks = ForensicDataLoader.load_ais_csv(ais_path)
    assert len(tracks) == 3
    track_by_mmsi = {t.mmsi: t for t in tracks}

    assert "419000111" in track_by_mmsi  # Alpha
    assert "419000222" in track_by_mmsi  # Beta
    assert "419000333" in track_by_mmsi  # Gamma

    alpha = track_by_mmsi["419000111"]
    assert alpha.vessel_name == "MV Ocean Pioneer"
    assert not alpha.has_gaps
    assert alpha.quality_score >= 0.9

    gamma = track_by_mmsi["419000333"]
    assert gamma.vessel_name == "MV Arabian Star"
    assert gamma.has_gaps is True  # 3-hour transponder gap detected
    assert gamma.max_gap_minutes >= 120.0
    assert gamma.quality_score < 0.9

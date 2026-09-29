"""
Unit and integration tests for Gate 3 Baseline Pipeline & Core Algorithms.
"""

import math
from datetime import datetime, timezone
import pytest
from src.characterization.geometry import SlickGeometryExtractor
from src.detection.lookalike import LookalikeDetector
from src.drift.lagrangian import LagrangianDriftEngine
from src.drift.origin_surface import OriginSurfaceEstimator
from src.ingestion.loader import ForensicDataLoader
from src.attribution.baseline import BaselineAttributionPipeline


def test_slick_geometry_extractor():
    # Unit square around (10.0, 10.0) with edge length ~11.13 km (0.1 deg)
    square_ring = [
        (9.95, 9.95),
        (10.05, 9.95),
        (10.05, 10.05),
        (9.95, 10.05),
        (9.95, 9.95)
    ]
    centroid = SlickGeometryExtractor.compute_polygon_centroid(square_ring)
    assert abs(centroid.latitude - 10.0) < 0.001
    assert abs(centroid.longitude - 10.0) < 0.001

    area = SlickGeometryExtractor.compute_polygon_area_km2(square_ring)
    assert area > 100.0  # ~11.13 * 11.13 ~ 124 km^2

    perimeter = SlickGeometryExtractor.compute_polygon_perimeter_km(square_ring)
    assert perimeter > 40.0  # ~4 * 11.13 ~ 44.5 km

    spill = SlickGeometryExtractor.characterize_polygon(
        spill_id="TEST_001",
        scene_id="SCENE_001",
        ring=square_ring,
        confidence=0.9
    )
    assert spill.spill_id == "TEST_001"
    assert spill.area_km2 == round(area, 2)


def test_lagrangian_backward_drift():
    drift_engine = LagrangianDriftEngine(dt_seconds=300.0)
    met = ForensicDataLoader.load_metocean_json("data/synthetic/metocean.json")
    start_pt = (72.276, 15.452)  # Observed slick centroid

    sim = drift_engine.run_simulation(
        seed_points=[start_pt] * 10,
        start_time=met.timestamp,
        duration_hours=6.0,
        metocean=met,
        backward=True,
        random_seed=42
    )

    term_cent = sim["terminal_centroid"]
    # Net drift was ~+8.16 km East, -5.31 km South.
    # In reverse (-dt), terminal centroid should be Northwest around (15.50 deg N, 72.20 deg E)
    assert abs(term_cent["latitude"] - 15.50) < 0.03
    assert abs(term_cent["longitude"] - 72.20) < 0.03


def test_origin_surface_estimator():
    pts = [
        (72.20 + 0.01 * math.cos(a), 15.50 + 0.01 * math.sin(a))
        for a in range(20)
    ]
    t0 = datetime(2024, 5, 10, 10, 0, tzinfo=timezone.utc)
    t1 = datetime(2024, 5, 10, 16, 0, tzinfo=timezone.utc)

    grid = OriginSurfaceEstimator.estimate_surface(
        terminal_points=pts,
        start_time=t0,
        end_time=t1,
        grid_resolution=30
    )

    matrix = grid.probability_matrix
    total_mass = sum(sum(row) for row in matrix)
    assert abs(total_mass - 1.0) < 1e-4
    assert grid.contour_geojson is not None
    assert len(grid.contour_geojson["features"]) == 3


def test_lookalike_detector():
    spill = ForensicDataLoader.load_slick_geojson("data/synthetic/detected_slick.geojson")
    met = ForensicDataLoader.load_metocean_json("data/synthetic/metocean.json")

    # Under standard 5 m/s wind, lookalike risk should be low
    res = LookalikeDetector.evaluate_lookalike_risk(spill, met)
    assert res["lookalike_risk_score"] < 0.40
    assert res["is_lookalike_suspected"] is False

    # Simulate calm low-wind conditions (1.5 m/s)
    met_calm = met.model_copy(update={"u_wind10_ms": 1.2, "v_wind10_ms": 0.8})
    res_calm = LookalikeDetector.evaluate_lookalike_risk(spill, met_calm)
    assert res_calm["lookalike_risk_score"] >= 0.50
    assert res_calm["is_lookalike_suspected"] is True
    assert any("LOW_WIND" in flag for flag in res_calm["flags"])


def test_baseline_pipeline_end_to_end():
    spill = ForensicDataLoader.load_slick_geojson("data/synthetic/detected_slick.geojson")
    met = ForensicDataLoader.load_metocean_json("data/synthetic/metocean.json")
    tracks = ForensicDataLoader.load_ais_csv("data/synthetic/vessel_traffic.csv")

    pipeline = BaselineAttributionPipeline()
    result = pipeline.run(
        spill=spill,
        metocean=met,
        tracks=tracks,
        hindcast_hours=6.0,
        num_seed_particles=30
    )

    assert result["pipeline"] == "BASELINE_HEURISTIC"
    assert result["total_candidates_evaluated"] >= 1
    assert result["top_candidate"] is not None

    ranked = result["ranked_vessels"]
    assert len(ranked) >= 2

    # Verify scores are bounded [0, 1]
    for r in ranked:
        assert 0.0 <= r["baseline_score"] <= 1.0

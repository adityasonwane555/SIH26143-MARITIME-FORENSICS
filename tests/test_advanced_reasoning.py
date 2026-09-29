"""
Unit and integration tests for Gate 4: Advanced Forensic Reasoning Engine.
Tests Multi-Hypothesis Generation, Bidirectional Evidence Fusion,
Counterfactual Forward Simulation, and Adversarial Falsification Attacks.
"""

from datetime import datetime, timezone
import pytest

from src.ingestion.loader import ForensicDataLoader
from src.drift.lagrangian import LagrangianDriftEngine
from src.drift.origin_surface import OriginSurfaceEstimator
from src.ais.filter import AISCorridorFilter
from src.hypotheses.generator import HypothesisGenerator
from src.evidence.aggregator import EvidenceAggregator
from src.counterfactual.simulator import CounterfactualSimulator
from src.falsification.attacks import AdversarialFalsificationEngine
from src.detection.lookalike import LookalikeDetector
from src.config.schemas import HypothesisType, DirectionEnum


@pytest.fixture
def benchmark_data():
    spill = ForensicDataLoader.load_slick_geojson("data/synthetic/detected_slick.geojson")
    met = ForensicDataLoader.load_metocean_json("data/synthetic/metocean.json")
    tracks = ForensicDataLoader.load_ais_csv("data/synthetic/vessel_traffic.csv")

    drift_engine = LagrangianDriftEngine(dt_seconds=300.0)
    sim = drift_engine.run_simulation(
        seed_points=spill.coordinates[0][:30],
        start_time=met.timestamp,
        duration_hours=6.0,
        metocean=met,
        backward=True,
        random_seed=42
    )

    from datetime import timedelta
    t_start = met.timestamp - timedelta(hours=sim["duration_hours"])
    origin_grid = OriginSurfaceEstimator.estimate_surface(
        terminal_points=sim["terminal_points"],
        start_time=t_start,
        end_time=met.timestamp,
        grid_resolution=30
    )

    candidates = AISCorridorFilter.filter_candidates(tracks, origin_grid, spatial_buffer_km=25.0)
    lookalike_info = LookalikeDetector.evaluate_lookalike_risk(spill, met)

    return {
        "spill": spill,
        "metocean": met,
        "tracks": tracks,
        "origin_grid": origin_grid,
        "candidates": candidates,
        "lookalike_info": lookalike_info
    }


def test_hypothesis_generation(benchmark_data):
    candidates = benchmark_data["candidates"]
    spill = benchmark_data["spill"]

    hypotheses = HypothesisGenerator.generate_hypotheses(
        candidate_vessels=candidates,
        spill=spill,
        lookalike_risk_score=0.1
    )

    assert len(hypotheses) >= 5
    types = [h.type for h in hypotheses]
    assert HypothesisType.VESSEL in types
    assert HypothesisType.FALSE_POSITIVE in types
    assert HypothesisType.NATURAL_SEEP in types
    assert HypothesisType.DARK_VESSEL in types

    total_prior = sum(h.prior_probability for h in hypotheses)
    assert abs(total_prior - 1.0) < 0.01


def test_evidence_aggregation(benchmark_data):
    candidates = benchmark_data["candidates"]
    spill = benchmark_data["spill"]
    met = benchmark_data["metocean"]
    origin_grid = benchmark_data["origin_grid"]
    lookalike = benchmark_data["lookalike_info"]

    hypotheses = HypothesisGenerator.generate_hypotheses(candidates, spill, lookalike["lookalike_risk_score"])
    cand_by_mmsi = {c["mmsi"]: c for c in candidates}

    # Evaluate Alpha (True source)
    h_alpha = next(h for h in hypotheses if h.subject_id == "419000111")
    EvidenceAggregator.evaluate_hypothesis_evidence(h_alpha, cand_by_mmsi["419000111"], spill, met, origin_grid, lookalike)
    assert len(h_alpha.supporting_evidence) > 0
    assert any(e.type == "spatial_origin_proximity" for e in h_alpha.supporting_evidence)

    # Evaluate Gamma (Upstream conflicting ship with AIS gap)
    h_gamma = next(h for h in hypotheses if h.subject_id == "419000333")
    EvidenceAggregator.evaluate_hypothesis_evidence(h_gamma, cand_by_mmsi["419000333"], spill, met, origin_grid, lookalike)
    assert len(h_gamma.contradicting_evidence) > 0
    assert any("upstream" in e.explanation.lower() or "divergent" in e.explanation.lower() for e in h_gamma.contradicting_evidence)
    assert any("gap" in e.explanation.lower() for e in h_gamma.contradicting_evidence)


def test_counterfactual_simulation(benchmark_data):
    spill = benchmark_data["spill"]
    met = benchmark_data["metocean"]
    candidates = benchmark_data["candidates"]
    cand_by_mmsi = {c["mmsi"]: c for c in candidates}

    sim = CounterfactualSimulator(dt_seconds=300.0)

    # Alpha: released at 10:00 UTC at (72.20, 15.50) -> should match observed slick at 16:00 UTC
    alpha_pt = cand_by_mmsi["419000111"]["closest_point"]
    cf_alpha = sim.evaluate_counterfactual(
        candidate_release_coord=(alpha_pt["longitude"], alpha_pt["latitude"]),
        candidate_release_time=datetime.fromisoformat(alpha_pt["timestamp"]),
        satellite_time=met.timestamp,
        observed_spill=spill,
        metocean=met
    )
    assert cf_alpha["is_feasible"] is True
    assert cf_alpha["centroid_error_km"] < 2.5
    assert cf_alpha["counterfactual_consistency_score"] >= 0.40
    assert cf_alpha["survives_counterfactual"] is True

    # Beta: passed at 15:30 UTC -> 30 mins before satellite pass. Cannot reproduce drifted slick!
    beta_pt = cand_by_mmsi["419000222"]["closest_point"]
    cf_beta = sim.evaluate_counterfactual(
        candidate_release_coord=(beta_pt["longitude"], beta_pt["latitude"]),
        candidate_release_time=datetime.fromisoformat(beta_pt["timestamp"]),
        satellite_time=met.timestamp,
        observed_spill=spill,
        metocean=met
    )
    assert cf_beta["is_feasible"] is True
    # In 30 mins, oil only drifts ~0.6 km, but slick was observed 8 km away from origin!
    # Centroid error will be large and IoU low
    assert cf_beta["centroid_error_km"] > 3.0 or cf_beta["counterfactual_consistency_score"] < 0.40


def test_adversarial_falsification_attacks(benchmark_data):
    spill = benchmark_data["spill"]
    met = benchmark_data["metocean"]
    origin_grid = benchmark_data["origin_grid"]
    candidates = benchmark_data["candidates"]
    cand_by_mmsi = {c["mmsi"]: c for c in candidates}

    engine = AdversarialFalsificationEngine(dt_seconds=300.0)
    hypotheses = HypothesisGenerator.generate_hypotheses(candidates, spill)

    # Attack Alpha (True polluter)
    h_alpha = next(h for h in hypotheses if h.subject_id == "419000111")
    res_alpha = engine.attack_hypothesis(h_alpha, cand_by_mmsi["419000111"], spill, met, origin_grid)
    assert res_alpha.survives is True
    assert res_alpha.challenges_failed == 0
    assert h_alpha.is_falsified is False

    # Attack Gamma (Upstream vessel with gap)
    h_gamma = next(h for h in hypotheses if h.subject_id == "419000333")
    res_gamma = engine.attack_hypothesis(h_gamma, cand_by_mmsi["419000333"], spill, met, origin_grid)
    assert res_gamma.survives is False
    assert res_gamma.challenges_failed >= 1
    assert any("HYDRODYNAMIC_FAILURE" in r for r in res_gamma.contradicting_reasons)
    assert h_gamma.is_falsified is True

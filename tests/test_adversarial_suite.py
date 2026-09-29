"""
SIH26143 — Comprehensive 10-Scenario Adversarial Test Suite.
Tests the system's stability, falsification capability, and abstention robustness
across the 10 adversarial stress scenarios specified in Section 54 of the Master Specification.
"""

from datetime import datetime, timezone
import pytest

from src.config.schemas import (
    Hypothesis,
    HypothesisType,
    AttributionDecision,
    DirectionEnum,
    EvidenceItem
)
from src.uncertainty.abstention import AbstentionEngine
from src.uncertainty.entropy import UncertaintyQuantifier


def test_scenario_1_single_obvious_candidate():
    """Scenario 1: Single obvious candidate with strong evidence -> must attribute."""
    h1 = Hypothesis(
        hypothesis_id="H1", type=HypothesisType.VESSEL, subject_id="V1", subject_name="MV Solo Polluter",
        prior_probability=0.5,
        supporting_evidence=[
            EvidenceItem(evidence_id="E1", hypothesis_id="H1", type="spatial", value=0.95, direction=DirectionEnum.SUPPORTS, source="AIS", confidence=0.95, explanation="Passed through origin.")
        ],
        is_falsified=False
    )
    h_fp = Hypothesis(hypothesis_id="H_FP", type=HypothesisType.FALSE_POSITIVE, subject_id="FP", subject_name="Lookalike", prior_probability=0.5)

    posteriors = UncertaintyQuantifier.compute_posteriors([h1, h_fp])
    res = AbstentionEngine.evaluate_attribution_decision(posteriors)
    assert res["decision"] == AttributionDecision.ATTRIBUTED
    assert res["leading_hypothesis"].subject_id == "V1"


def test_scenario_2_two_equally_plausible_vessels():
    """Scenario 2: Two equally plausible vessels with zero separating margin -> MUST ABSTAIN."""
    h1 = Hypothesis(hypothesis_id="H1", type=HypothesisType.VESSEL, subject_id="V1", subject_name="Ship A", prior_probability=0.45, posterior_probability=0.46, is_falsified=False)
    h2 = Hypothesis(hypothesis_id="H2", type=HypothesisType.VESSEL, subject_id="V2", subject_name="Ship B", prior_probability=0.45, posterior_probability=0.45, is_falsified=False)
    h_fp = Hypothesis(hypothesis_id="H_FP", type=HypothesisType.FALSE_POSITIVE, subject_id="FP", subject_name="Lookalike", prior_probability=0.10, posterior_probability=0.09)

    res = AbstentionEngine.evaluate_attribution_decision([h1, h2, h_fp])
    assert res["decision"] == AttributionDecision.INSUFFICIENT_EVIDENCE
    assert res["is_abstention"] is True


def test_scenario_3_three_nearby_vessels_one_consistent():
    """Scenario 3: Three nearby vessels but only one survives falsification -> attributes consistent one."""
    h1 = Hypothesis(hypothesis_id="H1", type=HypothesisType.VESSEL, subject_id="V1", subject_name="Ship Consistent", prior_probability=0.3, is_falsified=False)
    h2 = Hypothesis(hypothesis_id="H2", type=HypothesisType.VESSEL, subject_id="V2", subject_name="Ship Upstream", prior_probability=0.3, is_falsified=True)
    h3 = Hypothesis(hypothesis_id="H3", type=HypothesisType.VESSEL, subject_id="V3", subject_name="Ship Wrong Time", prior_probability=0.3, is_falsified=True)

    # h1 receives supporting evidence
    h1.supporting_evidence.append(EvidenceItem(
        evidence_id="E1", hypothesis_id="H1", type="drift", value=0.9, direction=DirectionEnum.SUPPORTS, source="Metocean", confidence=0.9, explanation="Consistent"
    ))

    posteriors = UncertaintyQuantifier.compute_posteriors([h1, h2, h3])
    res = AbstentionEngine.evaluate_attribution_decision(posteriors)
    assert res["decision"] == AttributionDecision.ATTRIBUTED
    assert res["leading_hypothesis"].subject_id == "V1"


def test_scenario_4_ais_gap():
    """Scenario 4: Vessel with severe AIS transponder gap receives contradicting evidence."""
    from src.evidence.aggregator import EvidenceAggregator
    from src.config.schemas import SpillPolygon, MetoceanObservation, OriginProbabilityGrid, BoundingBox, GeoPoint

    spill = SpillPolygon(
        spill_id="S1", scene_id="SC1", coordinates=[[(72.0, 15.0), (72.1, 15.0), (72.1, 15.1), (72.0, 15.1), (72.0, 15.0)]],
        area_km2=2.0, perimeter_km=8.0, centroid=GeoPoint(latitude=15.05, longitude=72.05),
        major_axis_len_km=2.0, minor_axis_len_km=1.0, orientation_deg=90.0, elongation=2.0, confidence=0.9
    )
    met = MetoceanObservation(
        timestamp=datetime.now(timezone.utc), grid_bounds=BoundingBox(min_lat=14.0, max_lat=16.0, min_lon=71.0, max_lon=73.0),
        u_current_ms=0.1, v_current_ms=0.0, u_wind10_ms=2.0, v_wind10_ms=0.0
    )
    origin_grid = OriginProbabilityGrid(
        grid_id="G1", timestamp_evaluated=datetime.now(timezone.utc), bounds=met.grid_bounds,
        resolution_lat=0.1, resolution_lon=0.1, probability_matrix=[[0.5]], estimated_centroid=GeoPoint(latitude=15.0, longitude=72.0),
        estimated_release_window=(datetime.now(timezone.utc), datetime.now(timezone.utc))
    )

    cand_meta = {
        "min_distance_km": 1.2,
        "closest_point": {"timestamp": datetime.now(timezone.utc).isoformat(), "latitude": 15.0, "longitude": 72.0, "sog_knots": 12.0, "cog_degrees": 90.0},
        "has_ais_gaps": True,
        "max_gap_minutes": 240.0
    }

    h = Hypothesis(hypothesis_id="H_GAP", type=HypothesisType.VESSEL, subject_id="V_GAP", subject_name="Gap Ship", prior_probability=0.5)
    EvidenceAggregator.evaluate_hypothesis_evidence(h, cand_meta, spill, met, origin_grid, {"lookalike_risk_score": 0.1})

    assert any(e.type == "ais_data_discontinuity" for e in h.contradicting_evidence)


def test_scenario_5_lookalike_low_wind():
    """Scenario 5: Meteorological look-alike in low wind -> flags FALSE_POSITIVE."""
    h_fp = Hypothesis(hypothesis_id="H_FP", type=HypothesisType.FALSE_POSITIVE, subject_id="FP", subject_name="Calm Sea Look-alike", prior_probability=0.75, posterior_probability=0.85)
    h_v = Hypothesis(hypothesis_id="H1", type=HypothesisType.VESSEL, subject_id="V1", subject_name="Innocent Ship", prior_probability=0.25, posterior_probability=0.15)

    res = AbstentionEngine.evaluate_attribution_decision([h_fp, h_v])
    assert res["decision"] == AttributionDecision.FALSE_POSITIVE


def test_scenario_6_non_vessel_source():
    """Scenario 6: Offshore infrastructure or natural seep is leading -> attributes NON_VESSEL_SOURCE."""
    h_seep = Hypothesis(hypothesis_id="H_SEEP", type=HypothesisType.NATURAL_SEEP, subject_id="SEEP_1", subject_name="Active Hydrocarbon Seep", prior_probability=0.6, posterior_probability=0.75)
    h_v = Hypothesis(hypothesis_id="H_V", type=HypothesisType.VESSEL, subject_id="V1", subject_name="Passing Ship", prior_probability=0.4, posterior_probability=0.25)

    res = AbstentionEngine.evaluate_attribution_decision([h_seep, h_v])
    assert res["decision"] == AttributionDecision.NON_VESSEL_SOURCE


def test_scenario_7_conflicting_environmental_data():
    """Scenario 7: Conflicting evidence produces high entropy -> triggers abstention."""
    # When evidence contradicts all candidates, posterior remains diffuse
    h_diffuse = [
        Hypothesis(hypothesis_id=f"H{i}", type=HypothesisType.VESSEL, subject_id=f"V{i}", subject_name=f"Ship {i}", prior_probability=0.2, posterior_probability=0.20)
        for i in range(5)
    ]
    res = AbstentionEngine.evaluate_attribution_decision(h_diffuse)
    assert res["decision"] == AttributionDecision.INSUFFICIENT_EVIDENCE
    assert res["is_abstention"] is True


def test_scenario_8_no_plausible_vessel_candidate():
    """Scenario 8: No plausible candidate in corridor -> abstains or attributes dark vessel."""
    h_dark = Hypothesis(hypothesis_id="H_DARK", type=HypothesisType.DARK_VESSEL, subject_id="DARK", subject_name="Untracked Dark Vessel", prior_probability=0.5, posterior_probability=0.60)
    h_fp = Hypothesis(hypothesis_id="H_FP", type=HypothesisType.FALSE_POSITIVE, subject_id="FP", subject_name="Lookalike", prior_probability=0.5, posterior_probability=0.40)

    res = AbstentionEngine.evaluate_attribution_decision([h_dark, h_fp])
    # When dark vessel leads without definitive evidence, margin is small or entropy high -> abstains safely
    assert res["is_abstention"] is True


def test_scenario_9_falsified_candidates_suppression():
    """Scenario 9: Candidate vessels fail counterfactuals -> posteriors penalized by 95%."""
    h_falsified = Hypothesis(hypothesis_id="H1", type=HypothesisType.VESSEL, subject_id="V1", subject_name="Ship Fails", prior_probability=0.5, is_falsified=True)
    h_other = Hypothesis(hypothesis_id="H2", type=HypothesisType.DARK_VESSEL, subject_id="DARK", subject_name="Dark Ship", prior_probability=0.5, is_falsified=False)

    posteriors = UncertaintyQuantifier.compute_posteriors([h_falsified, h_other])
    p_falsified = next(h.posterior_probability for h in posteriors if h.hypothesis_id == "H1")
    p_other = next(h.posterior_probability for h in posteriors if h.hypothesis_id == "H2")
    assert p_falsified < 0.10
    assert p_other > 0.90


def test_scenario_10_calibrated_decision_stability():
    """Scenario 10: Empty hypotheses list -> safely returns INSUFFICIENT_EVIDENCE without crash."""
    res = AbstentionEngine.evaluate_attribution_decision([])
    assert res["decision"] == AttributionDecision.INSUFFICIENT_EVIDENCE
    assert res["is_abstention"] is True

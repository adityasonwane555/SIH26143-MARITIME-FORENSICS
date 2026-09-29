"""
Unit and integration tests for Gate 5 (Uncertainty & Abstention) and Gate 6 (Active Sensing & Information Gain).
"""

from datetime import datetime, timezone
import pytest

from src.config.schemas import (
    Hypothesis,
    HypothesisType,
    AttributionDecision,
    OriginProbabilityGrid,
    BoundingBox,
    GeoPoint
)
from src.uncertainty.entropy import UncertaintyQuantifier
from src.uncertainty.abstention import AbstentionEngine
from src.evidence_selection.info_gain import ActiveSensingEngine


@pytest.fixture
def mock_origin_grid():
    bbox = BoundingBox(min_lat=15.0, max_lat=16.0, min_lon=72.0, max_lon=73.0)
    return OriginProbabilityGrid(
        grid_id="GRID_TEST",
        timestamp_evaluated=datetime.now(timezone.utc),
        bounds=bbox,
        resolution_lat=0.02,
        resolution_lon=0.02,
        probability_matrix=[[0.1, 0.2], [0.3, 0.4]],
        estimated_centroid=GeoPoint(latitude=15.5, longitude=72.5),
        estimated_release_window=(datetime.now(timezone.utc), datetime.now(timezone.utc))
    )


def test_uncertainty_quantifier_entropy():
    # 4 hypotheses with uniform probability -> normalized entropy should be 1.0
    h_uniform = [
        Hypothesis(hypothesis_id=f"H{i}", type=HypothesisType.VESSEL, subject_id=f"V{i}", subject_name=f"Ship {i}", prior_probability=0.25, posterior_probability=0.25)
        for i in range(4)
    ]
    stats_u = UncertaintyQuantifier.compute_shannon_entropy(h_uniform)
    assert abs(stats_u["normalized_entropy"] - 1.0) < 0.01
    assert abs(stats_u["entropy_bits"] - 2.0) < 0.01  # log2(4) = 2.0

    # 1 dominant hypothesis (0.97) -> normalized entropy should be close to 0
    h_dominant = [
        Hypothesis(hypothesis_id="H0", type=HypothesisType.VESSEL, subject_id="V0", subject_name="Ship 0", prior_probability=0.25, posterior_probability=0.97),
        Hypothesis(hypothesis_id="H1", type=HypothesisType.VESSEL, subject_id="V1", subject_name="Ship 1", prior_probability=0.25, posterior_probability=0.01),
        Hypothesis(hypothesis_id="H2", type=HypothesisType.VESSEL, subject_id="V2", subject_name="Ship 2", prior_probability=0.25, posterior_probability=0.01),
        Hypothesis(hypothesis_id="H3", type=HypothesisType.VESSEL, subject_id="V3", subject_name="Ship 3", prior_probability=0.25, posterior_probability=0.01)
    ]
    stats_d = UncertaintyQuantifier.compute_shannon_entropy(h_dominant)
    assert stats_d["normalized_entropy"] < 0.20


def test_abstention_engine_clear_winner():
    h_clear = [
        Hypothesis(hypothesis_id="H1", type=HypothesisType.VESSEL, subject_id="V1", subject_name="True Ship", prior_probability=0.2, posterior_probability=0.75, is_falsified=False),
        Hypothesis(hypothesis_id="H2", type=HypothesisType.VESSEL, subject_id="V2", subject_name="Decoy Ship", prior_probability=0.2, posterior_probability=0.15, is_falsified=True),
        Hypothesis(hypothesis_id="H3", type=HypothesisType.FALSE_POSITIVE, subject_id="FP", subject_name="Lookalike", prior_probability=0.2, posterior_probability=0.10)
    ]
    decision = AbstentionEngine.evaluate_attribution_decision(h_clear)
    assert decision["decision"] == AttributionDecision.ATTRIBUTED
    assert decision["is_abstention"] is False
    assert decision["leading_hypothesis"].subject_name == "True Ship"


def test_abstention_engine_ambiguous_margin():
    # Two ships with near identical probability (0.42 vs 0.40) -> MUST ABSTAIN!
    h_ambiguous = [
        Hypothesis(hypothesis_id="H1", type=HypothesisType.VESSEL, subject_id="V1", subject_name="Ship A", prior_probability=0.2, posterior_probability=0.42, is_falsified=False),
        Hypothesis(hypothesis_id="H2", type=HypothesisType.VESSEL, subject_id="V2", subject_name="Ship B", prior_probability=0.2, posterior_probability=0.40, is_falsified=False),
        Hypothesis(hypothesis_id="H3", type=HypothesisType.FALSE_POSITIVE, subject_id="FP", subject_name="Lookalike", prior_probability=0.2, posterior_probability=0.18)
    ]
    decision = AbstentionEngine.evaluate_attribution_decision(h_ambiguous)
    assert decision["decision"] == AttributionDecision.INSUFFICIENT_EVIDENCE
    assert decision["is_abstention"] is True
    assert decision["leading_hypothesis"].subject_name == "Ship A"


def test_abstention_engine_falsified_leader():
    # When candidate vessel is falsified and no viable candidate remains -> MUST ABSTAIN!
    h_falsified = [
        Hypothesis(hypothesis_id="H1", type=HypothesisType.VESSEL, subject_id="V1", subject_name="Disproven Ship 1", prior_probability=0.2, posterior_probability=0.60, is_falsified=True),
        Hypothesis(hypothesis_id="H2", type=HypothesisType.VESSEL, subject_id="V2", subject_name="Disproven Ship 2", prior_probability=0.2, posterior_probability=0.40, is_falsified=True)
    ]
    decision = AbstentionEngine.evaluate_attribution_decision(h_falsified)
    assert decision["decision"] == AttributionDecision.INSUFFICIENT_EVIDENCE
    assert decision["is_abstention"] is True


def test_active_sensing_recommendations(mock_origin_grid):
    from src.config.schemas import EvidenceItem, DirectionEnum
    h1 = Hypothesis(hypothesis_id="H1", type=HypothesisType.VESSEL, subject_id="V1", subject_name="Ship A", prior_probability=0.3, posterior_probability=0.55)
    h2 = Hypothesis(hypothesis_id="H2", type=HypothesisType.VESSEL, subject_id="V2", subject_name="Ship B", prior_probability=0.3, posterior_probability=0.35)
    # Add an AIS gap evidence to h2
    h2.contradicting_evidence.append(EvidenceItem(
        evidence_id="EV_GAP", hypothesis_id="H2", type="ais_gap", value=0.8,
        direction=DirectionEnum.REFUTES, source="AIS", confidence=0.8, explanation="Vessel had an AIS transmission gap of 150 minutes."
    ))

    recs = ActiveSensingEngine.recommend_next_evidence([h1, h2], mock_origin_grid)
    assert len(recs) >= 2
    # Verify recommended actions are ranked by Expected Information Gain descending
    for i in range(len(recs) - 1):
        assert recs[i].expected_information_gain_bits >= recs[i + 1].expected_information_gain_bits

    # Since Ship B has an AIS gap, SATELLITE_AIS_DEEP_ANALYTICS should be recommended
    action_types = [r.action_type for r in recs]
    assert "SATELLITE_AIS_DEEP_ANALYTICS" in action_types

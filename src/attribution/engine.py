"""
SIH26143 — Master Forensic Intelligence & Attribution Engine.
Executes the closed-loop investigative workflow:
Observe -> Detect -> Characterize -> Hindcast -> Hypotheses -> Evidence ->
Falsify -> Counterfactual -> Uncertainty -> Abstain/Attribute -> Active Sensing.
"""

from datetime import datetime, timezone
from typing import List, Dict, Any, Optional

from src.config.schemas import (
    SpillPolygon,
    MetoceanObservation,
    AISTrack,
    ForensicDossier,
    GeoPoint,
    AttributionDecision
)
from src.detection.lookalike import LookalikeDetector
from src.drift.lagrangian import LagrangianDriftEngine
from src.drift.origin_surface import OriginSurfaceEstimator
from src.ais.filter import AISCorridorFilter
from src.hypotheses.generator import HypothesisGenerator
from src.evidence.aggregator import EvidenceAggregator
from src.falsification.attacks import AdversarialFalsificationEngine
from src.uncertainty.entropy import UncertaintyQuantifier
from src.uncertainty.abstention import AbstentionEngine
from src.evidence_selection.info_gain import ActiveSensingEngine


class ForensicAttributionEngine:
    """Master orchestrator for explainable maritime forensic intelligence."""

    def __init__(self, dt_seconds: float = 300.0):
        self.dt_seconds = dt_seconds
        self.drift_engine = LagrangianDriftEngine(dt_seconds=dt_seconds)
        self.falsification_engine = AdversarialFalsificationEngine(dt_seconds=dt_seconds)

    def run_investigation(
        self,
        incident_id: str,
        title: str,
        spill: SpillPolygon,
        metocean: MetoceanObservation,
        tracks: List[AISTrack],
        hindcast_hours: float = 6.0,
        num_seed_particles: int = 40,
        known_infrastructure: Optional[List[Dict[str, Any]]] = None
    ) -> ForensicDossier:
        """
        Executes the complete forensic loop and returns an audit-ready ForensicDossier.
        """
        start_time = datetime.now(timezone.utc)

        # 1. Look-alike meteorological defense
        lookalike_info = LookalikeDetector.evaluate_lookalike_risk(spill, metocean)

        # 2. Reverse hydrodynamic drift hindcast
        ring = spill.coordinates[0]
        step = max(1, len(ring) // num_seed_particles)
        seed_points = ring[::step][:num_seed_particles]

        sim_result = self.drift_engine.run_simulation(
            seed_points=seed_points,
            start_time=metocean.timestamp,
            duration_hours=hindcast_hours,
            metocean=metocean,
            backward=True,
            random_seed=42
        )

        # 3. 2D Origin Probability Surface
        from datetime import timedelta
        t_release_start = metocean.timestamp - timedelta(hours=hindcast_hours)
        origin_grid = OriginSurfaceEstimator.estimate_surface(
            terminal_points=sim_result["terminal_points"],
            start_time=t_release_start,
            end_time=metocean.timestamp,
            grid_resolution=40
        )

        # 4. Spatiotemporal AIS corridor filtering
        candidate_metadata_list = AISCorridorFilter.filter_candidates(
            tracks=tracks,
            origin_grid=origin_grid,
            spatial_buffer_km=20.0,
            temporal_buffer_hours=2.0
        )
        cand_by_mmsi = {c["mmsi"]: c for c in candidate_metadata_list}

        # 5. Multi-Hypothesis generation
        hypotheses = HypothesisGenerator.generate_hypotheses(
            candidate_vessels=candidate_metadata_list,
            spill=spill,
            lookalike_risk_score=lookalike_info["lookalike_risk_score"],
            known_infrastructure=known_infrastructure
        )

        # 6. Bidirectional evidence evaluation
        for hyp in hypotheses:
            cand_meta = cand_by_mmsi.get(hyp.subject_id)
            EvidenceAggregator.evaluate_hypothesis_evidence(
                hypothesis=hyp,
                candidate_metadata=cand_meta,
                spill=spill,
                metocean=metocean,
                origin_grid=origin_grid,
                lookalike_info=lookalike_info
            )

        # 7. Adversarial Falsification Attacks (including Counterfactual forward runs)
        for hyp in hypotheses:
            cand_meta = cand_by_mmsi.get(hyp.subject_id)
            self.falsification_engine.attack_hypothesis(
                hypothesis=hyp,
                candidate_metadata=cand_meta,
                spill=spill,
                metocean=metocean,
                origin_grid=origin_grid
            )

        # 8. Uncertainty calibration & Shannon entropy
        sorted_hypotheses = UncertaintyQuantifier.compute_posteriors(hypotheses)
        entropy_metrics = UncertaintyQuantifier.compute_shannon_entropy(sorted_hypotheses)

        # 9. Decision-Theoretic Attribution vs. Abstention
        decision_result = AbstentionEngine.evaluate_attribution_decision(sorted_hypotheses)

        # 10. Active Sensing / Next-Best-Evidence Recommendations
        recommendations = ActiveSensingEngine.recommend_next_evidence(
            hypotheses=sorted_hypotheses,
            origin_grid=origin_grid
        )

        exec_time_ms = (datetime.now(timezone.utc) - start_time).total_seconds() * 1000.0

        leading_hyp = decision_result.get("leading_hypothesis")
        leading_id = leading_hyp.hypothesis_id if leading_hyp else None
        leading_name = leading_hyp.subject_name if leading_hyp else None

        dossier = ForensicDossier(
            incident_id=incident_id,
            title=title,
            incident_time=metocean.timestamp,
            location=spill.centroid,
            decision=decision_result["decision"],
            leading_hypothesis_id=leading_id,
            leading_subject_name=leading_name,
            attribution_confidence=round(decision_result["confidence"], 4),
            entropy_bits=entropy_metrics["entropy_bits"],
            is_abstention=decision_result["is_abstention"],
            abstention_reason=decision_result.get("reason"),
            hypotheses=sorted_hypotheses,
            origin_estimate=origin_grid,
            detected_slick=spill,
            recommended_evidence=recommendations,
            audit_trail={
                "engine_version": "1.0.0",
                "execution_time_ms": round(exec_time_ms, 2),
                "hindcast_hours": hindcast_hours,
                "num_candidates_screened": len(candidate_metadata_list),
                "lookalike_analysis": lookalike_info,
                "normalized_entropy": entropy_metrics["normalized_entropy"]
            }
        )

        return dossier

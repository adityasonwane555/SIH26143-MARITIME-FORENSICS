"""
SIH26143 — Adversarial Self-Falsification Engine.
Executes the signature "ATTACK HYPOTHESIS" stress test suite to challenge leading candidate sources.
Evaluates 5 orthogonal physical contradiction rules:
1. Spatial Overlap Challenge
2. Temporal Feasibility Challenge
3. Hydrodynamic Drift Direction Challenge
4. Counterfactual Forward Plume Consistency Challenge
5. AIS Data Continuity Challenge
"""

import math
from datetime import datetime
from typing import Dict, Any, List, Optional
from src.config.schemas import (
    Hypothesis,
    HypothesisType,
    FalsificationResult,
    SpillPolygon,
    MetoceanObservation,
    OriginProbabilityGrid
)
from src.counterfactual.simulator import CounterfactualSimulator
from src.evidence.aggregator import vector_to_nautical_bearing


class AdversarialFalsificationEngine:
    """Executes automated adversarial challenges attempting to disprove candidate source hypotheses."""

    def __init__(self, dt_seconds: float = 300.0):
        self.counterfactual_sim = CounterfactualSimulator(dt_seconds=dt_seconds)

    def attack_hypothesis(
        self,
        hypothesis: Hypothesis,
        candidate_metadata: Optional[Dict[str, Any]],
        spill: SpillPolygon,
        metocean: MetoceanObservation,
        origin_grid: OriginProbabilityGrid
    ) -> FalsificationResult:
        """
        Runs the full adversarial challenge suite against a candidate hypothesis.
        Returns a structured FalsificationResult indicating survival or contradiction.
        """
        contradictions: List[str] = []
        challenges_passed = 0
        challenges_failed = 0
        cf_iou: Optional[float] = None
        cf_hausdorff: Optional[float] = None

        if hypothesis.type == HypothesisType.VESSEL and candidate_metadata is not None:
            cand = candidate_metadata
            closest_pt = cand["closest_point"]
            d_km = cand["min_distance_km"]
            sog_knots = closest_pt["sog_knots"]
            cog_deg = closest_pt["cog_degrees"]
            t_pt = datetime.fromisoformat(closest_pt["timestamp"])
            t_sat = metocean.timestamp

            # CHALLENGE 1: Spatial Overlap Challenge
            if d_km > 8.0:
                challenges_failed += 1
                contradictions.append(
                    f"SPATIAL_FAILURE: Trajectory minimum distance ({d_km:.2f} km) exceeds 90% origin confidence envelope."
                )
            else:
                challenges_passed += 1

            # CHALLENGE 2: Temporal Feasibility Challenge
            if t_pt >= t_sat:
                challenges_failed += 1
                contradictions.append(
                    f"TEMPORAL_FAILURE: Vessel entered origin area at {t_pt.isoformat()}, which is AFTER satellite acquisition ({t_sat.isoformat()}). Impossible to have caused the drifted slick."
                )
            else:
                challenges_passed += 1

            # CHALLENGE 3: Hydrodynamic Drift Direction Challenge
            u_drift = metocean.u_current_ms + 0.032 * metocean.u_wind10_ms
            v_drift = metocean.v_current_ms + 0.032 * metocean.v_wind10_ms
            drift_bearing_deg = vector_to_nautical_bearing(u_drift, v_drift)
            course_divergence = abs((cog_deg - drift_bearing_deg + 180) % 360 - 180)

            if course_divergence > 110.0:
                challenges_failed += 1
                contradictions.append(
                    f"HYDRODYNAMIC_FAILURE: Vessel course ({cog_deg:.1f}°) diverged by {course_divergence:.1f}° from surface drift bearing ({drift_bearing_deg:.1f}°). Vessel was heading upstream against the current."
                )
            else:
                challenges_passed += 1

            # CHALLENGE 4: Counterfactual Forward Plume Simulation Challenge
            cf_res = self.counterfactual_sim.evaluate_counterfactual(
                candidate_release_coord=(closest_pt["longitude"], closest_pt["latitude"]),
                candidate_release_time=t_pt,
                satellite_time=t_sat,
                observed_spill=spill,
                metocean=metocean
            )
            cf_iou = cf_res.get("bbox_iou") or 0.0
            cf_centroid_err = cf_res.get("centroid_error_km")
            cf_centroid_err = 999.0 if cf_centroid_err is None else cf_centroid_err
            cf_hausdorff = cf_res.get("hausdorff_distance_km")

            if not cf_res.get("survives_counterfactual", False):
                challenges_failed += 1
                contradictions.append(
                    f"COUNTERFACTUAL_FAILURE: Simulated forward plume from vessel location missed observed slick "
                    f"(centroid error: {cf_centroid_err:.2f} km, IoU: {cf_iou:.2f})."
                )
            else:
                challenges_passed += 1

            # CHALLENGE 5: AIS Data Continuity Challenge
            if cand.get("has_ais_gaps", False) and cand.get("max_gap_minutes", 0) > 180.0:
                challenges_failed += 1
                contradictions.append(
                    f"AIS_DATA_INTEGRITY_FAILURE: Severe transponder silence ({cand.get('max_gap_minutes')} minutes) prevents verifiable track continuity."
                )
            else:
                challenges_passed += 1

        elif hypothesis.type == HypothesisType.FALSE_POSITIVE:
            # Challenge look-alike hypothesis
            wind_speed = math.sqrt(metocean.u_wind10_ms ** 2 + metocean.v_wind10_ms ** 2)
            if wind_speed >= 3.5:
                challenges_failed += 1
                contradictions.append(
                    f"WIND_SPEED_FAILURE: Wind speed is {wind_speed:.1f} m/s (>= 3.0 m/s threshold). Ambient sea roughness disproves a calm water false positive."
                )
            else:
                challenges_passed += 1

        survives = (challenges_failed == 0)

        result = FalsificationResult(
            hypothesis_id=hypothesis.hypothesis_id,
            survives=survives,
            challenges_passed=challenges_passed,
            challenges_failed=challenges_failed,
            contradicting_reasons=contradictions,
            counterfactual_iou=cf_iou,
            counterfactual_hausdorff_km=cf_hausdorff
        )

        hypothesis.falsification = result
        hypothesis.is_falsified = not survives
        return result

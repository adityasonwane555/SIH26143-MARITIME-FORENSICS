"""
SIH26143 — Bidirectional Evidence Aggregation Engine.
Evaluates supporting [+] and refuting [-] evidence across spatial, temporal,
hydrodynamic, kinematic, and meteorological dimensions for each candidate hypothesis.
"""

import math
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional

from src.config.schemas import (
    Hypothesis,
    HypothesisType,
    EvidenceItem,
    DirectionEnum,
    OriginProbabilityGrid,
    SpillPolygon,
    MetoceanObservation
)
from src.characterization.geometry import SlickGeometryExtractor


def vector_to_nautical_bearing(u_east: float, v_north: float) -> float:
    """
    Converts eastward (u) and northward (v) velocity components to nautical bearing [0, 360)
    where 0 = North, 90 = East, 180 = South, 270 = West.
    """
    bearing = math.degrees(math.atan2(u_east, v_north))
    return (bearing + 360.0) % 360.0


class EvidenceAggregator:
    """Evaluates and fuses bidirectional evidence for each hypothesis."""

    @classmethod
    def evaluate_hypothesis_evidence(
        cls,
        hypothesis: Hypothesis,
        candidate_metadata: Optional[Dict[str, Any]],
        spill: SpillPolygon,
        metocean: MetoceanObservation,
        origin_grid: OriginProbabilityGrid,
        lookalike_info: Dict[str, Any]
    ) -> Hypothesis:
        """
        Populates supporting_evidence and contradicting_evidence lists
        for a given hypothesis.
        """
        supporting: List[EvidenceItem] = []
        contradicting: List[EvidenceItem] = []

        now_utc = datetime.now(timezone.utc)

        # Net surface drift nautical bearing (direction water is moving towards)
        u_drift = metocean.u_current_ms + 0.032 * metocean.u_wind10_ms
        v_drift = metocean.v_current_ms + 0.032 * metocean.v_wind10_ms
        drift_bearing_deg = vector_to_nautical_bearing(u_drift, v_drift)

        if hypothesis.type == HypothesisType.VESSEL and candidate_metadata is not None:
            cand = candidate_metadata
            d_km = cand["min_distance_km"]
            pt = cand["closest_point"]
            sog_knots = pt["sog_knots"]
            cog_deg = pt["cog_degrees"]
            pt_ts = datetime.fromisoformat(pt["timestamp"])

            # 1. Spatial Overlap Evidence
            if d_km <= 2.0:
                supporting.append(EvidenceItem(
                    evidence_id=f"EV_SPAT_{hypothesis.hypothesis_id}",
                    hypothesis_id=hypothesis.hypothesis_id,
                    type="spatial_origin_proximity",
                    value=round(math.exp(-d_km / 5.0), 3),
                    direction=DirectionEnum.SUPPORTS,
                    source="AIS_vs_Origin_Surface",
                    confidence=0.92,
                    explanation=f"Vessel trajectory passed within {d_km:.2f} km of the reconstructed origin centroid.",
                    timestamp_evaluated=now_utc
                ))
            elif d_km > 10.0:
                contradicting.append(EvidenceItem(
                    evidence_id=f"EV_SPAT_REF_{hypothesis.hypothesis_id}",
                    hypothesis_id=hypothesis.hypothesis_id,
                    type="spatial_origin_conflict",
                    value=round(min(1.0, d_km / 25.0), 3),
                    direction=DirectionEnum.REFUTES,
                    source="AIS_vs_Origin_Surface",
                    confidence=0.85,
                    explanation=f"Vessel remained {d_km:.2f} km away from estimated origin, outside the 90% probability boundary.",
                    timestamp_evaluated=now_utc
                ))

            # 2. Hydrodynamic Course vs. Current Consistency
            # Nautical angular difference between vessel heading and drift bearing
            course_diff = abs((cog_deg - drift_bearing_deg + 180) % 360 - 180)
            if course_diff > 110.0:
                # Vessel was traveling UPSTREAM directly against current/drift!
                contradicting.append(EvidenceItem(
                    evidence_id=f"EV_DRIFT_UPSTREAM_{hypothesis.hypothesis_id}",
                    hypothesis_id=hypothesis.hypothesis_id,
                    type="hydrodynamic_drift_conflict",
                    value=round(min(1.0, course_diff / 180.0), 3),
                    direction=DirectionEnum.REFUTES,
                    source="Metocean_Kinematic_Coupling",
                    confidence=0.88,
                    explanation=(
                        f"Vessel heading ({cog_deg:.1f}°) was divergent ({course_diff:.1f}° difference) "
                        f"from the surface drift bearing ({drift_bearing_deg:.1f}°), indicating upstream movement inconsistent with slick deposition."
                    ),
                    timestamp_evaluated=now_utc
                ))
            elif course_diff < 50.0:
                supporting.append(EvidenceItem(
                    evidence_id=f"EV_DRIFT_ALIGN_{hypothesis.hypothesis_id}",
                    hypothesis_id=hypothesis.hypothesis_id,
                    type="hydrodynamic_drift_consistency",
                    value=round(1.0 - (course_diff / 50.0), 3),
                    direction=DirectionEnum.SUPPORTS,
                    source="Metocean_Kinematic_Coupling",
                    confidence=0.82,
                    explanation=f"Vessel course ({cog_deg:.1f}°) aligned with net surface drift bearing ({drift_bearing_deg:.1f}°).",
                    timestamp_evaluated=now_utc
                ))

            # 3. Kinematic Transit Feasibility
            if sog_knots < 1.0:
                contradicting.append(EvidenceItem(
                    evidence_id=f"EV_STATIONARY_{hypothesis.hypothesis_id}",
                    hypothesis_id=hypothesis.hypothesis_id,
                    type="kinematic_speed_conflict",
                    value=0.80,
                    direction=DirectionEnum.REFUTES,
                    source="AIS_Kinematics",
                    confidence=0.90,
                    explanation=f"Vessel was stationary (speed {sog_knots} knots), which contradicts an elongated trail slick.",
                    timestamp_evaluated=now_utc
                ))
            elif 8.0 <= sog_knots <= 22.0:
                supporting.append(EvidenceItem(
                    evidence_id=f"EV_CRUISE_{hypothesis.hypothesis_id}",
                    hypothesis_id=hypothesis.hypothesis_id,
                    type="kinematic_cruising_speed",
                    value=0.75,
                    direction=DirectionEnum.SUPPORTS,
                    source="AIS_Kinematics",
                    confidence=0.85,
                    explanation=f"Vessel transit speed ({sog_knots:.1f} knots) is standard cruising speed for en-route bilge discharges.",
                    timestamp_evaluated=now_utc
                ))

            # 4. AIS Transponder Continuity
            if cand.get("has_ais_gaps", False):
                gap_val = min(1.0, cand["max_gap_minutes"] / 360.0)
                contradicting.append(EvidenceItem(
                    evidence_id=f"EV_AIS_GAP_{hypothesis.hypothesis_id}",
                    hypothesis_id=hypothesis.hypothesis_id,
                    type="ais_data_discontinuity",
                    value=round(gap_val, 3),
                    direction=DirectionEnum.REFUTES,
                    source="AIS_Integrity_Audit",
                    confidence=0.75,
                    explanation=f"Vessel experienced an AIS transmission gap of {cand['max_gap_minutes']:.1f} minutes during transit window.",
                    timestamp_evaluated=now_utc
                ))

        elif hypothesis.type == HypothesisType.FALSE_POSITIVE:
            # Look-alike hypothesis evidence
            fp_risk = lookalike_info.get("lookalike_risk_score", 0.0)
            if fp_risk >= 0.50:
                supporting.append(EvidenceItem(
                    evidence_id="EV_FP_MET_SUPPORT",
                    hypothesis_id=hypothesis.hypothesis_id,
                    type="meteorological_lookalike_evidence",
                    value=fp_risk,
                    direction=DirectionEnum.SUPPORTS,
                    source="ERA5_Atmospheric_Audit",
                    confidence=0.90,
                    explanation=f"Low wind speed ({lookalike_info.get('wind_speed_ms', 0.0)} m/s) strongly supports a false-positive calm water look-alike.",
                    timestamp_evaluated=now_utc
                ))
            else:
                contradicting.append(EvidenceItem(
                    evidence_id="EV_FP_MET_REFUTE",
                    hypothesis_id=hypothesis.hypothesis_id,
                    type="meteorological_lookalike_refutation",
                    value=round(1.0 - fp_risk, 3),
                    direction=DirectionEnum.REFUTES,
                    source="ERA5_Atmospheric_Audit",
                    confidence=0.88,
                    explanation=f"Moderate wind speed ({lookalike_info.get('wind_speed_ms', 0.0)} m/s) contradicts a calm water look-alike.",
                    timestamp_evaluated=now_utc
                ))

        elif hypothesis.type == HypothesisType.DARK_VESSEL:
            # Dark vessel hypothesis
            supporting.append(EvidenceItem(
                evidence_id="EV_DARK_TRAFFIC",
                hypothesis_id=hypothesis.hypothesis_id,
                type="corridor_traffic_density",
                value=0.45,
                direction=DirectionEnum.SUPPORTS,
                source="Maritime_Traffic_Density",
                confidence=0.60,
                explanation="Active international shipping corridor where unmonitored non-SOLAS or dark vessels operate.",
                timestamp_evaluated=now_utc
            ))

        hypothesis.supporting_evidence = supporting
        hypothesis.contradicting_evidence = contradicting
        return hypothesis

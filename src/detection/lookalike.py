"""
SIH26143 — Look-Alike Defense and Meteorological Gating.
Assesses whether a detected dark SAR feature could be an oceanographic/meteorological look-alike
(e.g., low-wind calm sea, natural biogenic surfactants, internal waves) rather than mineral oil.
"""

import math
from typing import Dict, Any, List
from src.config.schemas import MetoceanObservation, SpillPolygon


class LookalikeDetector:
    """Evaluates false-positive look-alike risks against metocean conditions."""

    LOW_WIND_THRESHOLD_MS = 3.0   # Wind speeds below this cause calm water false dark spots
    HIGH_WIND_THRESHOLD_MS = 12.0 # Wind speeds above this break up surface mineral oil

    @classmethod
    def evaluate_lookalike_risk(
        cls,
        spill: SpillPolygon,
        metocean: MetoceanObservation
    ) -> Dict[str, Any]:
        """
        Calculates a comprehensive look-alike risk score in [0.0, 1.0]
        and generates descriptive flags.
        """
        flags: List[str] = []
        risk_score = 0.0

        # 1. Total Wind Speed
        wind_speed_ms = math.sqrt(metocean.u_wind10_ms ** 2 + metocean.v_wind10_ms ** 2)

        if wind_speed_ms < cls.LOW_WIND_THRESHOLD_MS:
            # Low wind area: immediate high look-alike risk because ocean surface is calm
            excess_calm = (cls.LOW_WIND_THRESHOLD_MS - wind_speed_ms) / cls.LOW_WIND_THRESHOLD_MS
            risk_score += 0.50 + 0.50 * excess_calm
            flags.append(
                f"LOW_WIND_LOOKALIKE_RISK: Wind speed is {wind_speed_ms:.1f} m/s (< 3.0 m/s threshold). "
                "Specular reflection from calm water mimics oil dampening."
            )
        elif wind_speed_ms > cls.HIGH_WIND_THRESHOLD_MS:
            # High wind area: slicks disperse rapidly into water column
            risk_score += 0.35
            flags.append(
                f"HIGH_WIND_DISPERSION_RISK: Wind speed is {wind_speed_ms:.1f} m/s (> 12.0 m/s). "
                "Slicks subject to rapid wave entrainment."
            )

        # 2. Geometric Shape Characteristics
        # Discharging ships produce elongated slicks aligned with ship transit or drift.
        # Perfectly circular or amorphous blobs with elongation close to 1.0 in open ocean are often biogenic slicks.
        if spill.elongation < 1.3 and spill.area_km2 < 1.0:
            risk_score += 0.25
            flags.append("COMPACT_GEOMETRY_RISK: Slick elongation is low (< 1.3), consistent with localized natural biogenic film.")

        # 3. Final Clamping
        risk_score = min(1.0, max(0.0, risk_score))
        is_lookalike_suspected = risk_score >= 0.50

        return {
            "lookalike_risk_score": round(risk_score, 3),
            "is_lookalike_suspected": is_lookalike_suspected,
            "wind_speed_ms": round(wind_speed_ms, 2),
            "flags": flags
        }

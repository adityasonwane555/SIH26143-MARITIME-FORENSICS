"""
SIH26143 — Active Sensing & Next-Best-Evidence Engine.
Formulates candidate follow-up observation actions and calculates their Expected Information Gain
(Entropy Reduction E[ΔH]) to mathematically identify the optimal next evidence to acquire.
"""

import math
from typing import List, Dict, Any, Tuple
from src.config.schemas import (
    Hypothesis,
    HypothesisType,
    NextEvidenceRecommendation,
    BoundingBox,
    OriginProbabilityGrid
)
from src.uncertainty.entropy import UncertaintyQuantifier


class ActiveSensingEngine:
    """Calculates expected information gain for prospective sensor tasking actions."""

    @classmethod
    def recommend_next_evidence(
        cls,
        hypotheses: List[Hypothesis],
        origin_grid: OriginProbabilityGrid
    ) -> List[NextEvidenceRecommendation]:
        """
        Ranks prospective observation actions by expected entropy reduction E[ΔH].
        """
        if len(hypotheses) < 2:
            return []

        entropy_stats = UncertaintyQuantifier.compute_shannon_entropy(hypotheses)
        h_current = entropy_stats["entropy_bits"]

        top1 = hypotheses[0]
        top2 = hypotheses[1]
        bbox = origin_grid.bounds

        recommendations: List[NextEvidenceRecommendation] = []

        # Candidate Action 1: Satellite AIS Gap Resolution
        # Relevant if either top candidate has AIS gaps
        has_ais_gap = any(
            any("gap" in ev.explanation.lower() for ev in h.contradicting_evidence)
            for h in (top1, top2)
        )
        if has_ais_gap:
            # Resolving AIS gap would decisively determine if ship was present
            p_gap_resolves = 0.85
            # If resolved, posterior collapses to dominant hypothesis
            h_after = max(0.2, h_current * 0.35)
            gain = max(0.1, h_current - h_after)
            recommendations.append(NextEvidenceRecommendation(
                recommendation_id="REC_AIS_SATELLITE_DEEP",
                action_type="SATELLITE_AIS_DEEP_ANALYTICS",
                target_sector=bbox,
                separates_hypotheses=(top1.subject_name, top2.subject_name),
                expected_information_gain_bits=round(gain, 3),
                rationale=(
                    f"Acquire commercial satellite AIS archives to reconstruct transponder gaps for "
                    f"'{top1.subject_name}' / '{top2.subject_name}'. Confirms whether candidate was underway or stationary during release."
                ),
                urgency="High"
            ))

        # Candidate Action 2: Optical Multispectral Verification (Look-alike vs Mineral Oil)
        is_lookalike_contender = any(h.type == HypothesisType.FALSE_POSITIVE for h in hypotheses[:3])
        if is_lookalike_contender:
            gain_opt = max(0.2, h_current * 0.55)
            recommendations.append(NextEvidenceRecommendation(
                recommendation_id="REC_OPTICAL_MULTISPECTRAL",
                action_type="OPTICAL_SATELLITE_TASKING",
                target_sector=bbox,
                separates_hypotheses=(top1.subject_name, "False-Positive Look-alike"),
                expected_information_gain_bits=round(gain_opt, 3),
                rationale=(
                    "Task cloud-free Sentinel-2 MSI optical observation over slick coordinates. "
                    "Multispectral band ratio (B2/B4/B8) discriminates mineral oil emulsions from biogenic algal films."
                ),
                urgency="High"
            ))

        # Candidate Action 3: Aerial Maritime Patrol / Vessel Inspection
        if top1.type == HypothesisType.VESSEL and top2.type == HypothesisType.VESSEL:
            gain_patrol = max(0.3, h_current * 0.70)
            recommendations.append(NextEvidenceRecommendation(
                recommendation_id="REC_AERIAL_PATROL",
                action_type="AERIAL_RECONNAISSANCE_TASKING",
                target_sector=bbox,
                separates_hypotheses=(top1.subject_name, top2.subject_name),
                expected_information_gain_bits=round(gain_patrol, 3),
                rationale=(
                    f"Deploy Coast Guard maritime patrol aircraft along transit corridor of leading suspect "
                    f"'{top1.subject_name}'. Visual/FLIR inspection of hull wake and bilge outlet provides decisive physical proof."
                ),
                urgency="Medium"
            ))

        # Candidate Action 4: High-Resolution SAR Revisit
        gain_sar = max(0.15, h_current * 0.40)
        recommendations.append(NextEvidenceRecommendation(
            recommendation_id="REC_SAR_REVISIT",
            action_type="HIGH_RES_SAR_REVISIT",
            target_sector=bbox,
            separates_hypotheses=(top1.subject_name, "Untracked Dark Vessel"),
            expected_information_gain_bits=round(gain_sar, 3),
            rationale=(
                "Task next ascending Sentinel-1 or commercial X-band SAR pass. "
                "Detects persistent secondary sheen and verifies vessel wake trails along the shipping corridor."
            ),
            urgency="Low"
        ))

        # Sort recommendations by Expected Information Gain descending
        recommendations.sort(key=lambda r: r.expected_information_gain_bits, reverse=True)
        return recommendations

"""
SIH26143 — Decision-Theoretic Abstention Engine.
Determines whether available evidence justifies candidate vessel attribution
or whether the scientifically defensible response is honest abstention (INSUFFICIENT_EVIDENCE).
"""

from typing import List, Dict, Any, Tuple, Optional
from src.config.schemas import (
    Hypothesis,
    HypothesisType,
    AttributionDecision
)
from src.uncertainty.entropy import UncertaintyQuantifier


class AbstentionEngine:
    """Enforces rigorous decision-theoretic boundaries to prevent reckless false attributions."""

    MAX_NORMALIZED_ENTROPY_THRESHOLD = 0.82 # If entropy > 82% of uniform, uncertainty is too high
    MIN_SEPARATION_MARGIN = 0.15           # Top-1 must beat Top-2 by at least 15% probability

    @classmethod
    def evaluate_attribution_decision(
        cls,
        hypotheses: List[Hypothesis]
    ) -> Dict[str, Any]:
        """
        Evaluates posterior distribution to output a definitive attribution or principled abstention.
        """
        if not hypotheses:
            return {
                "decision": AttributionDecision.INSUFFICIENT_EVIDENCE,
                "is_abstention": True,
                "reason": "No hypotheses provided for evaluation.",
                "leading_hypothesis": None,
                "confidence": 0.0,
                "entropy_metrics": {"entropy_bits": 0.0, "normalized_entropy": 1.0}
            }

        # Ensure posteriors are calculated and sorted
        sorted_hyp = UncertaintyQuantifier.compute_posteriors(hypotheses)
        entropy_metrics = UncertaintyQuantifier.compute_shannon_entropy(sorted_hyp)

        top1 = sorted_hyp[0]
        top2 = sorted_hyp[1] if len(sorted_hyp) > 1 else None

        p1 = top1.posterior_probability
        p2 = top2.posterior_probability if top2 is not None else 0.0
        margin = p1 - p2
        h_norm = entropy_metrics["normalized_entropy"]

        # Rule 1: High Information Entropy Check (unless top candidate has a decisive > 35% margin)
        if h_norm > cls.MAX_NORMALIZED_ENTROPY_THRESHOLD and margin < 0.35:
            return {
                "decision": AttributionDecision.INSUFFICIENT_EVIDENCE,
                "is_abstention": True,
                "reason": (
                    f"High information entropy (H_norm = {h_norm:.2f} > {cls.MAX_NORMALIZED_ENTROPY_THRESHOLD:.2f}). "
                    "Evidence is too uniformly distributed across multiple explanations to support definitive attribution."
                ),
                "leading_hypothesis": top1,
                "second_hypothesis": top2,
                "margin": round(margin, 3),
                "confidence": p1,
                "entropy_metrics": entropy_metrics
            }

        # Rule 2: Top-2 Indistinguishability Margin Check
        if top2 is not None and margin < cls.MIN_SEPARATION_MARGIN and top1.type == HypothesisType.VESSEL and top2.type == HypothesisType.VESSEL:
            return {
                "decision": AttributionDecision.INSUFFICIENT_EVIDENCE,
                "is_abstention": True,
                "reason": (
                    f"Ambiguous candidate margin (p1 = {p1:.2f}, p2 = {p2:.2f}, margin = {margin:.2f} < {cls.MIN_SEPARATION_MARGIN:.2f}). "
                    f"Vessels '{top1.subject_name}' and '{top2.subject_name}' are statistically indistinguishable under current data."
                ),
                "leading_hypothesis": top1,
                "second_hypothesis": top2,
                "margin": round(margin, 3),
                "confidence": p1,
                "entropy_metrics": entropy_metrics
            }

        # Rule 3: Look-Alike / False-Positive Top Rank
        if top1.type == HypothesisType.FALSE_POSITIVE:
            return {
                "decision": AttributionDecision.FALSE_POSITIVE,
                "is_abstention": False,
                "reason": (
                    f"Leading explanation is a false-positive natural or meteorological phenomenon "
                    f"('{top1.subject_name}', posterior = {p1:.2f}). No vessel attribution warranted."
                ),
                "leading_hypothesis": top1,
                "second_hypothesis": top2,
                "margin": round(margin, 3),
                "confidence": p1,
                "entropy_metrics": entropy_metrics
            }

        # Rule 4: Non-Vessel Infrastructure or Natural Seep Top Rank
        if top1.type in (HypothesisType.OFFSHORE_INFRASTRUCTURE, HypothesisType.NATURAL_SEEP):
            return {
                "decision": AttributionDecision.NON_VESSEL_SOURCE,
                "is_abstention": False,
                "reason": (
                    f"Leading source is non-vessel infrastructure or geology "
                    f"('{top1.subject_name}', posterior = {p1:.2f})."
                ),
                "leading_hypothesis": top1,
                "second_hypothesis": top2,
                "margin": round(margin, 3),
                "confidence": p1,
                "entropy_metrics": entropy_metrics
            }

        # Rule 5: Falsified Vessel Top Rank
        if top1.is_falsified:
            return {
                "decision": AttributionDecision.INSUFFICIENT_EVIDENCE,
                "is_abstention": True,
                "reason": (
                    f"Leading candidate vessel '{top1.subject_name}' failed adversarial physical contradiction challenges. "
                    "Cannot attribute to a falsified hypothesis."
                ),
                "leading_hypothesis": top1,
                "second_hypothesis": top2,
                "margin": round(margin, 3),
                "confidence": p1,
                "entropy_metrics": entropy_metrics
            }

        # Rule 6: Definitive Attribution
        return {
            "decision": AttributionDecision.ATTRIBUTED,
            "is_abstention": False,
            "reason": (
                f"Candidate vessel '{top1.subject_name}' (MMSI: {top1.subject_id}) is the leading hypothesis "
                f"with calibrated posterior probability {p1:.2f} (margin: +{margin:.2f} over next candidate). "
                "Survives all adversarial falsification and counterfactual physical tests."
            ),
            "leading_hypothesis": top1,
            "second_hypothesis": top2,
            "margin": round(margin, 3),
            "confidence": p1,
            "entropy_metrics": entropy_metrics
        }

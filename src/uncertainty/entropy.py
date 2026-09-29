"""
SIH26143 — Uncertainty Quantification and Bayesian Posterior Calibration.
Computes evidence likelihoods, posterior hypothesis distributions,
Shannon information entropy H(p), and calibration metrics.
"""

import math
from typing import List, Dict, Any, Tuple
from src.config.schemas import (
    Hypothesis,
    HypothesisType,
    DirectionEnum
)


class UncertaintyQuantifier:
    """Computes calibrated Bayesian posteriors and Shannon information entropy."""

    @classmethod
    def compute_posteriors(cls, hypotheses: List[Hypothesis]) -> List[Hypothesis]:
        """
        Fuses prior probabilities with bidirectional evidence into calibrated posterior probabilities.
        Applies multiplicative likelihood weighting for supporting [+] and contradicting [-] evidence.
        If no evidence items are attached and non-zero posteriors are already set, preserves them.
        """
        if not hypotheses:
            return []

        # Check if evidence is present on any hypothesis
        has_evidence = any(
            len(h.supporting_evidence) > 0 or len(h.contradicting_evidence) > 0 or h.is_falsified
            for h in hypotheses
        )
        has_preset_posteriors = any(h.posterior_probability > 0.0 for h in hypotheses)

        if not has_evidence and has_preset_posteriors:
            # Preserves pre-set posterior probabilities, just sort descending
            hypotheses.sort(key=lambda x: x.posterior_probability, reverse=True)
            return hypotheses

        unnormalized_likelihoods: List[float] = []

        for h in hypotheses:
            prior = max(0.01, h.prior_probability)
            score = prior

            # Multiply by supporting evidence factors
            for ev in h.supporting_evidence:
                weight = 1.0 + (ev.value * ev.confidence * 1.5)
                score *= weight

            # Multiply by contradicting evidence penalties
            for ev in h.contradicting_evidence:
                penalty = max(0.05, 1.0 - (ev.value * ev.confidence * 0.90))
                score *= penalty

            # If hypothesis failed falsification attack, heavily penalize
            if h.is_falsified:
                score *= 0.05

            unnormalized_likelihoods.append(score)

        total_mass = sum(unnormalized_likelihoods)
        if total_mass <= 0:
            uniform = 1.0 / len(hypotheses)
            for h in hypotheses:
                h.posterior_probability = round(uniform, 4)
            return hypotheses

        # Normalize to valid probability distribution summing to 1.0
        for h, raw_score in zip(hypotheses, unnormalized_likelihoods):
            post = raw_score / total_mass
            h.posterior_probability = round(post, 4)

        # Sort hypotheses by posterior probability descending
        hypotheses.sort(key=lambda x: x.posterior_probability, reverse=True)
        return hypotheses

    @classmethod
    def compute_shannon_entropy(cls, hypotheses: List[Hypothesis]) -> Dict[str, float]:
        """
        Computes Shannon information entropy: H(p) = -sum(p_i * log2(p_i)).
        Also computes normalized entropy H_norm in [0.0, 1.0] relative to uniform distribution.
        """
        n = len(hypotheses)
        if n <= 1:
            return {"entropy_bits": 0.0, "max_entropy_bits": 0.0, "normalized_entropy": 0.0}

        max_entropy = math.log2(n)
        h_bits = 0.0

        for h in hypotheses:
            p = h.posterior_probability
            if p > 1e-6:
                h_bits -= p * math.log2(p)

        h_norm = min(1.0, max(0.0, h_bits / max_entropy)) if max_entropy > 0 else 0.0

        return {
            "entropy_bits": round(h_bits, 3),
            "max_entropy_bits": round(max_entropy, 3),
            "normalized_entropy": round(h_norm, 3)
        }

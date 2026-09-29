"""
SIH26143 — Multi-Hypothesis Generation Engine.
Constructs competing, mutually exclusive source hypotheses for an oil spill incident:
Candidate vessels (H1..Hn), offshore infrastructure (H_infra), natural seeps (H_seep),
dark/untracked vessels (H_dark), and false-positive look-alikes (H_fp).
"""

from typing import List, Dict, Any, Optional
from src.config.schemas import (
    Hypothesis,
    HypothesisType,
    OriginProbabilityGrid,
    SpillPolygon
)


class HypothesisGenerator:
    """Generates a structured set of competing hypotheses with documented prior probabilities."""

    @classmethod
    def generate_hypotheses(
        cls,
        candidate_vessels: List[Dict[str, Any]],
        spill: SpillPolygon,
        lookalike_risk_score: float = 0.0,
        known_infrastructure: Optional[List[Dict[str, Any]]] = None
    ) -> List[Hypothesis]:
        """
        Creates candidate hypotheses:
        - One per filtered vessel candidate
        - Offshore infrastructure (if any nearby)
        - Natural hydrocarbon seep
        - Untracked / dark vessel
        - False-positive look-alike
        Assigns normalized Bayesian priors.
        """
        hypotheses: List[Hypothesis] = []

        # 1. Vessel Hypotheses
        for cand in candidate_vessels:
            hyp = Hypothesis(
                hypothesis_id=f"H_VESSEL_{cand['mmsi']}",
                type=HypothesisType.VESSEL,
                subject_id=cand["mmsi"],
                subject_name=cand["vessel_name"],
                prior_probability=0.0  # normalized below
            )
            hypotheses.append(hyp)

        # 2. Offshore Infrastructure Hypothesis
        has_infra = known_infrastructure is not None and len(known_infrastructure) > 0
        if has_infra:
            for infra in known_infrastructure:
                hypotheses.append(
                    Hypothesis(
                        hypothesis_id=f"H_INFRA_{infra['id']}",
                        type=HypothesisType.OFFSHORE_INFRASTRUCTURE,
                        subject_id=infra["id"],
                        subject_name=infra.get("name", "Offshore Platform / Pipeline"),
                        prior_probability=0.0
                    )
                )

        # 3. Natural Seep Hypothesis
        hypotheses.append(
            Hypothesis(
                hypothesis_id="H_SEEP_NATURAL",
                type=HypothesisType.NATURAL_SEEP,
                subject_id="SEEP_GEO",
                subject_name="Natural Seabed Hydrocarbon Seep",
                prior_probability=0.0
            )
        )

        # 4. Untracked / Dark Vessel Hypothesis
        hypotheses.append(
            Hypothesis(
                hypothesis_id="H_VESSEL_DARK",
                type=HypothesisType.DARK_VESSEL,
                subject_id="NON_BROADCASTING",
                subject_name="Untracked Vessel (AIS Silence / Spoofing)",
                prior_probability=0.0
            )
        )

        # 5. False-Positive Look-alike Hypothesis
        hypotheses.append(
            Hypothesis(
                hypothesis_id="H_LOOKALIKE_FP",
                type=HypothesisType.FALSE_POSITIVE,
                subject_id="NON_OIL_PHENOMENON",
                subject_name="False-Positive (Low-Wind / Biogenic Slicks)",
                prior_probability=0.0
            )
        )

        # 6. Normalize Priors
        # Uninformative base distribution adjusted by initial look-alike risk
        n_total = len(hypotheses)
        if n_total == 0:
            return []

        # Weight look-alike prior according to meteorological look-alike risk score
        fp_weight = max(0.05, lookalike_risk_score * 0.40)
        remaining_weight = 1.0 - fp_weight

        # Distribute remaining mass across remaining hypotheses
        non_fp_count = n_total - 1
        base_share = remaining_weight / max(1, non_fp_count)

        for h in hypotheses:
            if h.type == HypothesisType.FALSE_POSITIVE:
                h.prior_probability = round(fp_weight, 4)
            else:
                h.prior_probability = round(base_share, 4)

        return hypotheses

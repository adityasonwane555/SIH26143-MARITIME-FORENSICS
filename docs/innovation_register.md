# SIH26143 Innovation Register & Novelty Governance

**Document:** `docs/innovation_register.md`  
**System:** Maritime Forensic Intelligence Engine  
**Author:** Lead Architect & ML/Systems Engineer  
**Date:** 2026-09-29  
**Status:** Active Tracking  

---

## 1. Innovation Governance Principles
1. **No Novelty Theater:** An idea is not declared novel simply because we desire it to be. Every claimed differentiator is benchmarked against existing systems (CleanSeaNet, INCOIS OOSA, OpenDrift, SkyTruth Cerulean).
2. **Measurable Improvement:** Every innovation must eventually be validated by a quantitative experiment showing superior performance (accuracy, false accusation reduction, or uncertainty reduction) over a simpler baseline.
3. **Falsifiability:** If an innovation does not improve outcomes, the ablation study must honestly report it.

---

## 2. Innovation Catalog

### INN-01: Multi-Hypothesis Source Attribution Graph
- **What Existing Systems Do:** Select the single vessel nearest to the estimated origin, or output an unconstrained list of nearby ships sorted solely by Euclidean distance.
- **What We Do Differently:** Explicitly formulate mutually exclusive and collectively exhaustive hypotheses:
  - $H_1..H_n$: Candidate individual vessels with specific release time intervals.
  - $H_{infra}$: Offshore drilling rigs, production platforms, or subsea pipelines.
  - $H_{seep}$: Natural seabed hydrocarbon seeps.
  - $H_{dark}$: Unidentified/non-broadcasting vessel.
  - $H_{fp}$: False-positive oceanographic or atmospheric look-alike.
- **Why It Matters:** Prevents premature fixation on an innocent vessel when an offshore pipeline or natural seep was the real source.
- **How It Will Be Measured:** Attribution accuracy on multi-candidate benchmark cases; tracking whether non-vessel sources are correctly identified.
- **Current Status:** Designed; specification complete in `docs/architecture.md`.

---

### INN-02: Bidirectional Evidence Ledger (Positive vs. Negative Fusion)
- **What Existing Systems Do:** Only accumulate positive points in favor of candidate ships (confirmation bias).
- **What We Do Differently:** Maintain a formal evidence ledger that tallies:
  - **Supporting Evidence $[+]$:** Spatiotemporal containment, velocity consistency, course alignment with slick elongation.
  - **Contradicting Evidence $[-]$:** Vessel heading upstream against surface current, ship speed exceeding physically plausible slick deposition rate, vessel confirmed moored, or AIS reporting stationary status.
- **Why It Matters:** In forensic science, contradictory evidence carries higher falsification weight than circumstantial proximity.
- **How It Will Be Measured:** Reduction in false-positive vessel attributions on candidate sets where innocent ships passed near the spill after release.
- **Current Status:** Designed; schema established.

---

### INN-03: Adversarial Self-Falsification ("Attack Hypothesis")
- **What Existing Systems Do:** Display a single confidence number without challenging their own inference.
- **What We Do Differently:** Implement an automated adversarial challenge suite that subjects the leading hypothesis to 5 physical stress tests:
  1. Spatial overlap failure check.
  2. Kinematic transit feasibility check.
  3. Reverse-forward drift consistency check.
  4. Plume morphology consistency check.
  5. AIS track continuity stress test.
- **Why It Matters:** Surfaces hidden contradictions before an investigator takes enforcement action.
- **How It Will Be Measured:** Number of false attributions successfully disproven by the falsification engine across the 10 adversarial test scenarios.
- **Current Status:** Designed; challenge algorithms specified.

---

### INN-04: Counterfactual Physical Forward Simulation
- **What Existing Systems Do:** Stop after backward drift approximation.
- **What We Do Differently:** For each serious candidate, perform a *forward* Lagrangian simulation seeding particles at the candidate ship's exact historical GPS coordinates at time $T_{release}$, advecting forward to the satellite acquisition time $T_{sat}$, and computing the geometric Hausdorff distance and Intersection-over-Union (IoU) between the predicted plume and observed SAR slick.
- **Why It Matters:** Proves whether the suspect ship could physically have produced the observed slick geometry under actual wind and current conditions.
- **How It Will Be Measured:** Hausdorff distance ($\text{km}$) and IoU between forward counterfactual slick and satellite mask.
- **Current Status:** Designed; Runge-Kutta 4 integrator specified.

---

### INN-05: Decision-Theoretic Abstention (`INSUFFICIENT_EVIDENCE`)
- **What Existing Systems Do:** Always report a top-ranked ship, even when confidence is 12% or data is missing.
- **What We Do Differently:** Formulate an explicit decision boundary based on Shannon entropy of the posterior distribution and margin separation between top candidates. If uncertainty exceeds the threshold, the system formally outputs `INSUFFICIENT_EVIDENCE`.
- **Why It Matters:** In high-stakes maritime enforcement, an honest "we cannot determine the source with current data" is vastly superior to a reckless false accusation.
- **How It Will Be Measured:** Abstention rate on ambiguous benchmark scenarios; reduction in false accusations.
- **Current Status:** Designed; mathematical threshold formulated.

---

### INN-06: Active Sensing & Expected Information Gain (Next-Best-Evidence)
- **What Existing Systems Do:** None of the operational or academic systems reviewed algorithmically recommend the next optimal sensor tasking action.
- **What We Do Differently:** When the system abstains due to ambiguity, it calculates the Expected Information Gain ($\mathbb{E}[\Delta H]$) across candidate follow-up actions (satellite SAR revisit, optical imaging, coast guard aerial patrol, deep AIS gap analytics), and recommends the action that will reduce uncertainty the most.
- **Why It Matters:** Directly assists coastal authorities in allocating scarce surveillance assets (aircraft, patrol boats, satellite tasking credits) to resolve the case.
- **How It Will Be Measured:** Simulated entropy reduction $\Delta H$ achieved when the recommended observation is added versus a random observation.
- **Current Status:** Designed; information-theoretic formulation complete.

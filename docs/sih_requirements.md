# SIH26143 — Official Requirements Breakdown & Specification Matrix

**Document:** `docs/sih_requirements.md`  
**Problem Statement ID:** SIH26143  
**Sponsoring Organization:** National Technical Research Organisation (NTRO) / MoD  
**Domain / Theme:** Disaster Management / Space Technology / Maritime Domain Awareness  
**Version:** 1.0.0  
**Date:** 2026-09-29  

---

## 1. Problem Statement Overview

### 1.1 Verbatim Working Statement
> *"Leverage satellite imagery to determine oil spills at sea, correlate them with AIS data, reconstruct the likely spill origin and identify/rank vessels potentially responsible for the spill."*

### 1.2 Operational Objective
To build an automated, scientific, explainable intelligence system that transforms satellite observations of oil pollution in coastal and oceanic waters into forensically sound, actionable vessel attribution reports.

---

## 2. Requirements Decomposition

We categorize all system capabilities into three explicit tiers:
1. `REQUIRED`: Explicitly mandated by the problem statement and operational needs.
2. `OPTIONAL`: Practical operational extensions that enhance real-world utility.
3. `OUR INNOVATIONS`: Core differentiators that elevate this system above naive student/commercial baselines.

### 2.1 REQUIRED Tier

| Req ID | Title | Description | Acceptance Criteria |
|---|---|---|---|
| **REQ-S1** | Satellite Spill Detection | Detect candidate oil spills on sea surface from spaceborne imagery (primarily SAR C-band, with optical support). | Output binary mask and GeoJSON polygon with localized pixel confidence. |
| **REQ-S2** | Geometric Characterization | Calculate geometric properties of detected slick: surface area ($\text{km}^2$), perimeter ($\text{km}$), centroid, major/minor axes, orientation, and elongation. | Unit tests validating geometry calculations against known ground-truth shapes. |
| **REQ-S3** | Oceanographic & Metocean Ingestion | Ingest surface currents (CMEMS/HYCOM) and surface wind fields (ERA5/GFS). | Spatial-temporal interpolation providing $\vec{u}_c(x, y, t)$ and $\vec{u}_{10}(x, y, t)$. |
| **REQ-S4** | Reverse Drift Hindcasting | Reconstruct probable spill origin point and estimated release time window $[T_{rel\_min}, T_{rel\_max}]$. | Vectorized backward Lagrangian advection tracking with temporal bounds. |
| **REQ-S5** | Origin Probability Surface | Generate a continuous 2D spatial probability distribution surface rather than an oversimplified single point. | 2D raster / KDE contours representing origin likelihood. |
| **REQ-S6** | AIS Ingestion & Trajectory Analysis | Ingest historical AIS feeds; filter vessel tracks intersecting the origin envelope during the release time window. | Return filtered candidate vessel catalog with kinematic attributes. |
| **REQ-S7** | Candidate Vessel Ranking | Score and rank candidate vessels based on spatiotemporal compatibility with the reconstructed origin. | Transparent ranking score based on documented heuristic and probabilistic metrics. |

### 2.2 OPTIONAL Tier

| Req ID | Title | Description | Acceptance Criteria |
|---|---|---|---|
| **OPT-01** | Multi-Sensor Fusion | Cross-verify SAR detections against Sentinel-2 MSI optical reflectance. | Flagging of sunglint, algal blooms, and cloud obstruction. |
| **OPT-02** | Forward Forecasting | Simulate future 24–72h trajectory to forecast shoreline beaching risks. | Forward particle advection showing coastal impact zones. |
| **OPT-03** | Weathering Dynamics | Incorporate Mackay evaporation and natural emulsification rate approximations. | Oil mass balance breakdown (surface vs. evaporated). |
| **OPT-04** | Formal Investigation Report | Export complete case evidence into formatted PDF / Markdown / JSON dossiers. | Downloadable comprehensive incident dossier. |

### 2.3 OUR INNOVATIONS Tier (Differentiating Capabilities)

| Req ID | Title | Description | Acceptance Criteria |
|---|---|---|---|
| **INN-01** | Multi-Hypothesis Graph | Generate explicit competing explanations ($H_1..H_n$ vessels, $H_{infra}$ offshore platform, $H_{seep}$ natural seep, $H_{fp}$ look-alike). | Graph data model holding competing hypotheses with prior and posterior weights. |
| **INN-02** | Bidirectional Evidence Ledger | Explicitly score both supporting $[+]$ evidence and contradicting $[-]$ evidence (e.g., vessel moving against current, incompatible speed). | Evidence panel showing itemized proofs with source provenance. |
| **INN-03** | Adversarial Falsification ("Attack Hypothesis") | Automated challenge tests attempting to disprove leading candidates (spatial, temporal, kinematic, drift, shape contradictions). | "ATTACK HYPOTHESIS" button executing tests and surfacing counter-evidence. |
| **INN-04** | Counterfactual Forward Simulation | Run forward simulation from candidate ship's exact historical position and release time; compare predicted plume against observed SAR polygon. | Quantitative plume overlap metrics: Hausdorff distance and IoU. |
| **INN-05** | Decision-Theoretic Abstention | Formulate explicit abstention policy: return `INSUFFICIENT_EVIDENCE` when hypothesis entropy exceeds threshold or candidates are indistinguishable. | System refuses false attribution on ambiguous synthetic and historical cases. |
| **INN-06** | Information-Theoretic Active Sensing (Next-Best-Evidence) | Compute Expected Information Gain ($\mathbb{E}[\Delta H]$) over possible follow-up actions (targeted SAR pass, optical tasking, aerial patrol). | Algorithmic ranking of next sensor tasking actions by uncertainty reduction. |
| **INN-07** | Deterministic Offline Demo Mode | Complete end-to-end operation with `DEMO_MODE=true` without internet or live API dependencies. | Rehearsable 3–5 minute investigation walkthrough running entirely locally. |

---

## 3. Ambiguities & Defensive Engineering Decisions

1. **Ambiguity in "Spill Age":** Chemical weathering can only approximately indicate age without oil crude sampling.  
   *Decision:* The system reports an **estimated release window** derived from backward advection and diffusion dispersion bounds, rather than claiming a false chemical age precision.
2. **Ambiguity in AIS Coverage:** Transponder signals may be missing due to satellite receiver gaps or deliberate disabling.  
   *Decision:* The system treats AIS gaps as **data-quality uncertainty features**, not direct proof of illegal conduct. It formulates $H_{dark}$ (untracked vessel hypothesis) when shipping lane density is high.
3. **Ambiguity in Hydrodynamic Reversibility:** Advection is reversible; turbulent diffusion is not.  
   *Decision:* The backward drift engine produces an **expanding probability distribution surface**, explicitly quantifying the growing spatial uncertainty as one looks further back in time.

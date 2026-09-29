# SIH26143 Maritime Forensic Intelligence Engine
## Comprehensive Implementation Plan & Engineering Roadmap

**Document:** `docs/IMPLEMENTATION_PLAN.md`  
**System Version:** 1.0.0-PROPOSED  
**Author:** Lead Architect & Systems Engineer  
**Date:** 2026-09-29  
**Status:** Approved for Gate 1 Review  

---

## 1. Architectural Philosophy: The Closed-Loop Forensic Workflow

Unlike conventional pipelines that proceed linearly from detection to vessel ranking, our system operates as an **iterative evidence-driven Bayesian forensic loop**:

```text
       ┌────────────────────────────────────────────────────────┐
       │                1. SATELLITE OBSERVATION                │
       │  - Sentinel-1 SAR (VV/VH backscatter dampening)        │
       │  - Sentinel-2 Optical (multispectral verification)     │
       └───────────────────────────┬────────────────────────────┘
                                   │
                                   ▼
       ┌────────────────────────────────────────────────────────┐
       │         2. DETECTION & GEOMETRIC CHARACTERIZATION      │
       │  - Dark spot extraction & thresholding                 │
       │  - Look-alike meteorological defense (ERA5 wind check) │
       │  - Geometry: Area, Perimeter, Centroid, Axes, Elong.   │
       └───────────────────────────┬────────────────────────────┘
                                   │
                                   ▼
       ┌────────────────────────────────────────────────────────┐
       │         3. METOCEAN-DRIVEN BACKWARD DRIFT ENGINE       │
       │  - CMEMS Surface Currents (uo, vo) + ERA5 Winds (u, v) │
       │  - Reverse 4th-order Runge-Kutta Lagrangian solver     │
       │  - 2D Gaussian Kernel Origin Probability Surface P(x,y)│
       └───────────────────────────┬────────────────────────────┘
                                   │
                                   ▼
       ┌────────────────────────────────────────────────────────┐
       │           4. AIS INGESTION & CORRIDOR FILTERING        │
       │  - Historical AIS tracks (MMSI, SOG, COG, Lat/Lon)     │
       │  - Kinematic validation & gap analysis                 │
       │  - Spatiotemporal filter against Origin Envelope       │
       └───────────────────────────┬────────────────────────────┘
                                   │
                                   ▼
       ┌────────────────────────────────────────────────────────┐
       │              5. MULTI-HYPOTHESIS GENERATOR             │
       │  - Competing candidates: H1..Hn (Vessels)              │
       │  - Non-vessel candidates: H_infra, H_seep, H_fp        │
       └───────────────────────────┬────────────────────────────┘
                                   │
                                   ▼
       ┌────────────────────────────────────────────────────────┐
       │             6. BIDIRECTIONAL EVIDENCE FUSION           │
       │  - Positive Evidence: Spatial, Temporal, Drift overlap │
       │  - Negative Evidence: Speed conflict, course deviation │
       │  - Data Quality: AIS gap score, metocean variance      │
       └───────────────────────────┬────────────────────────────┘
                                   │
                                   ▼
       ┌────────────────────────────────────────────────────────┐
       │           7. ADVERSARIAL FALSIFICATION ENGINE          │
       │  - "Attack Hypothesis" self-contradiction tests        │
       │  - Kinematic feasibility check (can vessel be there?)  │
       │  - Counterfactual Forward Run: Plume vs Observed Slick │
       └───────────────────────────┬────────────────────────────┘
                                   │
                                   ▼
       ┌────────────────────────────────────────────────────────┐
       │         8. UNCERTAINTY QUANTIFICATION & ABSTENTION     │
       │  - Bayesian Posterior Probability & Entropy H(p)       │
       │  - If H(p) > threshold: Output INSUFFICIENT_EVIDENCE   │
       │  - Else: Rank leading candidate with calibrated conf.  │
       └───────────────────────────┬────────────────────────────┘
                                   │
                                   ▼
       ┌────────────────────────────────────────────────────────┐
       │          9. ACTIVE SENSING (NEXT-BEST-EVIDENCE)        │
       │  - Formulate hypothetical future observations          │
       │  - Compute Expected Information Gain ΔH for each action│
       │  - Recommend optimal targeted observation              │
       └───────────────────────────┬────────────────────────────┘
                                   │ (When new data arrives)
                                   └───────────────► [Loop Back to Step 5]
```

---

## 2. Directory Layout & Module Specifications

```text
SIH26143-MARITIME-FORENSICS/
├── app/                        # Web and API interfaces
│   ├── api/                    # FastAPI asynchronous application
│   │   ├── routes/             # Modular endpoint routers
│   │   │   ├── incidents.py    # Incident management
│   │   │   ├── detection.py    # Satellite detection runs
│   │   │   ├── drift.py        # Drift hindcasting & origin surfaces
│   │   │   ├── ais.py          # Vessel filtering & track retrieval
│   │   │   ├── hypotheses.py   # Multi-hypothesis graph & evaluation
│   │   │   ├── falsification.py# Adversarial attack tests
│   │   │   ├── uncertainty.py  # Uncertainty & abstention metrics
│   │   │   └── evidence_rec.py # Next-best-evidence recommendations
│   │   └── schemas/            # Pydantic v2 data models
│   └── frontend/               # React 19 + TypeScript + Vite workstation
├── src/                        # Core algorithmic Python packages
│   ├── detection/              # Satellite & SAR dark-spot algorithms
│   │   ├── base.py             # SpillDetector abstract base class
│   │   ├── threshold.py        # Adaptive thresholding detector
│   │   ├── lookalike.py        # Meteorological & texture look-alike filter
│   │   └── characterizer.py    # Polygon geometry & shape descriptors
│   ├── drift/                  # Oceanographic & atmospheric transport
│   │   ├── lagrangian.py       # Vectorized RK4 advection-diffusion solver
│   │   ├── metocean.py         # CMEMS current & ERA5 wind interpolators
│   │   └── origin_surface.py   # 2D KDE probability grid generation
│   ├── ais/                    # Vessel trajectory processing
│   │   ├── reader.py           # Ingestion for MarineCadastre / DMA / CSV
│   │   ├── cleaner.py          # Kinematic outlier rejection & gap tagging
│   │   └── filter.py           # Spatiotemporal intersection with origin envelope
│   ├── hypotheses/             # Hypothesis management & graph
│   │   ├── models.py           # Hypothesis dataclasses & priors
│   │   └── generator.py        # Candidate explanation generator
│   ├── evidence/               # Bidirectional evidence fusion
│   │   ├── aggregator.py       # Positive and negative score fusion
│   │   └── metrics.py          # Spatial, temporal, and drift likelihoods
│   ├── falsification/          # Adversarial testing & counterfactuals
│   │   ├── attacks.py          # Physical contradiction rules
│   │   └── counterfactual.py   # Forward plume simulation vs observed polygon
│   ├── uncertainty/            # Calibration & abstention
│   │   ├── entropy.py          # Shannon entropy & posterior calibration
│   │   └── abstention.py       # Decision-theoretic abstention rules
│   └── evidence_selection/     # Active sensing & information gain
│       ├── candidate_actions.py# Satellite/aerial/AIS action definitions
│       └── info_gain.py        # Expected entropy reduction calculator
├── data/                       # Data storage tiers
│   ├── raw/                    # Pristine source data
│   ├── interim/                # Intermediate working files
│   ├── processed/              # Analysis-ready GeoJSON/GeoTIFF
│   ├── synthetic/              # Mathematical ground-truth benchmarks
│   └── metadata/               # cases.csv and schemas
├── experiments/                # Reproducible case studies & reports
│   └── case_001/               # Primary end-to-end historical test
├── docs/                       # Technical documentation & registries
└── tests/                      # Automated test suite (unit, integration, adversarial)
```

---

## 3. Phased Implementation Roadmap (Gates 1 to 13)

### Gate 1: System Discovery & Architecture (Current Milestone)
- **Deliverables:** `docs/PROJECT_DISCOVERY.md`, `docs/PRIOR_ART.md`, `docs/DATA_REGISTRY.md`, `docs/IMPLEMENTATION_PLAN.md`, `data/metadata/cases.csv`.
- **Exit Verification:** Review architectural soundness, confirm absence of fake data, verify mathematical defensibility.

### Gate 2: Benchmark Case Data & Synthetic Generators
- **Deliverables:**
  - Build synthetic benchmark generator (`data/synthetic/generate_synthetic_case.py`) providing mathematically exact ground-truth (analytic current, known ship trajectory, forward-diffused slick polygon).
  - Package curated benchmark inputs for `CASE_001_WAKASHIO` and `CASE_005_SYNTHETIC_CHALLENGE`.
- **Exit Verification:** Unit test data loaders; verify all fields against Pydantic schemas.

### Gate 3: Detection & Geometric Characterization Module
- **Deliverables:**
  - `src/detection/base.py` & `src/detection/threshold.py`.
  - `src/detection/lookalike.py` (ERA5 wind gating $< 3\text{ m/s}$).
  - `src/detection/characterizer.py` (area, perimeter, centroid, orientation, elongation).
- **Exit Verification:** Test against synthetic slick and benchmark masks; verify polygon extraction and metadata preservation.

### Gate 4: Lagrangian Drift Engine & Origin Probability Surface
- **Deliverables:**
  - `src/drift/lagrangian.py` (RK4 integrator with reverse time-stepping).
  - `src/drift/metocean.py` (Spatial/temporal bilinear interpolation of $\vec{u}_c, \vec{u}_{10}$).
  - `src/drift/origin_surface.py` (2D Gaussian KDE generating continuous raster / GeoJSON contours).
- **Exit Verification:** Reversibility benchmark (forward simulation followed by backward hindcast); verify origin probability density coverage.

### Gate 5: AIS Ingestion, Cleaning & Spatiotemporal Filtering
- **Deliverables:**
  - `src/ais/cleaner.py` (speed sanity checks $> 35\text{ knots}$, acceleration spikes, coordinate validation).
  - `src/ais/cleaner.py` (AIS gap scoring: tag duration and distance of transponder silence).
  - `src/ais/filter.py` (filter vessel tracks intersecting origin probability envelope $[(X, Y) \pm \Delta r, T_0 \pm \Delta t]$).
- **Exit Verification:** Benchmark filtering against 100+ simultaneous vessel tracks; verify zero false negatives for intersecting vessels.

### Gate 6: End-to-End Baseline Pipeline (`Satellite -> Drift -> AIS -> Heuristic Ranking`)
- **Deliverables:**
  - Minimal end-to-end script executing naive nearest-neighbor attribution.
  - Generates baseline evaluation metrics on `CASE_005_SYNTHETIC_CHALLENGE`.
- **Exit Verification:** Save baseline results as `reports/baseline_report.md` to serve as the control for all subsequent innovation metrics.

### Gate 7: Multi-Hypothesis & Bidirectional Evidence Engine
- **Deliverables:**
  - `src/hypotheses/generator.py` (creates $H_1..H_n$, $H_{infra}$, $H_{seep}$, $H_{fp}$).
  - `src/evidence/aggregator.py` (computes explicit supporting $[+]$ and refuting $[-]$ evidence items).
- **Exit Verification:** Verify evidence balance for edge cases (e.g., vessel moving against current receives strong negative drift evidence).

### Gate 8: Adversarial Falsification & Counterfactual Forward Simulation
- **Deliverables:**
  - `src/falsification/attacks.py` ("Attack Hypothesis" test suite: spatial, temporal, kinematic, drift, shape).
  - `src/falsification/counterfactual.py` (forward simulation from suspect vessel's track; computes Hausdorff distance and IoU against observed SAR slick).
- **Exit Verification:** Successfully falsify innocent nearby vessels that fail counterfactual plume geometry matching.

### Gate 9: Uncertainty Propagation & Principled Abstention
- **Deliverables:**
  - `src/uncertainty/entropy.py` (computes Shannon entropy of posterior hypothesis distribution).
  - `src/uncertainty/abstention.py` (triggers `INSUFFICIENT_EVIDENCE` when entropy exceeds threshold or top two candidates are indistinguishable).
- **Exit Verification:** Run ambiguous two-ship test scenario; verify system correctly abstains rather than arbitrarily guessing.

### Gate 10: Next-Best-Evidence (Information Gain) Engine
- **Deliverables:**
  - `src/evidence_selection/info_gain.py` (evaluates candidate actions: satellite tasking, aerial surveillance, AIS forensics).
  - Ranks actions by expected entropy reduction $\mathbb{E}[\Delta H]$.
- **Exit Verification:** Confirm system identifies the exact observation that separates the top two ambiguous hypotheses.

### Gate 11: REST API & Interactive Investigation Workstation
- **Deliverables:**
  - FastAPI asynchronous backend with fully documented OpenAPI endpoints.
  - React + TypeScript + Vite frontend workstation featuring:
    - Interactive geospatial map (satellite slick, origin surface, AIS tracks, counterfactuals).
    - Evidence panel with bidirectional proof breakdown.
    - Interactive "WHY?", "ATTACK HYPOTHESIS", and "WHAT SHOULD WE CHECK NEXT?" controls.
- **Exit Verification:** End-to-end integration test from browser UI through backend to algorithmic response.

### Gate 12: Comprehensive Evaluation & Ablation Suite
- **Deliverables:**
  - Quantitative comparison: Baseline vs. Proposed Forensic System.
  - 10-scenario adversarial stress test suite.
  - Production of `reports/attribution_report.md` and `reports/ablation_report.md`.
- **Exit Verification:** Demonstrate statistically significant improvement in attribution precision and reduction in false accusations.

### Gate 13: Deterministic Offline Demo Mode
- **Deliverables:**
  - Complete zero-internet demo execution with `DEMO_MODE=true`.
  - Rehearsable 3–5 minute investigation walkthrough script (`docs/demo_script.md`).
- **Exit Verification:** Execute complete investigation demo with network adapters disabled.

---

## 4. Technical Risk Matrix & Mitigation Strategy

| Risk ID | Risk Description | Severity | Probability | Mitigation Strategy |
|---|---|:---:|:---:|---|
| **TR-1** | Missing native GIS libraries in Python 3.13 (`gdal`, `rasterio`) | High | Medium | Implement lightweight pure-Python + NumPy/SciPy fallbacks for raster handling; use standard Shapely / GeoPandas where wheels exist or pure GeoJSON math. |
| **TR-2** | Metocean grid resolution ($8\text{ km}$) too coarse for nearshore drift | High | High | Add stochastic sub-grid turbulent diffusion ($\sigma = \sqrt{2 D \Delta t}$); report spatial origin uncertainty as a broadened contour rather than a false point. |
| **TR-3** | Inverting turbulent diffusion is physically impossible (entropy increase) | Critical | Guaranteed | Formulate origin backward estimation as a probability density surface $P(x, y)$, NOT a single deterministic reverse trajectory. |
| **TR-4** | Non-compliant / dark vessels disabling AIS transponders | Critical | High | Explicitly generate hypothesis $H_{dark}$; evaluate shipping lane transit densities; calculate next-best-evidence recommendation for high-resolution SAR to detect non-broadcasting ship hulls. |
| **TR-5** | False attribution and legal liability | Critical | Medium | Enforce strict abstention policy; present findings as investigative decision support; prohibit definitive judicial accusation terminology. |

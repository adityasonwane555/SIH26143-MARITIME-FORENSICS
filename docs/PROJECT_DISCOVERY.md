# SIH26143 — Maritime Forensic Intelligence & Oil Spill Attribution System
## Project Discovery & Operational Specification

**Problem Statement ID:** SIH26143  
**Title:** Leveraging satellite imagery to determine oil spills at sea along with AIS data correlations to identify the vessel responsible for the spill  
**Sponsoring Organization:** National Technical Research Organisation (NTRO) / MoD  
**Domain:** Disaster Management / Space Technology / Maritime Domain Awareness (MDA)  
**Document Version:** 1.0.0  
**Date:** 2026-09-29  

---

## 1. Executive Summary & Problem Formulation

### 1.1 The Operational Context
Maritime oil discharges—both intentional bilge dumping and accidental tanker bunker releases—cause severe ecological destruction and economic harm. While spaceborne Synthetic Aperture Radar (SAR) can detect oil slicks across vast ocean expanses regardless of cloud cover or sunlight, **detection alone does not establish attribution**.

Attribution requires answering three coupled inverse problems:
1. **Geometric & Temporal Hindcast:** Given the observed slick polygon at satellite acquisition timestamp $T_{sat}$, where and when was the oil discharged? (Backtracking under meteorological and oceanographic forcing: surface currents $\vec{u}_c$, 10-meter wind $\vec{u}_{10}$, waves, and weathering).
2. **Kinematic & Trajectory Correlation:** Which vessels recorded in Automatic Identification System (AIS) transponder data occupied the spatiotemporal origin envelope $[(X, Y) \pm \Delta r, T_0 \pm \Delta t]$?
3. **Forensic Attribution under Uncertainty:** When multiple vessels or non-vessel sources (offshore platforms, natural oil seeps, low-wind look-alikes) are present, which hypothesis is most consistent with physical dynamics, and can competing explanations be decisively falsified?

### 1.2 System Positioning: Decision Support, Not Judicial Condemnation
In accordance with forensic science principles (ISO/IEC 17025, Daubert standard for scientific evidence):
- The system is an **Investigative Decision-Support and Attribution Intelligence Platform**.
- It **never** issues uncalibrated claims such as *"Vessel X is guilty"*.
- It produces probabilistic hypothesis rankings, supporting vs. contradicting evidence tallies, counterfactual forward-simulation validation, and explicitly **abstains** (`INSUFFICIENT_EVIDENCE`) when data density or physical uncertainty prevents separation of candidate hypotheses.

---

## 2. Requirements Matrix & Traceability

| ID | Category | Requirement Description | Classification | Verification Method |
|---|---|---|---|---|
| **REQ-01** | Satellite Ingestion & Detection | Ingest SAR (Sentinel-1 GRD IW) and multi-spectral (Sentinel-2 MSI) scenes; detect dark-spot anomalies with confidence scoring. | **Core** | IoU / F1 on benchmark SAR slick datasets |
| **REQ-02** | Look-alike Discrimination | Discriminate mineral oil slicks from biogenic films, upwelling, wind shadows, and internal waves using wind thresholds ($<3\text{ m/s}$ risk) and texture/gradient metrics. | **Core** | False-positive rejection rate on low-wind scenes |
| **REQ-03** | Geometric Characterization | Compute spatial envelope: perimeter, area ($\text{km}^2$), centroid, major/minor axes, orientation, and elongation. | **Core** | Geometric unit test against synthetic & ground-truth polygons |
| **REQ-04** | Metocean Data Ingestion | Acquire gridded surface current fields (CMEMS GLORYS12/Analysis) and surface wind fields (ECMWF ERA5 / GFS). | **Core** | Verification of spatial-temporal interpolation coverage |
| **REQ-05** | Reverse Drift Hindcasting | Compute backward Lagrangian particle trajectories to estimate source location and release timestamp window $T_{release} \in [T_{sat} - \Delta t, T_{sat}]$. | **Core** | Trajectory benchmark vs OpenDrift / analytical solutions |
| **REQ-06** | Origin Probability Surface | Generate continuous probability distribution grid $P(x, y, t)$ of spill release rather than an oversimplified single point. | **Core** | Gaussian KDE / particle density raster output verification |
| **REQ-07** | AIS Ingestion & Track Reconstruction | Ingest historical AIS records (MMSI, lat, lon, SOG, COG, timestamp); perform kinematic cleaning, dead-reckoning interpolation, and gap flagging. | **Core** | Trajectory continuity & kinematic boundary checks |
| **REQ-08** | Spatiotemporal Candidate Filtering | Filter all vessel tracks intersecting the origin probability envelope during the release time window. | **Core** | Spatiotemporal query benchmark against full vessel catalog |
| **REQ-09** | Baseline Attribution Pipeline | Compute deterministic heuristic score based on minimum distance, time delta, and trajectory intersection. | **Baseline** | Reproducible baseline pipeline execution |
| **REQ-10** | Multi-Hypothesis Evidence Engine | Generate competing hypotheses ($H_i: \text{Vessel}_i$, $H_{infra}: \text{Platform}$, $H_{seep}: \text{Natural Seep}$, $H_{fp}: \text{False Positive}$). | **Innovation** | Bidirectional evidence tally (supports vs contradicts) |
| **REQ-11** | Adversarial Falsification & Self-Attack | Execute automated consistency checks (spatial overlap, temporal feasibility, drift continuity, AIS integrity) to falsify hypotheses. | **Innovation** | Falsification engine unit tests across ambiguous edge cases |
| **REQ-12** | Counterfactual Forward Drift Simulation | For top candidate vessels, simulate forward discharge from historical vessel coordinates to verify if predicted slick matches observed SAR geometry. | **Innovation** | Overlap metric (Hausdorff distance, IoU, centroid drift error) |
| **REQ-13** | Uncertainty Quantification & Abstention | Propagate metocean, measurement, and sensor coverage uncertainty. Return `INSUFFICIENT_EVIDENCE` when hypothesis posterior entropy exceeds threshold. | **Innovation** | Calibration curve, Brier score, and abstention test suite |
| **REQ-14** | Information-Theoretic Next-Best-Evidence | Calculate expected information gain (entropy reduction $\Delta H$) of potential next observations (targeted SAR pass, optical tasking, aerial patrol). | **Innovation** | Ranking of tasking actions by expected uncertainty reduction |
| **REQ-15** | Closed-Loop Re-evaluation | Allow ingestion of incremental evidence (new AIS segment, aerial verification) and recompute posterior hypothesis graph. | **Innovation** | Dynamic state update test in FastAPI pipeline |
| **REQ-16** | Deterministic Offline Demo Mode | Run end-to-end without live internet connections using pre-packaged historical benchmark scenarios. | **System** | Complete pipeline execution with `DEMO_MODE=true` |

---

## 3. Current Repository Audit

A forensic scan of `E:\Drive D Clone\Made_By_Me\Applications\SIH26143-MARITIME-FORENSICS` reveals:
- **Directory Structure:**
  - `research/` (initialized with `.gitkeep`)
  - `data/` (initialized with subdirectories `raw/`, `interim/`, `processed/`, `synthetic/`, `metadata/`)
  - `experiments/` (initialized with `.gitkeep`)
  - `app/` (initialized with `.gitkeep`)
  - `docs/` (newly created for architectural artifacts)
  - `prompts/input/Building.md` (authoritative architectural directive)
  - `README.md` (initial root commit)
- **Runtime Environment:**
  - **OS:** Windows 10/11 x64
  - **Python:** 3.13.7 (64-bit)
  - **Node.js:** v24.11.1
  - **Git:** 2.50.1.windows.1
  - **Key Installed Packages:** `fastapi` 0.115.6, `uvicorn` 0.32.1, `pydantic` 2.13.4, `numpy` 2.2.0, `scipy` 1.16.1, `pandas` 2.3.1, `matplotlib` 3.10.6, `pillow` 11.3.0, `SQLAlchemy` 2.0.36, `asyncpg` 0.30.0, `psycopg2` 2.9.11, `httpx` 0.28.1, `pytest` 8.3.4.
- **Deficiencies & Technical Debt:**
  - No source code implemented yet.
  - Geospatial libraries (`shapely`, `pyproj`, `geopandas`, `rasterio`) not yet installed in Python 3.13 environment.
  - No database migration or schema defined yet.
- **Readiness:** High. The clean repository state allows a disciplined, modular architecture to be established without legacy refactoring friction.

---

## 4. System Assumptions & Falsifiability Analysis

| Assumption | Scientific Basis | Potential Failure Mode / Counter-Evidence | Mitigation / Safeguard |
|---|---|---|---|
| **A1: Surface Oil Advection** | Surface slicks drift at $\approx 100\%$ of surface ocean current $\vec{u}_c$ plus $3.0\%\text{--}3.5\%$ of 10m wind velocity $\vec{u}_{10}$ with Coriolis deflection angle ($0^\circ\text{--}15^\circ$ right in NH). | Non-linear Stokes drift from wave action, subsurface entrainment, or localized sub-mesoscale eddies not captured by global reanalysis ($0.083^\circ$ CMEMS). | Uncertainty parameterization: inject stochastic Brownian velocity perturbations $\sigma_u, \sigma_v$; output probabilistic probability density rather than a deterministic trajectory. |
| **A2: Reverse Drift Invertibility** | Advective components can be run in reverse ($-\Delta t$) to trace origin envelope. | Turbulent diffusion is thermodynamically irreversible. Backtracking particles diffuse outward, broadening the spatial envelope backwards in time. | Represent origin as a spatial probability density function $P(x, y)$ rather than a single trajectory trace. Explicitly report origin envelope expansion over time. |
| **A3: AIS Track Integrity** | Vessels transmitting AIS are identifiable via MMSI, IMO, and callsign. | Vessels deliberately discharging oily bilge often switch off Class A/B transponders (AIS dark activity) or transmit spoofed positions. | Model AIS gaps as data-quality/uncertainty features, not direct guilt. Formulate hypothesis $H_{dark}$ (untracked/dark vessel) and evaluate ship traffic density along maritime corridors. |
| **A4: SAR Slick Detectability** | Oil dampens capillary and short gravity waves ($1\text{--}10\text{ cm}$), causing specular reflection away from SAR sensor, resulting in dark signatures in VV/VH backscatter. | Low wind speeds ($< 2\text{--}3\text{ m/s}$) produce look-alike dark patches because water surface is calm everywhere. High winds ($> 12\text{--}14\text{ m/s}$) break and disperse slicks into the water column. | Implement meteorological gating: flag low-wind look-alike risk if ERA5 wind speed $< 3\text{ m/s}$; flag detection uncertainty if wind $> 12\text{ m/s}$. |

---

## 5. Technology Stack Decisions

```text
[ Satellite Data (Sentinel-1 SAR) ]   [ Metocean (CMEMS / ERA5) ]   [ AIS Transponder Feeds ]
                         \                         |                         /
                          \                        |                        /
                           ▼                       ▼                       ▼
            +-----------------------------------------------------------------------+
            |                        DATA & PIPELINE LAYER                         |
            |   - Rasterio / Shapely / GeoPandas: Spatial processing                |
            |   - Vectorized Lagrangian Engine: 4th-order Runge-Kutta advection      |
            |   - SciPy / NumPy: Kernel Density Estimation & Gaussian dispersion    |
            +-----------------------------------------------------------------------+
                                                   │
                                                   ▼
            +-----------------------------------------------------------------------+
            |                       CORE FORENSIC ENGINE                            |
            |   - Hypothesis Engine: Bayesian priors & candidate generation         |
            |   - Evidence Engine: Positive & negative evidence fusion               |
            |   - Falsification Engine: Automated hypothesis contradiction tests    |
            |   - Counterfactual Simulator: Forward trajectory verification         |
            |   - Uncertainty Engine: Information entropy & abstention threshold    |
            |   - Next-Best-Evidence: Information Gain (ΔH) optimization            |
            +-----------------------------------------------------------------------+
                                                   │
                                                   ▼
            +-----------------------------------------------------------------------+
            |                        BACKEND & API LAYER                            |
            |   - FastAPI (Python 3.13): Asynchronous REST API                     |
            |   - Pydantic v2: Strict typed schema validation                       |
            |   - PostgreSQL + PostGIS (with SQLite / Spatialite local fallback)    |
            +-----------------------------------------------------------------------+
                                                   │
                                                   ▼
            +-----------------------------------------------------------------------+
            |                       INVESTIGATION WORKSTATION                       |
            |   - React 19 + TypeScript + Vite: High-density analyst dashboard       |
            |   - MapLibre GL / Leaflet: Hardware-accelerated geospatial canvas     |
            |   - "Why?" & "Attack Hypothesis" & "Next Evidence" interactive panels  |
            +-----------------------------------------------------------------------+
```

---

## 6. Gated Verification Roadmap

The implementation is structured strictly according to the 13 Gates outlined in the master engineering specification:
- **Gate 1 (Current):** Research, Discovery, Architecture, Prior Art, Data Registry, and Implementation Plan.
- **Gate 2:** Benchmark Case Selection & Data Acquisition infrastructure.
- **Gate 3:** SAR Detection & Geospatial Slick Characterization.
- **Gate 4:** Lagrangian Backward Drift & Origin Probability Surface.
- **Gate 5:** Historical AIS Ingestion, Kinematic Cleaning & Spatiotemporal Filtering.
- **Gate 6:** End-to-End Baseline Pipeline (`Satellite -> Drift -> AIS -> Heuristic Ranking`).
- **Gate 7:** Multi-Hypothesis Generation & Evidence Graph Engine.
- **Gate 8:** Adversarial Falsification & Counterfactual Forward Simulation.
- **Gate 9:** Uncertainty Propagation & Principled Abstention.
- **Gate 10:** Next-Best-Evidence & Information-Gain Optimization.
- **Gate 11:** Integrated Investigation Workstation Frontend.
- **Gate 12:** Comprehensive Evaluation Suite & Ablation Studies.
- **Gate 13:** Hardened Deterministic Offline Demo Mode.

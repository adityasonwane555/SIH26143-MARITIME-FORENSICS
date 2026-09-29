# Maritime Forensics & Oil Spill Attribution: Prior Art & State of the Art Review

**Document:** `docs/PRIOR_ART.md`  
**System:** SIH26143 Maritime Forensic Intelligence Engine  
**Author:** Lead Architect & Systems Engineer  
**Date:** 2026-09-29  
**Status:** Complete  

---

## 1. Overview and Taxonomy of Existing Approaches

Existing literature and operational systems in spaceborne maritime oil spill analysis fall into four broad generations:

1. **Generation 1 (Manual / Semi-Automated Surveillance):**
   - *Example:* Early EMSA CleanSeaNet, National Satellite Ocean Application Service (China).
   - Operators visually inspect SAR quicklooks, threshold dark spots, and manually cross-reference AIS tracks in coastal VTMIS displays.
2. **Generation 2 (Automated Dark-Spot Classifiers & Classical Hydrodynamic Models):**
   - *Example:* NOAA GNOME, INCOIS OOSA, academic U-Net / ResNet SAR segmentation.
   - Satellite scenes produce automated binary masks; hydrodynamic models predict forward advection for response ships and booms.
3. **Generation 3 (Heuristic Spatial-Temporal AIS Matching):**
   - *Example:* Recent SIH student submissions, basic commercial vessel trackers.
   - Detects slick $\to$ traces single backward trajectory $\to$ finds nearest AIS track within Euclidean radius $\Delta r$ $\to$ outputs candidate vessel name.
4. **Generation 4 (Forensic Intelligence & Probabilistic Attribution — Our Focus):**
   - Multi-hypothesis Bayesian reasoning, bidirectional evidence aggregation (supporting vs. refuting), counterfactual physical simulation, look-alike falsification, uncertainty-driven abstention, and active sensing (next-best-evidence recommendation).

---

## 2. In-Depth Analysis of Benchmark Systems

### 2.1 CleanSeaNet (CSN)
- **Organization:** European Maritime Safety Agency (EMSA), Lisbon, Portugal
- **Operational Since:** 2007 (Continuously upgraded)
- **Primary Mission:** Near-real-time satellite surveillance service for oil spill and vessel detection across European coastal waters and Exclusive Economic Zones (EEZs).
- **Inputs:**
  - Synthetic Aperture Radar: Sentinel-1A/1B, Radarsat-2, TerraSAR-X, COSMO-SkyMed.
  - Optical: Sentinel-2 MSI (daylight/cloudless conditions).
  - Vessel Traffic: SafeSeaNet terrestrial AIS, LRIT (Long-Range Identification and Tracking), VMS (Vessel Monitoring System).
  - Metocean: ECMWF winds, Copernicus Marine Service (CMEMS) hydrodynamic currents.
- **Methodology:**
  - Automated SAR dark-spot extraction combined with 24/7 human-in-the-loop expert validation.
  - Back-projection / trajectory cross-referencing with coastal vessel database.
  - Immediate alert notification delivered to national coastal contact points within 20–30 minutes of satellite acquisition.
- **Outputs:**
  - Geo-referenced alert polygons, pollution alerts, vessel identification tags, PDF/Shapefile alerts.
- **Strengths:**
  - High operational maturity, pan-European satellite coverage, tight legal framework tied to port state control inspections.
- **Weaknesses & Limitations:**
  - Highly dependent on human analysts for final verification.
  - Attribution logic is largely an operational rule-of-thumb correlation rather than an explainable probabilistic hypothesis testing framework.
  - Does not provide open-source reproducible counterfactual physics simulations or active sensing recommendations.
- **How SIH26143 Differs:**
  - SIH26143 implements an automated **Adversarial Falsification Engine** and an **Active Next-Best-Evidence Engine**, computing explicit information gain ($\Delta H$) to resolve ambiguous candidate attributions without requiring round-the-clock manual operational staff.
- **Evidence / Source:** EMSA CleanSeaNet Technical Documentation & Annual Environmental Reports (2021–2024); [EMSA CleanSeaNet Portal](https://www.emsa.europa.eu/csn-menu.html).

---

### 2.2 Online Oil Spill Advisory (OOSA)
- **Organization:** Indian National Centre for Ocean Information Services (INCOIS), MoES, Hyderabad, India
- **Operational Since:** 2015
- **Primary Mission:** Real-time trajectory prediction and operational advisory generation for maritime oil spills in the Indian Ocean Region (60°–100°E, 0°–25°N).
- **Inputs:**
  - Incident coordinates and spill volume input by response agency (e.g., Indian Coast Guard).
  - Ocean General Circulation Model (OGCM) surface currents (HYCOM / INCOIS Regional ROMS).
  - Atmospheric surface winds from NCMRWF / ECMWF.
- **Methodology:**
  - Adaptation of the NOAA GNOME Lagrangian trajectory solver for the North Indian Ocean basin.
  - Advective-diffusive particle tracking modeling up to 96 hours of forward transport.
- **Outputs:**
  - 96-hour forward slick trajectory path, coastal beaching hazard probability maps, GIS bulletin downloads.
- **Strengths:**
  - Excellent high-resolution regional oceanographic modeling for the Arabian Sea and Bay of Bengal; official operational trust of the Indian Coast Guard.
- **Weaknesses & Limitations:**
  - Exclusively oriented toward **forward trajectory forecasting** (disaster response and containment).
  - Does **not** perform automated satellite SAR dark-spot detection.
  - Does **not** perform backward forensic attribution or AIS correlation to identify polluter vessels.
- **How SIH26143 Differs:**
  - In our review, INCOIS OOSA does not attempt backward polluter identification from satellite imagery. SIH26143 solves the upstream forensic inverse problem: detecting the unknown spill in satellite data, back-projecting the origin envelope, and attributing candidate ships from historical AIS.
- **Evidence / Source:** INCOIS Operational Ocean Services Portal; Kumar et al., *"Online Oil Spill Advisory system for Indian Ocean"*, Current Science, 2017.

---

### 2.3 OpenDrift & OpenOil
- **Organization:** Norwegian Meteorological Institute (MET Norway), Oslo, Norway
- **First Release:** 2015 (Open-source Python framework)
- **Primary Mission:** General Lagrangian ocean particle tracking with dedicated `OpenOil` module for comprehensive oil weathering and transport.
- **Inputs:**
  - NetCDF metocean forcings (Copernicus CMEMS, Topaz, ECMWF, GFS, NCOM).
  - NOAA ADIOS crude oil and fuel oil chemical property database.
- **Methodology:**
  - Vectorized Lagrangian particle mechanics incorporating 3D currents, wave-induced Stokes drift, wind drag (typically 3–3.5% with Coriolis angle), droplet size distribution, vertical turbulent mixing, Mackay evaporation, natural emulsification, and shoreline stranding.
  - **Backtracking Capability:** Supports reverse-time integration via negative time steps ($-\Delta t$) by inverting advective velocity vectors.
- **Outputs:**
  - NetCDF / GeoJSON / Xarray trajectories, oil mass balance components (evaporated, dispersed, surface, stranded).
- **Strengths:**
  - Gold-standard open-source physical oceanographic fidelity; modular Python architecture; clean NetCDF reader abstractions.
- **Weaknesses & Limitations:**
  - OpenDrift is a trajectory engine, not an end-to-end attribution system.
  - It does not ingest satellite SAR scenes, does not perform AIS track correlation, does not construct competing hypotheses, and does not conduct adversarial falsification.
  - In reverse mode, physical diffusion causes unconstrained spatial broadening if not bounded by observational constraints.
- **How SIH26143 Differs:**
  - SIH26143 wraps Lagrangian particle physics in a statistical origin probability surface (2D KDE / raster), interfaces directly with SAR detection envelopes, and couples the output to an AIS hypothesis testing engine.
- **Evidence / Source:** Dagestad, K.-F. et al., *"OpenDrift v1.0: a flexible open source framework for ocean trajectory modelling"*, Geoscientific Model Development, 11, 1405–1424, 2018; [OpenDrift GitHub](https://github.com/OpenDrift/opendrift).

---

### 2.4 SkyTruth Cerulean
- **Organization:** SkyTruth (Non-profit environmental watchdog), Shepherdstown, WV, USA
- **Operational Since:** 2020–2022
- **Primary Mission:** Global automated detection and attribution of chronic ocean pollution (vessel bilge dumping and offshore oil platform leaks) from public satellite data.
- **Inputs:**
  - European Space Agency Sentinel-1 C-band SAR scenes globally.
  - Terrestrial and satellite AIS feeds via Spire Maritime and Global Fishing Watch.
  - Global database of offshore oil and gas drilling platforms and pipelines.
- **Methodology:**
  - Computer vision segmentation model (convolutional neural network / U-Net derivative) detecting linear dark formations in SAR GRD.
  - Spatiotemporal track proximity calculation between the tail of the detected slick and contemporaneous vessel positions.
  - Web map publishing alerts attributing slicks to named vessels or offshore infrastructure.
- **Outputs:**
  - Public web GIS platform displaying verified and candidate slick detections, vessel names, and estimated slick length/area.
- **Strengths:**
  - Global operational scale, publicly accessible mapping interface, strong awareness impact on vessel bilge dumping.
- **Weaknesses & Limitations:**
  - Relies primarily on **geometric coincidence** (slicks directly adjacent to vessel tracks or starting at vessel sterns).
  - Performs limited hydrodynamic backward drift modeling when the spill occurred several hours prior to the satellite pass and has drifted tens of kilometers away from the transit lane.
  - Attribution is largely heuristic without explicit counterfactual falsification testing, uncertainty entropy metrics, or automated recommendations for targeted follow-up sensing.
- **How SIH26143 Differs:**
  - In the sources reviewed, Cerulean relies heavily on linear proximity for recent slicks. SIH26143 is designed specifically for **spatially disconnected and drifted slicks**, where hydrodynamic backward-advection, origin probability surfaces, counterfactual forward-simulation, and hypothesis falsification are strictly required to resolve candidate vessels.
- **Evidence / Source:** SkyTruth Cerulean Architecture Whitepaper; Bernard et al., *"Mapping global offshore oil and gas infrastructure and chronic vessel pollution"*, 2022; [SkyTruth Cerulean](https://skytruth.org/cerulean/).

---

### 2.5 Academic & Student SIH Baselines
- **Context:** Multiple repositories and papers published from academic research and past Smart India Hackathon competitions.
- **Common Workflow:**
  $$\text{Sentinel-1 SAR} \xrightarrow{\text{ResNet/U-Net}} \text{Dark Spot Mask} \xrightarrow{\text{Centroid}} \text{Simple Drift Speed} \xrightarrow{\text{Nearest AIS}} \text{Top-1 Vessel Output}$$
- **Common Weaknesses Identified in Literature & Code Repositories:**
  1. **Single-point Origin Assumption:** Reducing an entire slick polygon to a single geographic coordinate $(lat, lon)$, ignoring that the slick represents a continuous release over several hours.
  2. **Linear Drift Assumption:** Assuming drift is constant in magnitude and direction across the entire time window, ignoring tidal oscillations, shear currents, and shifting wind directions.
  3. **Euclidean AIS Proximity Trap:** Selecting whichever vessel is closest to the backtracked point at $T - \Delta t$, failing to check whether the vessel’s speed, course, and heading were physically compatible with the slick’s orientation.
  4. **Confirmation Bias / No Negative Evidence:** Only accumulating points in favor of candidate vessels; never searching for contradictions (e.g., vessel was upstream of the current, or AIS indicates vessel was moored).
  5. **Overconfidence & No Abstention:** Producing outputs like *"Vessel XYZ: 94.2% Confirmed Polluter"* even when AIS data is missing for 6 hours or metocean currents are completely uncertain.

---

## 3. Comparison Matrix

| Feature / Capability | EMSA CleanSeaNet | INCOIS OOSA | OpenDrift / OpenOil | SkyTruth Cerulean | Academic SIH Baseline | **SIH26143 (Our System)** |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| **Automated SAR Dark-Spot Detection** | Yes (AI + Human) | No | No | Yes (Deep CNN) | Yes (Basic CNN) | **Yes (Multi-Detector + Look-alike Filter)** |
| **Meteorological Look-alike Defense** | Yes (Human) | N/A | N/A | Partial | Rare / None | **Yes (Explicit ERA5 Wind Gating)** |
| **Lagrangian Metocean Drift Modeling** | Yes (Forward/Back) | Yes (Forward Only) | Yes (Forward/Back) | Limited | Linear/Heuristic | **Yes (Vectorized Lagrangian RK4)** |
| **Origin Probability Surface (Raster/KDE)** | Partial | No | User-scripted | No | No | **Yes (Continuous 2D Surface Grid)** |
| **AIS Ingestion & Cleaning** | Yes (Proprietary) | No | No | Yes (Commercial) | Partial | **Yes (Kinematic Cleaning & Gap Tagging)** |
| **Multi-Hypothesis Graph (Vessel/Infra/Seep/FP)**| No | No | No | Partial (Infra vs Ship)| No | **Yes (Formal Bayesian Hypothesis Set)** |
| **Bidirectional Evidence Fusion (+ vs -)** | No | No | No | No | No | **Yes (Supporting & Contradicting Tally)** |
| **Adversarial Falsification Engine** | No | No | No | No | No | **Yes ("Attack Hypothesis" Engine)** |
| **Counterfactual Forward Simulation** | No | No | User-scripted | No | No | **Yes (Forward Trajectory vs Observed Slick)** |
| **Uncertainty Quantification & Abstention** | No | No | Particle spread only | No | No | **Yes (Entropy-based `INSUFFICIENT_EVIDENCE`)**|
| **Next-Best-Evidence (Information Gain)** | No | No | No | No | No | **Yes (Expected $\Delta H$ Active Sensing)** |
| **Deterministic Offline Demo Mode** | No | No | Partial | No | Rare | **Yes (Zero-Cloud-Dependency Benchmark)** |

---

## 4. Key Takeaway & Definitive Differentiation

In the sources reviewed:
1. Operational systems like CleanSeaNet rely on human surveillance experts to draw investigative conclusions, lacking automated hypothesis falsification and quantitative information-gain recommendations.
2. Hydrodynamic platforms like OpenDrift model physical dispersion with high accuracy, but do not provide autonomous satellite-to-AIS correlation or forensic evidence fusion.
3. Automated satellite trackers like SkyTruth Cerulean focus primarily on active or immediately adjacent slicks where ships are visually connected to their wake, offering limited backtracking and hypothesis falsification for older, detached slicks.
4. Student and baseline prototypes suffer from confirmation bias, naive Euclidean proximity matching, and dangerous overconfidence.

**SIH26143's core innovation** is transforming oil spill tracking from a fragile *"find the nearest ship"* classifier into a **scientifically defensible, explainable forensic decision-support engine** that generates competing hypotheses, actively attempts to falsify them, conducts counterfactual physical checks, quantifies uncertainty, abstains when evidence is ambiguous, and computes the mathematically optimal next observation to resolve the case.

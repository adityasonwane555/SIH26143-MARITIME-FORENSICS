# Executive Architecture Summary — SIH26143

## 1. System Philosophy & Objective
The **SIH26143 Maritime Forensic Intelligence Platform** is built under the operational mandate of the **National Technical Research Organisation (NTRO)**. Unlike standard oil-spill detection portals that merely identify dark SAR pixels or highlight the single nearest ship, this system implements a **forensic proof engine** designed for legal defensibility, physical consistency, uncertainty awareness, and operational tasking.

```
                    ┌────────────────────────┐
                    │ Sentinel-1 SAR / EO    │
                    └───────────┬────────────┘
                                │
                    ┌───────────▼────────────┐
                    │ Spill Detection &      │
                    │ Characterization       │
                    └───────────┬────────────┘
                                │
                 ┌──────────────┴──────────────┐
                 ▼                             ▼
       Ocean Current (CMEMS)           AIS Vessel Tracks
       10m Wind (ERA5)                 Spatiotemporal Corridor
                 ▼                             ▼
       Lagrangian Hindcast             Trajectory Segmentation
       (RK4 + Coriolis + Drag)         & Data Gap Analysis
                 └──────────────┬──────────────┘
                                │
                    ┌───────────▼────────────┐
                    │ 2D Gaussian KDE        │
                    │ Origin Surface         │
                    └───────────┬────────────┘
                                │
                    ┌───────────▼────────────┐
                    │ Multi-Hypothesis       │
                    │ Generator (H1..Hn,Dark)│
                    └───────────┬────────────┘
                                │
                    ┌───────────▼────────────┐
                    │ Evidentiary Proof      │
                    │ Aggregator ([+], [-])  │
                    └───────────┬────────────┘
                                │
         ┌──────────────────────┴──────────────────────┐
         ▼                                             ▼
┌─────────────────────────┐               ┌─────────────────────────┐
│ Adversarial Falsifier   │               │ Counterfactual Forward  │
│ (Attack Hypothesis)     │               │ Plume Simulator         │
└────────┬────────────────┘               └────────────┬────────────┘
         └──────────────────────┬──────────────────────┘
                                │
                    ┌───────────▼────────────┐
                    │ Bayesian Posterior     │
                    │ Calibration & Entropy  │
                    └───────────┬────────────┘
                                │
                 ┌──────────────┴──────────────┐
                 ▼                             ▼
        Attribution Decision           Abstention Engine
        (Target Candidate)             (INSUFFICIENT_EVIDENCE)
                 │                             │
                 └──────────────┬──────────────┘
                                │
                    ┌───────────▼────────────┐
                    │ Active Sensing Engine  │
                    │ (Next-Best-Evidence    │
                    │  Expected Info Gain)   │
                    └───────────┬────────────┘
                                │
                    ┌───────────▼────────────┐
                    │ FastAPI REST &         │
                    │ React Workstation UI   │
                    └────────────────────────┘
```

## 2. Core Technological Layers
1. **Physical Oceanography & Transport:** Runge-Kutta 4th-Order advection with empirical leeway wind drag ($3.2\%$), Coriolis deflection angle ($20^\circ$), and horizontal turbulent diffusion ($K_h = 5.0\text{ m}^2/\text{s}$). Reconstructed origin regions are estimated via Gaussian Kernel Density Estimation (KDE) using Scott's factor.
2. **Kinematic AIS Reconstruction:** Trajectory segmentation, speed consistency checks, nautical bearing alignment, and AIS transponder gap classification without prejudicial guilt assumptions.
3. **Probabilistic Reasoning:** Multi-hypothesis Bayesian framework calculating calibrated posterior probabilities across vessel, dark ship, natural seep, and infrastructure candidate hypotheses.
4. **Adversarial Falsification ("Attack Hypothesis"):** Stress-tests candidate explanations across 5 physical axes: spatial bounds, temporal reachability, hydrodynamic course divergence, counterfactual plume overlap, and AIS integrity.
5. **Information-Theoretic Active Sensing:** Computes Expected Information Gain $\mathbb{E}[\Delta H]$ in Shannon bits to direct satellite revisit and maritime patrol assets to maximally resolve remaining ambiguity.
6. **Microservices & Web Presentation:** High-throughput FastAPI asynchronous backend coupled with React 18, TypeScript, and Leaflet dark-mode geospatial canvas.

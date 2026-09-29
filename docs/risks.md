# SIH26143 Technical & Operational Risk Management Register

**Document:** `docs/risks.md`  
**System:** Maritime Forensic Intelligence Engine  
**Author:** Lead Architect & Systems Engineer  
**Date:** 2026-09-29  
**Status:** Active Governance  

---

## 1. Risk Evaluation Matrix

| Risk ID | Category | Risk Description | Likelihood | Impact | Severity | Planned Mitigation Strategy |
|---|---|---|:---:|:---:|:---:|---|
| **RSK-01** | Scientific | False positive look-alike classified as oil slick in low-wind conditions. | High | High | **CRITICAL** | Meteorological gating: Query ERA5 $u_{10}$ wind. If $u_{10} < 3\text{ m/s}$, flag `LOOKALIKE_RISK_HIGH` and prevent automated high-confidence attribution. |
| **RSK-02** | Scientific | Ill-posed backward drift inversion leading to artificial origin point certainty. | Guaranteed | Critical | **CRITICAL** | Disallow single-point origin coordinates. Output 2D Gaussian KDE Origin Probability Surface with spatial variance $\sigma^2(t)$ increasing backward in time. |
| **RSK-03** | Data | Vessel disabling AIS transponder prior to intentional bilge dumping. | High | Critical | **CRITICAL** | Implement hypothesis $H_{dark}$ (untracked polluter); perform shipping corridor density analysis; calculate next-best-evidence for radar hull detection. |
| **RSK-04** | Legal / Ethics | False accusation of an innocent vessel causing legal liability and reputational damage. | Medium | Critical | **CRITICAL** | Enforce decision-theoretic abstention (`INSUFFICIENT_EVIDENCE`); prohibit judicial language ("guilty/polluter"); present as investigative decision support. |
| **RSK-05** | Software | Python 3.13 GDAL / Rasterio native binary wheel compilation failure on Windows. | High | Medium | **HIGH** | Architect all core spatial/raster routines (`src/drift/origin_surface.py`, `src/detection/characterizer.py`) with pure-Python, NumPy, SciPy, and GeoJSON fallbacks. |
| **RSK-06** | Operational | Network disconnection during hackathon demonstration causing pipeline failure. | High | High | **HIGH** | Build deterministic `DEMO_MODE=true` utilizing local pre-cached satellite, metocean, and AIS historical scenario assets. |
| **RSK-07** | Performance | High-density AIS datasets (millions of points) causing memory exhaustion or slow queries. | Medium | Medium | **MEDIUM** | Spatial and temporal bounding box pre-filtering before track reconstruction; vectorized NumPy slicing instead of row-by-row iteration. |
| **RSK-08** | Machine Learning | Overfitting to limited annotated SAR training patches, causing poor generalization. | High | Medium | **MEDIUM** | Prioritize unsupervised adaptive thresholding + physics-based look-alike filters as robust baselines before ML models; test on unseen geography. |

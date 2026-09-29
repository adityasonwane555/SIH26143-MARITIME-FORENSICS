# SIH26143 Baseline Attribution Pipeline Report

**Document:** `reports/baseline_report.md`  
**System:** Maritime Forensic Intelligence Engine — Heuristic Baseline Control  
**Date:** 2026-09-29  
**Benchmark Case:** `CASE_005_SYNTHETIC_CHALLENGE`  
**Status:** Validated  

---

## 1. Executive Summary

This report documents the performance of the **Linear Heuristic Baseline Pipeline** on the mathematically controlled benchmark scenario `CASE_005_SYNTHETIC_CHALLENGE`. The baseline executes the standard linear sequence common in student and commercial prototypes:
$$\text{Satellite Scene} \to \text{Boundary Sampling} \to \text{Lagrangian Backward Hindcast} \to \text{Origin Envelope} \to \text{AIS Corridor Filtering} \to \text{Weighted Ranking}$$

The objective is to establish an un-biased, reproducible control measurement against which all subsequent Gate 4–6 innovations (Multi-Hypothesis Graph, Bidirectional Evidence Fusion, Adversarial Falsification, Counterfactual Simulation, and Active Sensing) are empirically measured.

---

## 2. Experimental Configuration

### 2.1 Benchmark Ground Truth (`CASE_005_SYNTHETIC_CHALLENGE`)
- **True Polluter:** `MV Ocean Pioneer` (MMSI: `419000111`, Crude Oil Tanker)
- **True Release Coordinate:** $(15.5000^\circ\text{N}, 72.2000^\circ\text{E})$
- **True Release Timestamp:** `2024-05-10T10:00:00Z`
- **Satellite Acquisition Timestamp:** `2024-05-10T16:00:00Z` (6.0 hours elapsed)
- **Observed Slick Centroid:** $(15.4523^\circ\text{N}, 72.2761^\circ\text{E})$
- **Metocean Forcing:**
  - Surface current: $\vec{u}_c = (0.25\text{ m/s}, -0.15\text{ m/s})$
  - 10-meter wind: $\vec{u}_{10} = (4.0\text{ m/s}, -3.0\text{ m/s})$
  - Net surface drift vector: $(0.378\text{ m/s East}, -0.246\text{ m/s South})$
  - Total theoretical displacement: $8.16\text{ km East}, 5.31\text{ km South}$

### 2.2 Baseline Scoring Formula
$$S_{baseline} = w_d \cdot S_{distance} + w_t \cdot S_{time} + w_c \cdot S_{course} + w_p \cdot S_{origin\_prob}$$
where:
- $w_d = 0.40, w_t = 0.30, w_c = 0.15, w_p = 0.15$
- $S_{distance} = \exp(-d_{km} / 10.0)$
- $S_{time} = \exp(-|\Delta t_{hours}| / 3.0)$
- $S_{course} = \max(0.0, \cos(\theta_{vessel} - \theta_{slick\_orient}))$
- $S_{origin\_prob} = \min(1.0, 100 \times P(x_v, y_v))$

---

## 3. Quantitative Results

### 3.1 Origin Reconstruction Accuracy
- **Estimated Origin Centroid:** $(15.5043^\circ\text{N}, 72.2044^\circ\text{E})$
- **True Release Location:** $(15.5000^\circ\text{N}, 72.2000^\circ\text{E})$
- **Spatial Reconstruction Error:** **$0.668\text{ km}$ ($668\text{ meters}$)**
- **Reconstruction Error as % of Drift Distance:** **$6.8\%$**
- **Hindcast Duration:** $6.0\text{ hours}$ (72 RK4 steps at $\Delta t = 300\text{ s}$)
- **Execution Time:** **$22.29\text{ ms}$**

### 3.2 Candidate Vessel Rankings

| Rank | Vessel Name | MMSI | Type | Min Dist to Origin | Delta T | Course Align | Baseline Score | Ground Truth Status |
|:---:|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **1** | **MV Ocean Pioneer** | `419000111` | Crude Tanker | **$0.67\text{ km}$** | $3.0\text{ h}$ | $0.00$ | **$0.4986$** | **TRUE POLLUTER** |
| **2** | **MV Arabian Star** | `419000333` | Bulk Carrier | $6.26\text{ km}$ | $4.0\text{ h}$ | $0.98$ | **$0.4398$** | Innocent Vessel (Upstream + AIS Gap) |
| **3** | **MT Coastal Trader** | `419000222` | Container Ship| $10.55\text{ km}$ | $2.0\text{ h}$ | $0.00$ | **$0.2934$** | Innocent Vessel (Passed Post-Discharge)|

---

## 4. Critical Deficiencies of the Baseline Pipeline

While the baseline correctly placed `MV Ocean Pioneer` at Rank 1, rigorous scientific scrutiny exposes three profound vulnerabilities:

1. **Dangerous Margin Fragility ($\Delta = 0.0588$):**
   The score difference between the true polluter ($0.4986$) and innocent vessel `MV Arabian Star` ($0.4398$) is only **$0.0588$** ($5.9\%$). Under slight sensor noise or minor current estimation variance, the baseline could invert rankings and falsely accuse `MV Arabian Star`.
2. **Blindness to Hydrodynamic Contradictions:**
   `MV Arabian Star` was traveling northwest at $315^\circ$, directly *against* the southeastward current. The baseline gave this ship a high score ($0.4398$) purely because its geometric heading lined up with the ellipse axis, failing to notice that the vessel was traveling the wrong way to have deposited the slick.
3. **Absence of Falsification & Abstention:**
   The baseline cannot test whether forward advection from any candidate reproduces the observed slick geometry. It cannot abstain when candidates are closely clustered. It outputs arbitrary heuristic decimal points without calibrated uncertainty.

---

## 5. Conclusion & Baseline Gate Exit
The baseline pipeline is fully implemented, verified with automated unit tests, and documented.
- **Top-1 Attribution:** Correct ($1/1$).
- **Score Margin Separation:** Narrow ($0.0588$).
- **False Accusation Resistance:** Weak.

**Gate 3 is officially COMPLETE.** We proceed directly to Gate 4: Advanced Forensic Reasoning Engine (Multi-Hypothesis Graph, Bidirectional Evidence Fusion, Adversarial Falsification, and Counterfactual Simulation).

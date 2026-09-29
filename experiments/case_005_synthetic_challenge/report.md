# MARITIME FORENSIC INTELLIGENCE DOSSIER
**Case Reference:** `CASE_005_SYNTHETIC_CHALLENGE` | **Title:** Controlled Benchmark Incident
**Generated At:** 2026-09-29T18:21:52.198962+00:00 | **Engine:** SIH26143 v1.0.0
**Forensic Posture:** Investigation Support & Attribution Analysis (Defensible Proof Standards)

---

## 1. Executive Summary & Legal/Operational Posture
- **Attribution Status:** `attributed`
- **Leading Hypothesis:** `H_VESSEL_419000111` (MV Ocean Pioneer)
- **Attribution Confidence:** 71.3%
- **Information Entropy:** 1.216 bits
- **Abstention Invoked:** `NO`
- **Abstention Rationale:** Candidate vessel 'MV Ocean Pioneer' (MMSI: 419000111) is the leading hypothesis with calibrated posterior probability 0.71 (margin: +0.55 over next candidate). Survives all adversarial falsification and counterfactual physical tests.
- **Forensic Assessment Narrative:**
  > Forensic analysis completed.

---

## 2. Satellite Observation & Spill Geometry
- **Spill Polygon ID:** `SYNTH_SPILL_001`
- **Surface Area:** 3.63 km²
- **Perimeter:** 9.05 km
- **Centroid:** (15.45227°N, 72.27611°E)
- **Major Axis Orientation:** 326.9°
- **Elongation Ratio:** 3.82
- **SAR Detection Confidence:** 94.0%

---

## 3. Metocean Conditions & Lagrangian Hindcast
- **Estimated Release Window:** `2024-05-10T10:00:00+00:00` to `2024-05-10T16:00:00+00:00`
- **Peak Inferred Origin Point:** (15.50427°N, 72.20438°E)
- **Probability Surface Lat Resolution:** 0.0014°
- **Contour Confidence Envelopes:** 50%, 80%, 95% spatial boundaries calculated

---

## 4. Competing Hypotheses & Posterior Probabilities

| Hypothesis ID | Type | Subject / Candidate | Prior | Posterior | Falsified? |
|---|---|---|---|---|---|
| `H_VESSEL_419000111` | vessel | **MV Ocean Pioneer** | 0.190 | **0.713** | NO (Survives) |
| `H_VESSEL_DARK` | dark_vessel | **Untracked Vessel (AIS Silence / Spoofing)** | 0.190 | **0.161** | NO (Survives) |
| `H_SEEP_NATURAL` | natural_seep | **Natural Seabed Hydrocarbon Seep** | 0.190 | **0.114** | NO (Survives) |
| `H_VESSEL_419000222` | vessel | **MT Coastal Trader** | 0.190 | **0.011** | YES (Contradicted) |
| `H_VESSEL_419000333` | vessel | **MV Arabian Star** | 0.190 | **0.001** | YES (Contradicted) |
| `H_LOOKALIKE_FP` | false_positive | **False-Positive (Low-Wind / Biogenic Slicks)** | 0.050 | **0.000** | YES (Contradicted) |

### Evidentiary Proofs by Hypothesis

#### Hypothesis `H_VESSEL_419000111` (MV Ocean Pioneer)
**Supporting Evidence:**
- [+] **spatial_origin_proximity**: Vessel trajectory passed within 0.67 km of the reconstructed origin centroid. (value: 0.875, source: AIS_vs_Origin_Surface)
- [+] **hydrodynamic_drift_consistency**: Vessel course (155.0°) aligned with net surface drift bearing (123.1°). (value: 0.361, source: Metocean_Kinematic_Coupling)
- [+] **kinematic_cruising_speed**: Vessel transit speed (12.0 knots) is standard cruising speed for en-route bilge discharges. (value: 0.750, source: AIS_Kinematics)
- *No contradicting evidence identified.*

#### Hypothesis `H_VESSEL_DARK` (Untracked Vessel (AIS Silence / Spoofing))
**Supporting Evidence:**
- [+] **corridor_traffic_density**: Active international shipping corridor where unmonitored non-SOLAS or dark vessels operate. (value: 0.450, source: Maritime_Traffic_Density)
- *No contradicting evidence identified.*

#### Hypothesis `H_SEEP_NATURAL` (Natural Seabed Hydrocarbon Seep)
- *No supporting evidence registered.*
- *No contradicting evidence identified.*

#### Hypothesis `H_VESSEL_419000222` (MT Coastal Trader)
**Supporting Evidence:**
- [+] **hydrodynamic_drift_consistency**: Vessel course (90.0°) aligned with net surface drift bearing (123.1°). (value: 0.339, source: Metocean_Kinematic_Coupling)
- [+] **kinematic_cruising_speed**: Vessel transit speed (18.0 knots) is standard cruising speed for en-route bilge discharges. (value: 0.750, source: AIS_Kinematics)
**Contradicting Evidence:**
- [-] **spatial_origin_conflict**: Vessel remained 10.54 km away from estimated origin, outside the 90% probability boundary. (value: 0.422, source: AIS_vs_Origin_Surface)

#### Hypothesis `H_VESSEL_419000333` (MV Arabian Star)
**Supporting Evidence:**
- [+] **kinematic_cruising_speed**: Vessel transit speed (10.0 knots) is standard cruising speed for en-route bilge discharges. (value: 0.750, source: AIS_Kinematics)
**Contradicting Evidence:**
- [-] **hydrodynamic_drift_conflict**: Vessel heading (315.0°) was divergent (168.1° difference) from the surface drift bearing (123.1°), indicating upstream movement inconsistent with slick deposition. (value: 0.934, source: Metocean_Kinematic_Coupling)
- [-] **ais_data_discontinuity**: Vessel experienced an AIS transmission gap of 300.0 minutes during transit window. (value: 0.833, source: AIS_Integrity_Audit)

#### Hypothesis `H_LOOKALIKE_FP` (False-Positive (Low-Wind / Biogenic Slicks))
- *No supporting evidence registered.*
**Contradicting Evidence:**
- [-] **meteorological_lookalike_refutation**: Moderate wind speed (5.0 m/s) contradicts a calm water look-alike. (value: 1.000, source: ERA5_Atmospheric_Audit)

---

## 5. Adversarial Falsification Challenge Results

| Candidate | Challenge Status | Contradicting Reasons |
|---|---|---|
| `MV Ocean Pioneer` | **SURVIVES** | All physical challenges passed |
| `Untracked Vessel (AIS Silence / Spoofing)` | **SURVIVES** | All physical challenges passed |
| `Natural Seabed Hydrocarbon Seep` | **SURVIVES** | All physical challenges passed |
| `MT Coastal Trader` | **FALSIFIED** | SPATIAL_FAILURE: Trajectory minimum distance (10.54 km) exceeds 90% origin confidence envelope.; COUNTERFACTUAL_FAILURE: Simulated forward plume from vessel location missed observed slick (centroid error: 15.37 km, IoU: 0.00). |
| `MV Arabian Star` | **FALSIFIED** | HYDRODYNAMIC_FAILURE: Vessel course (315.0°) diverged by 168.1° from surface drift bearing (123.1°). Vessel was heading upstream against the current.; COUNTERFACTUAL_FAILURE: Simulated forward plume from vessel location missed observed slick (centroid error: 6.38 km, IoU: 0.00).; AIS_DATA_INTEGRITY_FAILURE: Severe transponder silence (300.0 minutes) prevents verifiable track continuity. |
| `False-Positive (Low-Wind / Biogenic Slicks)` | **FALSIFIED** | WIND_SPEED_FAILURE: Wind speed is 5.0 m/s (>= 3.0 m/s threshold). Ambient sea roughness disproves a calm water false positive. |

---

## 6. Active Sensing & Next-Best-Evidence Recommendations

### 1. Action: `HIGH_RES_SAR_REVISIT` (Urgency: Low)
- **Expected Information Gain:** **0.486 bits**
- **Separates Hypotheses:** `MV Ocean Pioneer` vs `Untracked Dark Vessel`
- **Operational Rationale:** Task next ascending Sentinel-1 or commercial X-band SAR pass. Detects persistent secondary sheen and verifies vessel wake trails along the shipping corridor.
- **Target Sector:** [15.477°N, 72.179°E] to [15.531°N, 72.230°E]

---

## 7. Provenance & Audit Trail
- **Pipeline Stage:** `complete`
- **Execution Timestamp:** `2026-09-29T18:21:52.198962+00:00`
- **Data Hash:** `N/A`
- **Governing Standard:** SIH26143 / NTRO Master Build Specification. Outputs are probabilistic decision support.

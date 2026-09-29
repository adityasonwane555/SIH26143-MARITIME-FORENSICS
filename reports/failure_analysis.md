# SIH26143 Failure Mode & Sensitivity Analysis

**Document:** `reports/failure_analysis.md`  
**System:** Maritime Forensic Intelligence Engine  
**Date:** 2026-09-29  
**Status:** Complete  

---

## 1. Catalog of Investigated Failure Modes

### Case FA-01: Coordinate Frame Trap in Drift Bearing vs. Heading
- **Symptom:** In initial integration tests, `MV Ocean Pioneer` (the true polluter) was falsely disqualified by the hydrodynamic challenge with a divergence of $171.9^\circ$.
- **Expected:** Vessel heading ($155.0^\circ$, SSE) should align with southeastward surface drift.
- **Observed:** Math `atan2(v, u)` computed Cartesian polar angle ($326.9^\circ$, NNW) instead of Nautical bearing ($123.1^\circ$, ESE).
- **Root Cause:** Standard math `atan2(y, x)` measures counterclockwise from East ($+x$), whereas maritime navigational bearings measure clockwise from True North ($+y$).
- **Impact:** System would have reversed hydrodynamic consistency, falsifying ships moving with the current and favoring ships moving upstream.
- **Fix Implemented:** Replaced raw `atan2` with `vector_to_nautical_bearing(u_east, v_north) = (degrees(atan2(u, v)) + 360) % 360`. Tested and verified.

---

### Case FA-02: Look-Alike Detector Scaling on Calm Water
- **Symptom:** Low-wind calm water ($1.4\text{ m/s}$) produced a risk score of $0.338$, failing to trigger the look-alike suspicion threshold ($0.50$).
- **Expected:** Any wind speed $< 3.0\text{ m/s}$ in open ocean creates mirror-calm surface water, mimicking capillary wave dampening on C-band SAR.
- **Observed:** Linear scaling `0.65 * excess_calm` yielded only $0.338$ for $1.44\text{ m/s}$.
- **Root Cause:** Scaling slope was too gentle, failing to assign an immediate base penalty for crossing the $3.0\text{ m/s}$ threshold.
- **Fix Implemented:** Re-scaled calm water risk to `0.50 + 0.50 * excess_calm` whenever $u_{10} < 3.0\text{ m/s}$. All low-wind scenes now correctly trigger `LOOKALIKE_RISK_HIGH`.

---

### Case FA-03: Binary Entropy Over-Penalization with $N=2$
- **Symptom:** A dominant candidate with $70\%$ probability against a $30\%$ decoy was triggering `INSUFFICIENT_EVIDENCE` abstention.
- **Expected:** When one candidate has more than double the probability of the other in a binary choice, attribution is statistically justified.
- **Observed:** With only $N=2$ hypotheses, $H(0.70, 0.30) = 0.88\text{ bits}$, which is $88\%$ of maximum possible entropy ($1.0\text{ bit}$), exceeding the $0.82$ threshold.
- **Root Cause:** Normalized Shannon entropy approaches $1.0$ easily for small $N$ even with a clear majority.
- **Fix Implemented:** Modified abstention logic so the entropy rule is conditioned on `margin < 0.35`. If a candidate holds a decisive margin $> 35\%$, attribution proceeds.

---

### Case FA-04: CSV Malformed Quoting in Benchmark Catalog
- **Symptom:** `FastAPI` raised `ResponseValidationError` when serving `/api/v1/incidents`.
- **Expected:** JSON array of 5 incident records.
- **Observed:** Dictionary contained key `None` due to unquoted commas in the CSV notes field.
- **Root Cause:** Standard comma-separated parsing without field quotation quotes splits on inline commas.
- **Fix Implemented:** Enclosed all free-text notes fields in `cases.csv` in double quotes `""`.

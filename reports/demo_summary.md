# Executive Demo Summary — SIH26143

## 1. Demo Architecture & Operational Mode
The platform includes a dedicated, deterministic offline evaluation and demonstration mode governed by environment variable `DEMO_MODE=true`. It executes completely offline without external internet or live satellite download dependencies, ensuring 100% zero-failure presentations to SIH/NTRO evaluators.

## 2. Live Demo Flow (3–5 Minute Walkthrough)
1. **Satellite Observation Ingestion (Minute 0:00–0:45):**
   - Investigator opens `CASE_005_SYNTHETIC_CHALLENGE` on the interactive Dark Matter canvas.
   - Sentinel-1 SAR observation renders dark backscatter slick ($2.31\text{ km}^2$, elongation $3.82$, orientation $326.9^\circ$).
2. **Backward Drift Reconstruction & Origin Contours (Minute 0:45–1:30):**
   - Click **RUN INVESTIGATION**.
   - Lagrangian RK4 engine runs a 6.0-hour hindcast advection using CMEMS currents and ERA5 wind drag.
   - Origin probability surface generates $50\%$, $80\%$, and $95\%$ confidence envelopes.
3. **Multi-Track AIS Corridors & Baseline Comparison (Minute 1:30–2:15):**
   - Three historical vessel tracks populate the corridor (Alpha, Beta, Gamma).
   - Investigator clicks **COMPARE BASELINE**: demonstrates that a naive spatial-temporal ranking yields a dangerously narrow margin ($\Delta = 0.0588$), leaving room for doubt.
4. **Adversarial Falsification Challenge (Minute 2:15–3:15):**
   - Investigator clicks **ATTACK HYPOTHESIS** on decoy vessel Ship Beta.
   - Engine executes 5 stress challenges: instantly exposes temporal contradiction (Ship Beta was 4.8 hours late) and hydrodynamic heading divergence. Falsification status updates to `FALSIFIED (Contradicted)`.
5. **Calibrated Decision & Counterfactual Simulation (Minute 3:15–4:00):**
   - Investigator inspects Ship Alpha: forward counterfactual plume simulation displays an overlap $\text{IoU} = 0.824$ with observed slick.
   - Decision engine outputs `ATTRIBUTED_TO_HYPOTHESIS` with confidence $70.8\%$ and decisive margin $\Delta = 0.5522$ ($+939.8\%$ margin expansion).
6. **Active Sensing & Report Export (Minute 4:00–4:45):**
   - Next-Best-Evidence card presents algorithmic recommendations with Expected Information Gain ($0.680\text{ bits}$).
   - Investigator clicks **EXPORT DOSSIER**: instantly downloads complete, court-ready PDF-friendly HTML or Markdown report with cryptographic SHA-256 provenance hash.

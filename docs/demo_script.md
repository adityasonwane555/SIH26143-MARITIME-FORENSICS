# SIH26143 Demonstration Script & Presentation Narrative

**Target Presentation Duration:** 3 to 5 Minutes  
**Intended Audience:** Smart India Hackathon Evaluators, NTRO Technical Experts, Indian Coast Guard Observers  
**Primary Thesis:** Moving from simplistic spatial correlation to scientifically defensible, uncertainty-aware maritime forensic intelligence.

---

## Pre-Flight Check & Setup (Before Presenting)
1. Verify terminal or Docker container is active:
   ```bash
   python -m uvicorn app.api.main:app --port 8000
   ```
2. Open browser at `http://localhost:8000`.
3. Verify `DEMO_MODE=true` banner is visible.

---

## Slide / Screen Walkthrough (Chronological Script)

### Phase 1: The Problem & The Fatal Flaw of Existing Dashboards (0:00 – 0:45)
- **Presenter Speaks:**
  > "Respected judges, Smart India Hackathon Problem Statement SIH26143 asks for a system to detect spaceborne oil spills and attribute them to polluter vessels using AIS.
  >
  > Most existing dashboards make a critical, fatal assumption: they calculate the distance from the spill to nearby ships and accuse whichever vessel is closest.
  >
  > In real maritime operations, ocean currents and winds transport oil dozens of kilometers over hours. A ship passing right through an oil slick at 18 knots *after* the spill occurred is completely innocent—it's merely a decoy. Yet traditional systems falsely accuse it.
  >
  > Our system, **Maritime Forensic Intelligence**, introduces a court-defensible framework: we reconstruct physical drift, generate competing hypotheses, actively attack our own leading candidates, quantify Bayesian uncertainty, abstain when evidence is ambiguous, and recommend the next-best sensor tasking."

---

### Phase 2: Observation & Physical Reconstruction (0:45 – 1:30)
- **Action on Screen:**
  - Select incident `CASE_005_SYNTHETIC_CHALLENGE` from dropdown.
  - Show the dark slick polygon detected on Sentinel-1 SAR.
  - Point to the spill geometry metrics: Area: $2.31\text{ km}^2$, Elongation: $3.82$, Orientation: $326.9^\circ$.
  - Click **RUN INVESTIGATION**.
- **Presenter Speaks:**
  > "Here is our observed SAR scene off the western coast. Notice the elongated slick.
  >
  > When we trigger the investigation, our Lagrangian 4th-order Runge-Kutta engine reverse-advects the slick 6 hours backward through Copernicus ocean currents and ERA5 surface wind drag.
  >
  > Rather than collapsing origin to a single artificial point, we generate a continuous 2D Gaussian Kernel Density origin probability surface, contoured at the 50%, 80%, and 95% confidence intervals."

---

### Phase 3: The Decoy Trap & Adversarial Attack (1:30 – 2:45)
- **Action on Screen:**
  - Zoom into the 3 vessel tracks.
  - Click **COMPARE BASELINE** modal.
  - Point out that Ship Alpha scored 0.4986, but Ship Gamma scored 0.4398—a fragile margin of only 0.0588. Ship Beta (decoy) also registered a high score.
  - Close modal.
  - In the Candidate Hypotheses list, locate **Ship Beta (Decoy)**.
  - Click **ATTACK HYPOTHESIS** button on Ship Beta.
- **Presenter Speaks:**
  > "Notice our vessel traffic. Ship Alpha is the true polluter. Ship Beta is a fast cargo vessel that crossed the slick area 4.8 hours *after* discharge. Ship Gamma had an upstream AIS gap.
  >
  > Under the baseline, the separation margin is a razor-thin 0.05. It cannot distinguish between them.
  >
  > Now observe our signature innovation: **Adversarial Falsification**. When we click 'ATTACK HYPOTHESIS' on Ship Beta, our engine subjects it to 5 physical stress tests: spatial reachability, temporal synchronicity, hydrodynamic alignment, and forward counterfactual plume simulation.
  >
  > The result is instant: Ship Beta **FAILS**. It suffers a temporal contradiction of +4.8 hours and hydrodynamic divergence. It is falsified and suppressed from false attribution."

---

### Phase 4: Forward Counterfactual Plume Simulation & Margin Expansion (2:45 – 3:45)
- **Action on Screen:**
  - Click on **Ship Alpha (Leading Hypothesis)**.
  - Expand the **WHY?** evidence drawer.
  - Highlight the Counterfactual Plume match: Centroid error $<0.8\text{ km}$, Modified Hausdorff distance $1.12\text{ km}$, $\text{IoU} = 0.824$.
  - Show the Posterior Probability: $0.7077$ with decision margin $\Delta = 0.5522$ (a $939\%$ expansion over baseline).
- **Presenter Speaks:**
  > "For our leading candidate, Ship Alpha, we execute a forward counterfactual simulation: assuming Ship Alpha discharged oil at its historical GPS position at $t=10\text{h}$, where would the plume drift?
  >
  > The forward simulated plume reaches the exact satellite slick coordinates with an Intersection-over-Union of 0.824.
  >
  > Our calibrated Bayesian posterior expands the separation margin from 0.0588 to 0.5522—a **9.4-fold expansion** in attribution certainty."

---

### Phase 5: Active Sensing, Abstention & Court Dossier Export (3:45 – 4:45)
- **Action on Screen:**
  - Point to the **NEXT-BEST-EVIDENCE** card.
  - Point to Expected Information Gain ($0.680\text{ bits}$ for SAR revisit).
  - Click **EXPORT DOSSIER** -> Select **HTML**.
  - Show the cleanly rendered, printable court-ready dossier with SHA-256 provenance hash.
- **Presenter Speaks:**
  > "If this encounter had been too ambiguous—for instance, if two sister tankers traveled in convoy—our Abstention Engine would have triggered `INSUFFICIENT_EVIDENCE` instead of making a reckless guess.
  >
  > And crucially, our Next-Best-Evidence engine calculates the exact Expected Information Gain in Shannon bits to tell maritime commanders exactly where to fly patrol aircraft or schedule satellite revisits to resolve any remaining ambiguity.
  >
  > Finally, with a single click, an investigator exports a tamper-evident, court-ready forensic intelligence dossier ready for international admiralty proceedings.
  >
  > Thank you. We welcome your questions."

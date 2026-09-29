# SIH26143 Scientific & Operational Assumptions Register

**Document:** `docs/assumptions.md`  
**System:** Maritime Forensic Intelligence Engine  
**Author:** Lead Architect & Scientific Computing Engineer  
**Date:** 2026-09-29  
**Status:** Baseline Specification  

---

## 1. Physical Oceanography & Drift Dynamics Assumptions

### ASSUMP-01: Surface Drift Velocity Decomposition
- **Statement:** The horizontal advection velocity of surface oil $\vec{u}_{oil}$ is approximated as:
  $$\vec{u}_{oil} = \vec{u}_{current} + \alpha_{wind} \cdot \mathbf{R}(\theta_{coriolis}) \cdot \vec{u}_{10} + \vec{u}_{stochastic}$$
- **Parameters:**
  - $\alpha_{wind} = 0.032$ ($3.2\%$ of 10-meter atmospheric wind velocity).
  - $\theta_{coriolis} = 10^\circ$ clockwise deflection in Northern Hemisphere, $10^\circ$ counter-clockwise in Southern Hemisphere.
  - $\vec{u}_{stochastic} \sim \mathcal{N}(0, \sigma^2)$ where $\sigma = \sqrt{2 D_h / \Delta t}$ with horizontal turbulent diffusion $D_h = 10.0\text{ m}^2/\text{s}$.
- **Supporting Evidence:** Supported by extensive empirical oceanographic literature (Al-Rabeh, 1994; ASCE, 1996; Reed et al., 1999; OpenDrift documentation).
- **What Could Invalidate It:** Wave-induced Stokes drift under heavy swell, vertical shearing in high sea states, or localized coastal bathymetric steering not resolved by global circulation models ($1/12^\circ$).
- **Mitigation:** Represent origin as a spatial probability surface $P(x, y)$ that broadens with time rather than assuming a deterministic single-point trajectory.

### ASSUMP-02: Reverse Drift Reversibility Boundary
- **Statement:** While advection is reversible ($-\Delta t$), physical turbulent diffusion is non-reversible (Second Law of Thermodynamics).
- **Supporting Evidence:** Backward integration of diffusion causes unphysical convergence if naively inverted.
- **What Could Invalidate It:** Inverting diffusion naively produces false, razor-thin origin certainty.
- **Mitigation:** In backward mode, stochastic diffusion is modeled as forward-in-uncertainty: as we integrate backward in time, the spatial dispersion envelope *expands* to reflect increasing uncertainty regarding the release origin.

---

## 2. Satellite Remote Sensing & Look-Alike Assumptions

### ASSUMP-03: SAR Dampening Signature
- **Statement:** Mineral oil dampens capillary and short gravity ocean waves ($1\text{--}10\text{ cm}$), reducing radar backscatter $\sigma^0$ by $3\text{--}15\text{ dB}$ relative to ambient sea clutter, appearing as a dark patch in C-band SAR imagery.
- **Supporting Evidence:** Established electromagnetic wave scattering theory (Alpers & Huhnerfuss, 1988; Solberg et al., 2007).
- **What Could Invalidate It:** Look-alikes produced by:
  - Low wind speed regions ($u_{10} < 3\text{ m/s}$): ambient water is smooth everywhere, producing false dark spots.
  - Natural biogenic surfactant films (fish oil, algal blooms).
  - Rain cells and downdrafts.
  - Internal solitary waves and ship wakes.
- **Mitigation:** Meteorological gating with ERA5 wind reanalysis. If $u_{10} < 3\text{ m/s}$, flag detection as `LOOKALIKE_RISK_HIGH` and discount detection confidence.

---

## 3. AIS Data & Vessel Kinematics Assumptions

### ASSUMP-04: Transponder Transmission & Kinematic Integrity
- **Statement:** Merchant vessels $\ge 300\text{ GT}$ on international voyages are mandated by IMO SOLAS Chapter V to broadcast Class A AIS messages at 2–10 second intervals while underway.
- **Supporting Evidence:** IMO International Convention for the Safety of Life at Sea (SOLAS).
- **What Could Invalidate It:**
  - Terrestrial AIS receiver shadow zones beyond line-of-sight ($> 25\text{--}40\text{ nm}$ from shore).
  - Satellite AIS message collisions in high-density choke points (e.g., Malacca Strait, English Channel).
  - Deliberate transponder disabling (AIS dark activity) during illicit discharge operations.
- **Mitigation:** Never treat an AIS gap as conclusive proof of illegal conduct. Treat gaps as data-quality indicators. When vessel traffic density is high and origin probability is strong, formulate the untracked candidate hypothesis $H_{dark}$.

---

## 4. Probabilistic Attribution & Decision Assumptions

### ASSUMP-05: Principle of Honest Abstention
- **Statement:** When available evidence cannot discriminate between competing hypotheses within statistical bounds, the correct scientific behavior is to abstain (`INSUFFICIENT_EVIDENCE`) rather than to report a forced winner.
- **Supporting Evidence:** Standard practice in forensic statistics (likelihood ratio frameworks, Scottish verdict "not proven", ISO 17025).
- **What Could Invalidate It:** Operational pressure from users demanding a single culprit name.
- **Mitigation:** Clearly display the top competing hypotheses alongside the abstention decision, and present the Active Sensing recommendation indicating what specific evidence would resolve the ambiguity.

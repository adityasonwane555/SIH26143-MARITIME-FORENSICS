# Scientific Methods & Physical Principles — SIH26143

This document formalizes the mathematics, physical equations, oceanographic transport approximations, and statistical decision theory underpinning the Maritime Forensic Intelligence Engine.

---

## 1. Lagrangian Drift & Hydrodynamic Advection

### 1.1 Total Surface Drift Velocity
The net velocity vector $\vec{U}_{\text{drift}}(x, y, t)$ acting on a surface oil slick particle is governed by the superposition of ocean surface currents and wind-induced leeway transport:

$$\vec{U}_{\text{drift}} = \vec{u}_{\text{current}} + \alpha_{\text{wind}} \cdot \mathbf{R}(\theta_{\text{Coriolis}}) \cdot \vec{u}_{\text{wind10}} + \vec{u}_{\text{diff}}$$

Where:
- $\vec{u}_{\text{current}} = (u_c, v_c)$ is the eastward and northward surface ocean current velocity (m/s) obtained from CMEMS or regional models.
- $\vec{u}_{\text{wind10}} = (u_w, v_w)$ is the 10-meter atmospheric wind velocity (m/s) obtained from ERA5 reanalysis or ECMWF NWP.
- $\alpha_{\text{wind}} = 0.032$ ($3.2\%$) is the empirical wind leeway drag factor for medium-to-heavy crude oils (ASCE Task Committee on Modeling of Oil Spills).
- $\mathbf{R}(\theta_{\text{Coriolis}})$ is the 2D rotation matrix representing the Coriolis deflection angle ($\approx 20^\circ$ clockwise in the Northern Hemisphere, counterclockwise in the Southern Hemisphere).
- $\vec{u}_{\text{diff}}$ is the stochastic turbulent diffusion component.

### 1.2 Runge-Kutta 4th-Order Integration Scheme
Spatial trajectory integration over discrete time step $\Delta t = 300\text{ s}$ ($5\text{ minutes}$) utilizes standard 4th-order Runge-Kutta:

$$\vec{x}(t + \Delta t) = \vec{x}(t) + \frac{\Delta t}{6} \left( \vec{k}_1 + 2\vec{k}_2 + 2\vec{k}_3 + \vec{k}_4 \right)$$

$$\begin{aligned}
\vec{k}_1 &= \vec{U}_{\text{drift}}(\vec{x}(t), t) \\
\vec{k}_2 &= \vec{U}_{\text{drift}}\left(\vec{x}(t) + \frac{\Delta t}{2}\vec{k}_1, t + \frac{\Delta t}{2}\right) \\
\vec{k}_3 &= \vec{U}_{\text{drift}}\left(\vec{x}(t) + \frac{\Delta t}{2}\vec{k}_2, t + \frac{\Delta t}{2}\right) \\
\vec{k}_4 &= \vec{U}_{\text{drift}}(\vec{x}(t) + \Delta t\vec{k}_3, t + \Delta t)
\end{aligned}$$

For **backward drift reconstruction (hindcast)**, time is integrated with negative step $-\Delta t$.

### 1.3 Horizontal Turbulent Diffusion (Random Walk)
To prevent unphysical singular convergence during backward advection, random turbulent diffusion is superimposed:

$$\Delta \vec{x}_{\text{turb}} = \zeta \cdot \sqrt{2 K_h \Delta t}$$

Where:
- $\zeta \sim \mathcal{N}(0, 1)$ is a standard Gaussian random vector.
- $K_h = 5.0\text{ m}^2/\text{s}$ is the horizontal eddy diffusivity constant.

---

## 2. Origin Probability Surface Estimation

### 2.1 2D Gaussian Kernel Density Estimation (KDE)
Given an ensemble of $N$ backward-advected particles $\{(\phi_i, \lambda_i)\}_{i=1}^N$ at the inferred release time window $t_{\text{release}}$, the continuous probability density function $P(\phi, \lambda)$ is evaluated via Gaussian KDE:

$$P(\phi, \lambda) = \frac{1}{2\pi N b_\phi b_\lambda} \sum_{i=1}^N \exp \left( -\frac{1}{2} \left[ \left(\frac{\phi - \phi_i}{b_\phi}\right)^2 + \left(\frac{\lambda - \lambda_i}{b_\lambda}\right)^2 \right] \right)$$

Where bandwidths $b_\phi, b_\lambda$ are determined by Scott's Rule:

$$b = N^{-\frac{1}{d+4}} \cdot \sigma = N^{-\frac{1}{6}} \cdot \sigma$$

Iso-probability contours at $50\%$, $80\%$, and $95\%$ are extracted via marching squares over the normalized grid matrix.

---

## 3. Bayesian Multi-Hypothesis Attribution

### 3.1 Prior Normalization
For a candidate set of $M$ vessel hypotheses $H_1, \dots, H_m$ plus background non-vessel/dark vessel hypotheses $H_{\text{infra}}, H_{\text{seep}}, H_{\text{dark}}$:

$$\sum_{k=1}^K P(H_k) = 1.0$$

Prior probabilities $P(H_k)$ incorporate baseline spatial-temporal corridor intersection and vessel gross tonnage/fuel capacity priors.

### 3.2 Evidence Likelihood Updating
Each piece of observed evidence $E_j \in \mathcal{E}$ (e.g. trajectory alignment, course consistency, speed appropriateness) contributes a likelihood factor $L(E_j | H_k) \in (0, \infty)$:

$$P(H_k | \mathcal{E}) = \frac{P(H_k) \prod_{j=1}^J L(E_j | H_k)^{\omega_j}}{\sum_{l=1}^K P(H_l) \prod_{j=1}^J L(E_j | H_l)^{\omega_j}}$$

Where $\omega_j \in [0, 1]$ represents the data quality confidence weight of the observing sensor.

---

## 4. Adversarial Falsification & Physical Stress Tests

A leading hypothesis $H^*$ must pass five simultaneous falsification gates to avoid disqualification:
1. **Spatial Bounding Gate:** The candidate's historical track must intersect the $95\%$ origin confidence envelope during the inferred release window:
   $$\min_{t \in [t_0, t_1]} d(\vec{x}_{\text{vessel}}(t), \vec{x}_{\text{origin\_peak}}) \le R_{95\%}$$
2. **Temporal Synchronicity Gate:** Difference between candidate passage time and hindcast release time must satisfy:
   $$|\Delta t| = |t_{\text{passage}} - t_{\text{release}}| \le 2.0\text{ hours}$$
3. **Hydrodynamic Course Alignment:** In navigation coordinates, angle $\theta_{\text{rel}}$ between candidate heading $\psi$ and slick major orientation $\theta_{\text{slick}}$:
   $$\Delta \theta = \min(|\psi - \theta_{\text{slick}}|, 180^\circ - |\psi - \theta_{\text{slick}}|) \le 45^\circ$$
4. **Counterfactual Plume Consistency:** Forward simulation from candidate GPS must yield Modified Hausdorff distance $<3.0\text{ km}$ and bounding box $\text{IoU} \ge 0.15$.
5. **AIS Integrity Verification:** Track data gap must not exceed $4.0\text{ hours}$ without spatial continuity reconciliation.

---

## 5. Information-Theoretic Uncertainty & Active Sensing

### 5.1 Shannon Entropy
Attribution uncertainty across posterior distribution $\mathbf{p} = (p_1, \dots, p_K)$ is quantified by Shannon entropy $H(\mathbf{p})$ in bits:

$$H(\mathbf{p}) = -\sum_{k=1}^K p_k \log_2(p_k)$$

The maximum possible entropy for $K$ discrete hypotheses is $H_{\max} = \log_2(K)$.

### 5.2 Expected Information Gain (Active Sensing)
For a prospective sensing action $A_m$ (e.g., optical satellite revisit, SAR tasking, or patrol flight), the Expected Information Gain $\mathbb{E}[\Delta H(A_m)]$ is:

$$\mathbb{E}[\Delta H(A_m)] = H(\mathbf{p}) - \sum_{y \in \mathcal{Y}} P(y | A_m) H(\mathbf{p}_{| y})$$

The system recommends actions ranked by descending $\mathbb{E}[\Delta H(A_m)]$, directing operational assets to maximize ambiguity reduction.

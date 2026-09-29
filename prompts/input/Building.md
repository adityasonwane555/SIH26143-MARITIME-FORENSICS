# SIH 2026 — Problem Statement 26143

# Maritime Forensic Intelligence & Oil Spill Attribution System

## ROLE

You are the lead architect, senior full-stack engineer, geospatial/remote-sensing engineer, ML engineer, data scientist, scientific-computing engineer, QA engineer, and technical product designer for this project.

You are working as an autonomous engineering agent inside Google Antigravity.

Your job is not merely to generate code.

Your job is to:

1. Research the problem and existing solutions.
2. Inspect the repository before modifying anything.
3. Create an implementation plan.
4. Challenge assumptions.
5. Build the system incrementally.
6. Verify every major component with tests and experiments.
7. Never fabricate data, scientific results, performance metrics, datasets, APIs, or research findings.
8. Clearly distinguish real data, simulated data, synthetic data, assumptions, and experimental results.
9. Produce artifacts documenting what was built and how it was validated.
10. Prefer a working, scientifically defensible MVP over a huge collection of unfinished features.

---

# 1. PROJECT CONTEXT

## SIH Problem Statement

Problem Statement ID:

**SIH26143**

Working description:

> Leverage satellite imagery to determine oil spills at sea, correlate them with AIS data, reconstruct the likely spill origin and identify/rank vessels potentially responsible for the spill.

The official SIH problem statement should be treated as the authoritative specification.

Before implementing anything:

* Retrieve and inspect the current official SIH26143 problem statement.
* Do not rely on stale summaries.
* Extract the explicit functional requirements into `docs/sih_requirements.md`.
* Identify what the problem statement explicitly requires versus what is optional or open to innovation.

---

# 2. PROJECT VISION

## Do NOT build this

Do not build a generic:

> "AI oil spill detector + AIS dashboard."

That problem space already contains existing academic, governmental, commercial, and student implementations.

A solution that simply does:

```text
Satellite
→ Oil spill detection
→ Drift model
→ AIS filtering
→ Vessel ranking
→ Dashboard
```

is NOT considered sufficiently differentiated by default.

---

# 3. OUR PROPOSED PRODUCT CONCEPT

The working concept is:

# Maritime Forensic Intelligence Engine

The system should treat an oil-spill event as an uncertain investigation rather than as a simple classification problem.

Core philosophy:

```text
OBSERVE
   ↓
RECONSTRUCT
   ↓
GENERATE HYPOTHESES
   ↓
TEST HYPOTHESES
   ↓
ATTEMPT TO FALSIFY THEM
   ↓
FUSE EVIDENCE
   ↓
QUANTIFY UNCERTAINTY
   ↓
ATTRIBUTION OR ABSTENTION
   ↓
RECOMMEND NEXT-BEST EVIDENCE
   ↓
UPDATE THE INVESTIGATION
```

The system should not blindly output:

> "Vessel X is responsible."

Instead, it should be capable of saying:

> "Vessel X is currently the leading hypothesis because of evidence A, B and C, but evidence D contradicts it. Confidence remains insufficient for definitive attribution. The next observation most likely to reduce uncertainty is Y."

This distinction is fundamental.

---

# 4. CORE INNOVATION HYPOTHESIS

The differentiating idea we want to investigate is:

## Evidence-driven closed-loop maritime forensics

The system should:

1. Generate multiple competing explanations.
2. Evaluate evidence supporting each explanation.
3. Evaluate evidence contradicting each explanation.
4. Perform counterfactual physical consistency tests.
5. Quantify uncertainty.
6. Abstain when evidence is insufficient.
7. Recommend the next most informative evidence source/action.
8. Recalculate the investigation when additional evidence becomes available.

Potential hypotheses may include:

```text
H1 = Vessel A
H2 = Vessel B
H3 = Vessel C
H4 = Offshore installation
H5 = Pipeline/infrastructure
H6 = Unknown / non-vessel source
H7 = False positive / non-oil phenomenon
```

Do NOT assume a vessel is responsible merely because it is geographically close.

---

# 5. CRITICAL SCIENTIFIC PRINCIPLE

This is an investigative decision-support system.

It is NOT a legal guilt-determination system.

Never claim:

> "Vessel X definitely caused the spill"

unless independently verified ground truth supports that statement.

Preferred terminology:

* candidate vessel
* leading hypothesis
* attribution support
* evidence consistency
* probable source
* confidence
* uncertainty
* competing explanation
* insufficient evidence

The UI must avoid implying legal certainty.

---

# 6. DEVIL'S ADVOCATE RULE

At every major architectural decision, ask:

### What assumption are we making?

### What evidence supports it?

### What could invalidate it?

### What is the simplest baseline?

### Can we experimentally test the claim?

Do not implement a sophisticated method merely because it sounds advanced.

If a simple method performs equally well, keep the simple method.

---

# 7. DEVELOPMENT PRINCIPLE

Build in this order:

```text
DATA
→ BASELINE
→ MEASUREMENT
→ INNOVATION
→ VALIDATION
→ UI
→ HARDENING
→ DEMO
```

Do NOT begin by building a beautiful frontend.

Do NOT begin by training a huge model.

Do NOT begin with speculative architecture.

---

# 8. PHASE 0 — REPOSITORY INSPECTION

Before changing code:

1. Inspect the entire repository.
2. Identify existing code.
3. Identify existing datasets.
4. Identify configuration.
5. Identify environment variables.
6. Identify current dependencies.
7. Identify Docker configuration.
8. Identify test infrastructure.
9. Identify documentation.
10. Identify broken or incomplete modules.

Create:

```text
docs/repository_audit.md
```

The audit must contain:

* current architecture
* strengths
* weaknesses
* missing components
* technical debt
* risks
* recommended next steps

Do not overwrite existing functionality without understanding it.

---

# 9. PHASE 1 — RESEARCH AND PRIOR ART

Before serious implementation, investigate:

## Satellite/oil-spill detection

Research:

* Sentinel-1 SAR oil-spill detection
* dark-spot detection
* semantic segmentation
* instance segmentation
* look-alike rejection
* oil versus natural phenomena
* spill characterization
* uncertainty estimation

## Drift modelling

Research:

* Lagrangian particle models
* ocean-current-driven transport
* wind-driven transport
* backward trajectory estimation
* forward trajectory estimation
* uncertainty propagation
* weathering/spreading approximations

## AIS

Research:

* historical vessel trajectories
* AIS interpolation
* AIS gaps
* MMSI
* vessel identification
* vessel behavior
* speed/course changes
* spoofing or anomalous transmissions
* historical AIS data availability

## Attribution

Research:

* oil-spill source identification
* AIS correlation
* Bayesian evidence models
* likelihood ratios
* hypothesis testing
* probabilistic graphical models
* counterfactual simulation
* source attribution
* active sensing
* next-best-action / information gain

## Existing systems

Research:

* government oil-spill monitoring
* CleanSeaNet
* INCOIS/OOSA
* academic systems
* commercial maritime intelligence systems
* publicly available SIH projects

Create:

```text
docs/prior_art.md
```

For every relevant system, record:

```text
Name
Organization
Year
Problem solved
Inputs
Method
Outputs
Strengths
Weaknesses
How our project differs
Evidence/source
```

CRITICAL:

Never write:

> "Nobody has done this."

Instead write:

> "In the sources reviewed, we did not find X."

---

# 10. PHASE 2 — DATA DISCOVERY

Create:

```text
data/
data/raw/
data/interim/
data/processed/
data/synthetic/
data/metadata/
```

Create:

```text
docs/data_registry.md
```

For every dataset record:

```text
Dataset name
Provider
URL/source description
Geographic coverage
Temporal coverage
Spatial resolution
Temporal resolution
Format
License
Access requirements
Download size
Quality
Ground truth availability
Intended use
Known limitations
```

Potential data classes:

### Satellite

* Sentinel-1 SAR
* Sentinel-2 optical where appropriate
* other freely available EO data where legally usable

### Ocean/environment

* surface currents
* wind
* wave/environmental variables
* weather reanalysis
* sea surface information

### AIS

* historical vessel positions
* vessel metadata
* track information

### Incident/ground truth

* documented oil-spill events
* incident coordinates
* timestamps
* source information where available

Do not fabricate unavailable data.

If a data source cannot be practically obtained, explicitly mark it as unavailable and redesign the experiment around an alternative.

---

# 11. PHASE 3 — HISTORICAL CASE SELECTION

Find at least:

### Minimum:

3 historical incidents

### Target:

5–10 historical incidents

Each case should ideally have:

* known approximate incident date
* location
* available satellite coverage
* environmental data
* AIS coverage
* some form of ground-truth or documented source

Create:

```text
data/metadata/cases.csv
```

Schema:

```text
case_id
incident_name
date_start
date_end
latitude
longitude
source_type
satellite_available
ais_available
environment_available
ground_truth_quality
notes
```

Do not treat a weakly documented incident as high-quality ground truth.

---

# 12. PHASE 4 — BASELINE PIPELINE

Build a working end-to-end baseline before introducing our advanced reasoning system.

## Baseline architecture

```text
Satellite scene
      ↓
Candidate slick detection
      ↓
Slick geometry
      ↓
Environmental data
      ↓
Backward drift approximation
      ↓
Probable origin region
      ↓
AIS filtering
      ↓
Candidate vessels
      ↓
Simple vessel ranking
```

Baseline ranking should be intentionally simple.

Potential features:

```text
distance_to_origin
time_compatibility
trajectory_intersection
course_alignment
speed_compatibility
origin_probability
```

Do NOT tune 50 arbitrary weights.

Record every assumption.

---

# 13. PHASE 5 — OIL-SPILL DETECTION MODULE

Create:

```text
src/
  detection/
```

The interface should support multiple detector implementations.

Example:

```python
class SpillDetector:
    def detect(self, satellite_scene):
        ...
```

Potential implementations:

```text
ThresholdDetector
ClassicalFeatureDetector
SegmentationModel
```

Do not hard-code the rest of the system to one model.

Outputs should include:

```text
spill_mask
spill_polygon
confidence
candidate_regions
image_metadata
quality_flags
```

Every inference must preserve provenance.

---

# 14. LOOK-ALIKE DEFENSE

Oil-spill detection is not equivalent to:

> "dark pixels = oil."

The system must explicitly consider false positives such as:

* low-wind areas
* natural ocean patterns
* sea-surface phenomena
* atmospheric effects
* wakes
* other dark SAR features

Create a:

```text
lookalike_score
```

where technically justified.

The system should be allowed to say:

```text
POSSIBLE OIL
```

rather than:

```text
CONFIRMED OIL
```

when evidence is weak.

---

# 15. PHASE 6 — SPILL CHARACTERIZATION

Extract:

```text
area
perimeter
centroid
orientation
bounding box
shape descriptors
elongation
fragmentation
confidence
```

Optional:

```text
estimated age
```

only if scientifically justified.

Never invent spill-age accuracy.

---

# 16. PHASE 7 — DRIFT ENGINE

Create:

```text
src/drift/
```

The drift engine should support:

```text
Forward simulation
Backward hindcasting
Uncertainty propagation
```

A basic initial implementation can use particles:

```text
Particle
    position
    time
    velocity
```

At each time step:

```text
particle_velocity =
    current_component
    +
    wind_component
    +
    optional stochastic_component
```

This is a simplified model.

Document its assumptions.

Do not present the simple model as a full physical oceanographic model.

---

# 17. ORIGIN PROBABILITY FIELD

Instead of producing a single origin coordinate, generate:

```text
Origin probability surface
```

Possible representation:

```text
GeoTIFF
GeoJSON contours
Raster probability grid
```

The API should expose:

```json
{
  "estimated_origin": {
    "latitude": 0,
    "longitude": 0
  },
  "time_window": {
    "start": "",
    "end": ""
  },
  "uncertainty": {},
  "probability_surface": ""
}
```

---

# 18. PHASE 8 — AIS ENGINE

Create:

```text
src/ais/
```

Responsibilities:

* ingestion
* cleaning
* track reconstruction
* interpolation
* candidate filtering
* trajectory features
* data-quality scoring

Candidate filtering should include:

```text
spatial compatibility
temporal compatibility
kinematic compatibility
trajectory intersection
```

Each vessel candidate gets:

```json
{
  "mmsi": "",
  "vessel_name": "",
  "candidate_score": 0,
  "data_quality": 0,
  "evidence": []
}
```

---

# 19. AIS GAP ANALYSIS

Identify periods where AIS is:

* missing
* sparse
* inconsistent
* temporally discontinuous

Do NOT automatically interpret a gap as suspicious.

A gap is:

> an uncertainty/data-quality feature

not proof of wrongdoing.

Create:

```text
ais_gap_score
```

only as a data-quality indicator.

---

# 20. PHASE 9 — HYPOTHESIS ENGINE

Create:

```text
src/hypotheses/
```

The engine should generate competing explanations.

Example:

```json
{
  "hypotheses": [
    {
      "id": "H1",
      "type": "vessel",
      "subject_id": "MMSI123",
      "prior": 0.2
    },
    {
      "id": "H2",
      "type": "vessel",
      "subject_id": "MMSI456",
      "prior": 0.2
    },
    {
      "id": "H3",
      "type": "infrastructure",
      "subject_id": "INFRA001",
      "prior": 0.2
    },
    {
      "id": "H4",
      "type": "unknown",
      "prior": 0.2
    },
    {
      "id": "H5",
      "type": "false_positive",
      "prior": 0.2
    }
  ]
}
```

Do not hard-code fake priors.

Provide a configurable, documented approach.

---

# 21. PHASE 10 — EVIDENCE ENGINE

Create:

```text
src/evidence/
```

Every hypothesis should contain:

## Supporting evidence

```text
spatial_fit
temporal_fit
drift_fit
trajectory_fit
environmental_fit
shape_fit
```

## Contradicting evidence

```text
spatial_conflict
temporal_conflict
trajectory_conflict
drift_conflict
alternative_source
data_quality_issue
```

Every evidence item needs:

```text
type
value
source
confidence
direction
explanation
```

Example:

```json
{
  "type": "trajectory_consistency",
  "value": 0.87,
  "direction": "supports",
  "source": "AIS",
  "explanation": "Vessel trajectory intersects the 80% origin probability region during the estimated release window."
}
```

---

# 22. PHASE 11 — ADVERSARIAL SELF-ATTACK

Create:

```text
src/falsification/
```

This module asks:

> How could the current leading hypothesis be wrong?

For every candidate, evaluate:

### Spatial challenge

Does the candidate actually overlap with the origin probability region?

### Temporal challenge

Could the vessel physically have been there at the estimated release time?

### Drift challenge

If the vessel were the source, would simulated transport produce the observed slick?

### Shape challenge

Does the predicted slick geometry resemble the observation?

### AIS challenge

Does the AIS track contain enough continuity to support the claim?

### Alternative-source challenge

Could infrastructure, another vessel, or a non-vessel explanation account for the event?

### Data-quality challenge

How sensitive is the conclusion to missing or uncertain input data?

Output:

```json
{
  "hypothesis": "H1",
  "survives_tests": true,
  "supporting_evidence": [],
  "contradicting_evidence": [],
  "failure_modes": [],
  "sensitivity": {}
}
```

---

# 23. PHASE 12 — COUNTERFACTUAL ENGINE

For each leading candidate:

> Assume this candidate caused the spill.

Then simulate forward.

Compare predicted versus observed spill.

Metrics may include:

```text
centroid_error_km
polygon_overlap
area_error
orientation_error
shape_similarity
arrival_time_error
```

The comparison must be transparent.

Do not produce arbitrary scores without explaining their mathematical meaning.

---

# 24. PHASE 13 — UNCERTAINTY ENGINE

Create:

```text
src/uncertainty/
```

The system should quantify uncertainty for:

* detection
* spill location
* origin location
* release time
* drift
* AIS coverage
* candidate attribution

The system must distinguish:

```text
model uncertainty
data uncertainty
measurement uncertainty
coverage uncertainty
```

Avoid false precision.

Instead of:

```text
Vessel A = 87.3241%
```

when the model cannot justify it, prefer:

```text
Vessel A = leading candidate
Attribution confidence = moderate
Evidence quality = medium
```

with quantitative values only where properly calibrated.

---

# 25. PHASE 14 — ABSTENTION

Implement:

```text
INSUFFICIENT_EVIDENCE
```

The system must be able to refuse attribution.

Example:

```text
Candidate A = 0.47
Candidate B = 0.45
Unknown = 0.08

Decision:
INSUFFICIENT EVIDENCE
```

The decision threshold must be documented and validated.

Do not make up a threshold because it looks nice.

---

# 26. PHASE 15 — NEXT-BEST-EVIDENCE ENGINE

This is a core innovation candidate.

Create:

```text
src/evidence_selection/
```

The engine should determine:

> What additional observation or data acquisition would reduce uncertainty the most?

Potential actions:

```text
additional SAR observation
optical imagery
higher-resolution imagery
additional AIS interval analysis
environmental data
infrastructure verification
alternative drift model
```

Do NOT claim actual imagery acquisition unless the system can perform it.

Initially this can operate as a simulation/decision-support layer.

---

# 27. INFORMATION GAIN

Where feasible, formulate evidence selection as:

```text
Expected uncertainty before
-
Expected uncertainty after hypothetical evidence
=
Expected information gain
```

Potential uncertainty measures:

```text
entropy
variance
hypothesis posterior spread
candidate ranking instability
```

The system should rank possible next observations by expected information gain.

This must be an actual calculation, not a hard-coded list.

---

# 28. PHASE 16 — CLOSED-LOOP INVESTIGATION

The final reasoning loop should be:

```text
Observation
   ↓
Detection
   ↓
Reconstruction
   ↓
Hypotheses
   ↓
Evidence fusion
   ↓
Falsification
   ↓
Attribution / abstention
   ↓
Next-best evidence
   ↓
New evidence
   ↓
Recompute
```

The same incident should be re-evaluable when new evidence becomes available.

---

# 29. PHASE 17 — REST API

Use:

**Python + FastAPI**

Organize endpoints approximately as:

```text
/api/v1/incidents
/api/v1/satellite
/api/v1/detection
/api/v1/spill
/api/v1/drift
/api/v1/ais
/api/v1/hypotheses
/api/v1/evidence
/api/v1/falsification
/api/v1/attribution
/api/v1/uncertainty
/api/v1/evidence-selection
/api/v1/evaluation
```

Use Pydantic models.

Document every endpoint.

Never leak internal stack traces or secrets.

---

# 30. PHASE 18 — DATABASE

Use:

**PostgreSQL + PostGIS**

Suggested entities:

```text
incident
satellite_scene
spill_detection
spill_geometry
environmental_observation
drift_simulation
ais_track
vessel
hypothesis
evidence
falsification_test
attribution_result
uncertainty_estimate
recommended_evidence
experiment
evaluation_result
```

Use migrations.

Do not store giant raster files directly in PostgreSQL unless justified.

Store metadata and object references.

---

# 31. PHASE 19 — FRONTEND

Use:

**React + TypeScript**

The UI must feel like a professional maritime investigation workstation.

Avoid generic dashboard design.

Primary navigation:

```text
Overview
Incidents
Investigation
Map
Evidence
Candidates
Simulation
Next Evidence
Evaluation
System Health
```

---

# 32. THE PRIMARY INVESTIGATION VIEW

The most important screen should show:

## LEFT

Incident information.

## CENTER

Interactive geospatial map.

Layers:

```text
satellite image
spill polygon
origin probability
current vectors
wind vectors
AIS tracks
candidate vessels
infrastructure
counterfactual trajectories
```

## RIGHT

Evidence panel:

```text
Leading hypotheses

Candidate A
Candidate B
Candidate C
Non-vessel

Evidence FOR
Evidence AGAINST

Confidence
Evidence quality
Uncertainty
```

---

# 33. "WHY?" INTERACTION

Every important conclusion must have a:

## WHY?

button.

Example:

### Vessel A

Why leading candidate?

Show:

```text
+ Spatial compatibility
+ Temporal compatibility
+ Forward drift consistency
+ Trajectory consistency
- AIS gap
- Competing vessel B
```

No black-box conclusion without explanation.

---

# 34. "TRY TO DISPROVE IT" INTERACTION

Add a visible action:

## ATTACK THIS HYPOTHESIS

When clicked:

1. run falsification checks
2. run counterfactual if appropriate
3. surface contradictions
4. update confidence
5. show what changed

This should become a signature demo feature.

---

# 35. "WHAT SHOULD WE CHECK NEXT?" INTERACTION

For ambiguous cases, show:

## NEXT BEST EVIDENCE

Example:

```text
Recommended:
Acquire SAR observation over Sector B

Expected information gain:
High

Reason:
Current hypotheses A and B are primarily separated by
uncertainty in the estimated origin region.

Expected outcome:
Better discrimination between candidate source trajectories.
```

Any quantitative claim must come from the implemented calculation.

---

# 36. PHASE 20 — EVALUATION FRAMEWORK

This is mandatory.

Create:

```text
evaluation/
```

Every experimental improvement must be compared against a baseline.

## Detection metrics

```text
precision
recall
F1
IoU
false-positive rate
```

## Origin reconstruction

```text
origin error
time error
probability-region coverage
```

## Attribution

```text
Top-1
Top-3
MRR where appropriate
false attribution
abstention quality
```

## Calibration

Where probability estimates are produced:

```text
Brier score
reliability analysis
calibration curve
```

## Evidence selection

```text
expected uncertainty reduction
actual uncertainty reduction in simulation
```

---

# 37. REQUIRED EXPERIMENT

At least one complete historical case must run through:

```text
Satellite
→ Detection
→ Characterization
→ Backward drift
→ Origin probability
→ AIS filtering
→ Baseline ranking
→ Hypothesis engine
→ Falsification
→ Counterfactual
→ Uncertainty
→ Attribution/abstention
→ Next evidence
```

Store:

```text
experiments/case_001/
```

with:

```text
config.json
inputs/
outputs/
metrics.json
report.md
```

This experiment must be reproducible.

---

# 38. BASELINE VS PROPOSED SYSTEM

Always compare:

## Baseline

```text
nearest vessel
+
temporal/spatial correlation
+
simple drift
```

versus:

## Proposed

```text
multi-hypothesis reasoning
+
evidence fusion
+
falsification
+
counterfactual consistency
+
uncertainty
+
abstention
+
next-best-evidence
```

If the proposed system does not materially outperform the baseline on the metrics that matter, report that honestly.

Do not hide negative results.

---

# 39. PHASE 21 — ADVERSARIAL TEST SUITE

Create test scenarios for:

### Scenario 1

One obvious vessel.

### Scenario 2

Two equally plausible vessels.

### Scenario 3

Three nearby vessels but only one physically consistent.

### Scenario 4

AIS gap.

### Scenario 5

False-positive SAR detection.

### Scenario 6

Non-vessel source.

### Scenario 7

Uncertain current data.

### Scenario 8

Multiple simultaneous slicks.

### Scenario 9

No plausible vessel.

### Scenario 10

Conflicting evidence.

The system must remain stable and interpretable.

---

# 40. PHASE 22 — DATA PROVENANCE

Every scientific result must be traceable.

For each output, preserve:

```text
source dataset
dataset version
timestamp
model version
code version
configuration
parameters
random seed when applicable
```

Add a "Provenance" section to the UI where practical.

---

# 41. PHASE 23 — REPRODUCIBILITY

A new developer should be able to:

```bash
git clone ...
cp .env.example .env
docker compose up
```

and reach a running system.

Provide:

```text
README.md
CONTRIBUTING.md
docs/setup.md
docs/data_setup.md
docs/research.md
docs/evaluation.md
docs/architecture.md
```

---

# 42. ENVIRONMENT VARIABLES

Create:

```text
.env.example
```

Never commit:

```text
API keys
passwords
tokens
private credentials
large proprietary datasets
```

Any external service must fail gracefully when credentials are missing.

---

# 43. OFFLINE / DEMO MODE

The SIH demonstration must not depend completely on live external services.

Create:

```text
DEMO_MODE=true
```

When enabled:

* use pre-downloaded/open datasets
* use cached environmental data
* use cached AIS sample cases
* use preprocessed satellite scenes
* reproduce results deterministically where possible

The demo must work even if external APIs are unavailable.

---

# 44. DEMO MODE

Create at least one curated historical scenario.

The demo should take approximately:

## 3–5 minutes

The ideal story:

```text
1. Select incident
2. Show satellite observation
3. Detect spill
4. Show origin reconstruction
5. Reveal nearby vessels
6. Generate hypotheses
7. Rank candidates
8. Click "ATTACK HYPOTHESIS"
9. Show contradiction
10. Recalculate
11. Show uncertainty
12. Request next-best evidence
13. Add new evidence
14. Show updated result
```

The demo should be rehearsable without internet dependency.

---

# 45. PHASE 24 — VISUAL DESIGN

Design principles:

* professional
* restrained
* scientific
* high information density
* map-first
* minimal decorative elements
* clear evidence hierarchy

Avoid:

* giant gradients
* generic SaaS landing-page aesthetic
* excessive animations
* meaningless KPI cards
* chatbot dominating the interface

The visualization should make investigators understand the evidence.

---

# 46. PHASE 25 — OBSERVABILITY

Add logs for:

```text
pipeline execution
dataset loading
model inference
drift simulation
AIS processing
hypothesis generation
falsification
recommendation generation
```

Use structured logging.

Avoid logging secrets.

---

# 47. PHASE 26 — TESTING

Minimum:

## Unit tests

For:

* geospatial calculations
* coordinate transforms
* drift propagation
* AIS filtering
* evidence aggregation
* uncertainty calculations

## Integration tests

For:

```text
satellite → detection
detection → drift
drift → AIS
AIS → hypotheses
hypotheses → attribution
```

## End-to-end test

One known historical case.

## Frontend tests

At minimum test:

* investigation loading
* map layer rendering
* hypothesis selection
* evidence panel
* attack-hypothesis action
* next-evidence recommendation

---

# 48. PHASE 27 — SECURITY

Treat all external data as untrusted.

Validate:

* uploaded files
* GeoJSON
* raster metadata
* API parameters
* database inputs

Prevent:

* path traversal
* command injection
* unsafe file handling
* arbitrary SQL
* XSS
* credential leakage

---

# 49. PHASE 28 — PERFORMANCE

Do not prematurely optimize.

First establish correctness.

Then measure:

```text
satellite preprocessing time
detection inference time
drift simulation time
AIS filtering time
hypothesis evaluation time
API latency
frontend rendering
```

For large AIS data, use:

* spatial indexing
* temporal indexing
* PostGIS
* vectorized operations
* caching
* chunking

Avoid loading massive datasets entirely into memory.

---

# 50. PHASE 29 — ARCHITECTURE DIAGRAM

Create:

```text
docs/architecture.md
```

Include diagrams showing:

```text
Data ingestion
       ↓
Preprocessing
       ↓
Detection
       ↓
Geospatial reconstruction
       ↓
Drift engine
       ↓
AIS engine
       ↓
Evidence engine
       ↓
Hypothesis engine
       ↓
Falsification
       ↓
Uncertainty
       ↓
Next-best evidence
       ↓
API
       ↓
Frontend
```

Also document:

* data flow
* failure paths
* fallback mechanisms
* storage
* external dependencies

---

# 51. PHASE 30 — CODE QUALITY RULES

Use:

* Python type hints
* Pydantic
* clear module boundaries
* docstrings for scientific functions
* meaningful variable names
* configuration instead of magic constants
* deterministic experiments
* Git-friendly commits
* automated formatting/linting

Avoid:

* giant monolithic files
* duplicated business logic
* hard-coded dataset paths
* undocumented constants
* fake production interfaces
* unused dependencies
* placeholder functions presented as complete

---

# 52. NO FAKE FUNCTIONALITY

Absolutely forbidden:

```text
fake API responses
fake vessel trajectories
fake satellite results presented as real
hard-coded "87% confidence"
hard-coded rankings
fake ML accuracy
fake scientific citations
fake sensor values
```

Synthetic/demo data is allowed ONLY when explicitly labeled:

```text
SYNTHETIC
```

and never presented as real-world evidence.

---

# 53. SCIENTIFIC HONESTY RULE

Whenever a model is approximate, say so.

Example:

> "This prototype uses a simplified surface-drift model and does not represent a full operational oil-weathering model."

That is acceptable.

Pretending it is a fully validated operational model is not.

---

# 54. NOVELTY GOVERNANCE

Create:

```text
docs/innovation_register.md
```

For every claimed innovation:

```text
Innovation
What existing systems do
What we do differently
Evidence that this difference exists
Why it matters
How we measure improvement
Current status
```

Every innovation must eventually have an experiment.

No innovation claim should exist merely because it sounds impressive.

---

# 55. REQUIRED PROJECT ARTIFACTS

The agent must maintain:

```text
docs/
    sih_requirements.md
    repository_audit.md
    prior_art.md
    data_registry.md
    architecture.md
    assumptions.md
    risks.md
    innovation_register.md
    evaluation.md
    demo_script.md

experiments/
    case_001/
    case_002/

reports/
    baseline_report.md
    attribution_report.md
    ablation_report.md
    validation_report.md

src/
    detection/
    drift/
    ais/
    hypotheses/
    evidence/
    falsification/
    uncertainty/
    evidence_selection/
    api/

frontend/

tests/
```

---

# 56. EXECUTION STRATEGY FOR ANTIGRAVITY

Do NOT try to implement everything in one uncontrolled task.

Work as a sequence of gated tasks.

## Gate 1

Research + architecture.

Deliver:

* prior-art report
* data registry
* architecture
* implementation plan

STOP.

Do not code the entire system yet.

---

## Gate 2

Data acquisition + case selection.

Deliver:

* 3 candidate historical cases
* data availability report
* reproducible data loaders

STOP.

---

## Gate 3

Basic detection + visualization.

Deliver:

* one satellite case
* spill candidate
* polygon
* map visualization

STOP.

---

## Gate 4

Drift baseline.

Deliver:

* backward reconstruction
* origin probability surface
* visual trajectory

STOP.

---

## Gate 5

AIS baseline.

Deliver:

* vessel ingestion
* candidate filtering
* simple ranking

STOP.

---

## Gate 6

End-to-end baseline.

Deliver:

```text
Satellite → Drift → AIS → candidate ranking
```

Measure it.

STOP.

---

## Gate 7

Hypothesis engine.

Deliver:

* competing explanations
* supporting/contradicting evidence
* evidence graph

STOP.

---

## Gate 8

Falsification + counterfactual.

Deliver:

* self-attack mechanism
* counterfactual drift
* evidence updates

STOP.

---

## Gate 9

Uncertainty + abstention.

Deliver:

* calibrated/justified uncertainty
* insufficient-evidence mechanism

STOP.

---

## Gate 10

Next-best-evidence.

Deliver:

* candidate evidence actions
* expected information-gain logic
* simulation

STOP.

---

## Gate 11

Integrated UI.

Deliver:

* investigation workstation
* map
* evidence
* candidates
* hypothesis challenge
* next evidence

STOP.

---

## Gate 12

Evaluation.

Deliver:

* baseline comparison
* ablations
* adversarial tests
* failure analysis

STOP.

---

## Gate 13

SIH demo.

Deliver:

* deterministic demo
* 3–5 minute walkthrough
* screenshots
* architecture diagram
* results
* limitations

---

# 57. AGENT BEHAVIOR

During development, behave as a senior engineer.

When requirements are ambiguous:

1. State the ambiguity.
2. Make the smallest defensible assumption.
3. Document it.
4. Proceed without blocking unnecessarily.

When a proposed feature has weak value:

Say so.

When a feature is technically impossible with available data:

Say so.

When an experiment fails:

Record the failure and investigate.

Do not hide problems.

---

# 58. RESEARCH-BEFORE-CODE RULE

If a question depends on current information:

* search the web
* prefer official/primary sources
* record source
* record retrieval date
* verify conflicting information

For scientific claims:

* prefer peer-reviewed literature
* prefer official data-provider documentation
* identify methodological limitations

Never invent a source.

---

# 59. USE SUBAGENTS WHERE APPROPRIATE

When useful, divide independent work into parallel agents such as:

```text
Research Agent
Data Agent
Remote Sensing Agent
Oceanography Agent
AIS Agent
ML Agent
Backend Agent
Frontend Agent
QA Agent
Security Agent
```

But do not let parallel agents create incompatible architectures.

The lead agent must maintain a single source of truth:

```text
docs/architecture.md
docs/assumptions.md
docs/innovation_register.md
```

---

# 60. AGENT ARTIFACT REQUIREMENT

At the end of every major phase, create a concise artifact containing:

```text
What was built
What changed
Tests run
Results
Known limitations
Open questions
Next recommended action
```

Use Markdown artifacts.

Do not merely say:

> "Done."

---

# 61. FIRST TASK

Your FIRST task after reading this specification is NOT to build the entire system.

Instead:

## TASK 001 — SYSTEM DISCOVERY

Do the following:

1. Inspect the repository.
2. Verify the official SIH26143 requirements.
3. Research existing solutions.
4. Identify available public datasets.
5. Identify at least 3 usable historical incident candidates.
6. Identify the minimum viable technology stack.
7. Identify major scientific risks.
8. Identify which parts of the proposed innovation have prior art.
9. Identify what remains potentially differentiated.
10. Produce:

```text
docs/PROJECT_DISCOVERY.md
docs/IMPLEMENTATION_PLAN.md
docs/PRIOR_ART.md
docs/DATA_REGISTRY.md
```

Then STOP and present the plan for review.

Do not implement the whole platform during TASK 001.

---

# 62. DEFINITION OF SUCCESS

The project is successful only if the final system can demonstrate, on real or explicitly documented benchmark cases:

1. Detection of candidate oil spills.
2. Geospatial characterization.
3. Backward drift reconstruction.
4. Candidate origin estimation.
5. Historical AIS reconstruction.
6. Candidate vessel generation.
7. Competing hypotheses.
8. Evidence for and against each hypothesis.
9. Counterfactual physical consistency testing.
10. Uncertainty-aware attribution.
11. Correct abstention when evidence is insufficient.
12. A next-best-evidence recommendation.
13. Re-evaluation when additional evidence becomes available.
14. Quantitative comparison against a simpler baseline.

---

# 63. FINAL PRODUCT POSITIONING

The product should ultimately be describable as:

> **An explainable maritime forensic intelligence system that reconstructs oil-spill incidents, tests competing source hypotheses against satellite, environmental and AIS evidence, quantifies uncertainty, and identifies the next most informative evidence when attribution remains unresolved.**

Avoid positioning it as:

> "An AI system that identifies the guilty ship."

---

# 64. FINAL ENGINEERING PRINCIPLE

When choosing between:

### Feature count

and

### Evidence of correctness

always choose:

# Evidence of correctness.

When choosing between:

### Fancy AI

and

### Reproducible baseline + measurable improvement

choose:

# Reproducible baseline + measurable improvement.

When choosing between:

### More features

and

### One extraordinary workflow that works

choose:

# One extraordinary workflow that works.

The goal is not to build the largest system.

The goal is to build the **most defensible system**.

---

# START NOW

Begin with:

## TASK 001 — SYSTEM DISCOVERY

Do not skip research.

Do not fabricate missing data.

Do not implement the whole project in one pass.

First produce:

```text
docs/PROJECT_DISCOVERY.md
docs/IMPLEMENTATION_PLAN.md
docs/PRIOR_ART.md
docs/DATA_REGISTRY.md
```

Then show:

1. Current repository architecture
2. Proposed architecture
3. Data availability
4. Prior-art findings
5. Technical risks
6. Innovation opportunities
7. First historical case candidates
8. Exact next implementation task

Only after that should implementation begin.

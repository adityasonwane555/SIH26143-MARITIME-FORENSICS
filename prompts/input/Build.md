# SIH26143 — MASTER BUILD SPECIFICATION

# Maritime Forensic Intelligence & Oil Spill Attribution Platform

---

# 0. EXECUTIVE INSTRUCTION

You are the lead engineering agent responsible for designing, implementing, testing, documenting, validating, and packaging a complete solution for **Smart India Hackathon 2026 Problem Statement SIH26143**.

The objective is NOT to produce a generic oil-spill detection dashboard.

The objective is to build a scientifically defensible, explainable, uncertainty-aware **Maritime Forensic Intelligence System** that can:

1. Detect candidate oil spills from satellite imagery.
2. Characterize the detected spill.
3. Estimate likely spill origin and release-time window.
4. Reconstruct historical vessel movements using AIS.
5. Generate competing source hypotheses.
6. Evaluate evidence supporting and contradicting each hypothesis.
7. Perform counterfactual physical consistency tests.
8. Quantify uncertainty.
9. Abstain when evidence is insufficient.
10. Recommend the next most informative evidence/action.
11. Recalculate conclusions when new evidence is introduced.
12. Present the entire investigation through a professional geospatial interface.
13. Demonstrate measurable improvement over a simple baseline.

The final system must prioritize:

> **Correctness > explainability > evidence > reproducibility > novelty > visual polish.**

---

# 1. NON-NEGOTIABLE RULES

## 1.1 Never fabricate

Never invent:

* datasets
* satellite observations
* AIS records
* scientific results
* model accuracy
* historical incidents
* API availability
* citations
* ground truth
* confidence values
* validation results

Synthetic/demo data is allowed only when clearly marked:

`SYNTHETIC`

Do not present synthetic data as real-world evidence.

---

## 1.2 Never overclaim

This is an investigation-support system, not a legal adjudication system.

Never label a vessel:

> "Guilty"

or:

> "Confirmed polluter"

unless independent ground truth genuinely supports that claim.

Use:

* candidate vessel
* leading hypothesis
* attribution support
* evidence consistency
* confidence
* uncertainty
* insufficient evidence

---

## 1.3 Research before implementation

When a claim depends on current or specialized information:

1. Search primary sources.
2. Prefer official documentation.
3. Prefer peer-reviewed research for scientific claims.
4. Record sources.
5. Record dates.
6. Record uncertainty.

Never claim an idea is globally unique simply because a basic web search did not find it.

---

## 1.4 Baseline before innovation

Always implement a simple baseline first.

We need to be able to answer:

> "Does our advanced approach actually improve the outcome?"

---

## 1.5 Every important claim needs evidence

For example:

BAD:

> Our approach is more accurate.

GOOD:

> On benchmark cases X/Y/Z, the proposed approach improved Top-3 source attribution from A to B under evaluation protocol C.

---

## 1.6 No feature theater

Do not add:

* blockchain
* chatbots
* unnecessary AR/VR
* generic LLM features
* decorative digital twins
* random IoT hardware
* excessive animations
* arbitrary AI models

unless they solve an actual measured problem.

---

# 2. PRODUCT VISION

## Working product name

Use a temporary internal name:

# MARITIME FORENSICS

Do not spend time on branding until the core system works.

Possible final positioning:

> **An explainable maritime forensic intelligence platform that reconstructs oil-spill incidents, evaluates competing source hypotheses against satellite, environmental and AIS evidence, challenges its own conclusions, quantifies uncertainty, and recommends the next most informative evidence when attribution remains unresolved.**

---

# 3. CORE CONCEPT

The system must follow this investigation loop:

```text
OBSERVE
   ↓
DETECT
   ↓
CHARACTERIZE
   ↓
RECONSTRUCT
   ↓
GENERATE HYPOTHESES
   ↓
FUSE EVIDENCE
   ↓
ATTACK HYPOTHESES
   ↓
COUNTERFACTUAL TEST
   ↓
ESTIMATE UNCERTAINTY
   ↓
ATTRIBUTION OR ABSTENTION
   ↓
SELECT NEXT-BEST EVIDENCE
   ↓
INCORPORATE NEW EVIDENCE
   ↓
RECOMPUTE
```

The key product idea is not merely:

> "Which vessel is closest?"

It is:

> "Which explanation best survives evidence and attempts to disprove it, and what evidence should be obtained next if uncertainty remains?"

---

# 4. REQUIRED FUNCTIONAL SYSTEM

The completed product must contain the following major subsystems:

```text
1. Incident Management
2. Satellite Data Management
3. Oil Spill Detection
4. Spill Characterization
5. Ocean/Environmental Data Processing
6. Drift Reconstruction
7. Origin Probability Estimation
8. AIS Ingestion
9. AIS Track Reconstruction
10. Candidate Vessel Generation
11. Hypothesis Engine
12. Evidence Engine
13. Falsification Engine
14. Counterfactual Engine
15. Uncertainty Engine
16. Attribution Engine
17. Abstention Engine
18. Next-Best-Evidence Engine
19. Investigation UI
20. Experiment/Evaluation Framework
21. Demo Mode
22. Provenance and Audit Trail
```

---

# 5. FIRST STEP: INSPECT THE WORKSPACE

Before modifying anything:

1. Inspect all files.
2. Identify existing code.
3. Identify frameworks.
4. Identify environment variables.
5. Identify datasets.
6. Identify documentation.
7. Identify build configuration.
8. Identify test infrastructure.
9. Identify Git status/history where relevant.
10. Identify existing reusable components.

Produce:

`docs/repository_audit.md`

Include:

* current architecture
* reusable components
* technical debt
* missing infrastructure
* risks
* recommendations

Do not overwrite existing work blindly.

---

# 6. PHASE 1 — OFFICIAL REQUIREMENTS

Verify the current official SIH26143 statement using the official SIH source available to the agent.

Create:

`docs/sih_requirements.md`

Extract:

* exact problem statement
* organization
* theme
* category
* explicit requirements
* expected solution
* required datasets/data sources
* stated constraints
* optional capabilities
* ambiguous areas
* potential innovation areas

Separate:

`REQUIRED`

from

`OPTIONAL`

from

`OUR ADDITIONS`

---

# 7. PHASE 2 — PRIOR ART

Perform a serious prior-art review.

Investigate:

## Operational systems

* CleanSeaNet
* INCOIS/OOSA
* other maritime pollution systems
* government EO monitoring systems
* commercial maritime intelligence products

## Academic research

Search for:

* Sentinel-1 oil spill detection
* SAR oil spill segmentation
* look-alike rejection
* oil spill drift modelling
* backward trajectory reconstruction
* AIS correlation
* vessel attribution
* oil-spill source identification
* trajectory anomaly detection
* counterfactual attribution
* uncertainty-aware attribution
* active sensing
* information-gain-based evidence acquisition

## Public SIH implementations

Search for publicly available SIH26143 repositories, demos, papers, videos, articles and project reports.

Create:

`docs/prior_art.md`

For every meaningful system:

```text
Name
Organization/team
Year
Inputs
Method
Outputs
Strengths
Weaknesses
Overlap with SIH26143
Potential differentiation
Source
```

Do not claim:

> "No one has done this."

Use language such as:

> "In the sources reviewed, we did not identify..."

---

# 8. PHASE 3 — DATA REGISTRY

Create:

`docs/data_registry.md`

Investigate publicly usable sources for:

## Satellite

* Sentinel-1
* Sentinel-2 when applicable
* other open EO sources if appropriate

## Environmental

* wind
* ocean currents
* waves
* sea-surface conditions
* weather/reanalysis

## AIS

* historical AIS
* vessel metadata
* vessel trajectories
* AIS data quality

## Incident/ground truth

* historical oil-spill events
* documented incidents
* known-source events

For each source record:

```text
Provider
URL
Coverage
Resolution
Temporal coverage
Format
License
Access process
Download size
Rate limitations
Data quality
Ground truth relation
Potential usage
Known limitations
```

---

# 9. PHASE 4 — HISTORICAL BENCHMARK CASES

Identify at least:

### Minimum: 3

### Target: 5–10

historical oil-spill incidents that are usable for experiments.

Each case should ideally contain:

* approximate event date
* approximate location
* usable satellite observation
* environmental data
* AIS data
* source/ground truth information

Create:

`data/metadata/cases.csv`

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

Do not call a case "ground truth" when only approximate incident information exists.

---

# 10. REPOSITORY STRUCTURE

Use a clear monorepo structure:

```text
SIH26143-MARITIME-FORENSICS/
│
├── README.md
├── LICENSE
├── .gitignore
├── .env.example
├── docker-compose.yml
│
├── docs/
│   ├── sih_requirements.md
│   ├── repository_audit.md
│   ├── prior_art.md
│   ├── data_registry.md
│   ├── architecture.md
│   ├── assumptions.md
│   ├── risks.md
│   ├── innovation_register.md
│   ├── evaluation.md
│   ├── demo_script.md
│   └── troubleshooting.md
│
├── data/
│   ├── raw/
│   ├── interim/
│   ├── processed/
│   ├── synthetic/
│   └── metadata/
│
├── experiments/
│   ├── case_001/
│   ├── case_002/
│   └── case_003/
│
├── reports/
│   ├── baseline_report.md
│   ├── validation_report.md
│   ├── ablation_report.md
│   └── adversarial_test_report.md
│
├── src/
│   ├── config/
│   ├── ingestion/
│   ├── detection/
│   ├── characterization/
│   ├── drift/
│   ├── ais/
│   ├── hypotheses/
│   ├── evidence/
│   ├── falsification/
│   ├── counterfactual/
│   ├── uncertainty/
│   ├── attribution/
│   ├── evidence_selection/
│   ├── evaluation/
│   └── api/
│
├── frontend/
│
└── tests/
```

---

# 11. TECHNOLOGY STACK

Use boring, mature technologies unless research shows a strong reason otherwise.

## Backend

Python 3.12+

FastAPI

Pydantic

SQLAlchemy

Alembic

## Scientific

NumPy

SciPy

Pandas

xarray

GeoPandas

Shapely

Rasterio

PyProj

GDAL where required

## ML

PyTorch

scikit-learn

Prefer modular interfaces so models can be swapped.

## Database

PostgreSQL

PostGIS

## Frontend

React

TypeScript

Vite

MapLibre GL JS or another open geospatial visualization library.

## API

REST/OpenAPI.

## Deployment

Docker

Docker Compose

## Quality

pytest

ruff

mypy where practical

pre-commit where practical

---

# 12. ARCHITECTURE

Implement this architecture:

```text
                    ┌──────────────────┐
                    │ Satellite / EO   │
                    └────────┬─────────┘
                             ↓
                    ┌──────────────────┐
                    │ Spill Detection  │
                    └────────┬─────────┘
                             ↓
                    ┌──────────────────┐
                    │ Characterization │
                    └────────┬─────────┘
                             ↓
                ┌────────────┴────────────┐
                ↓                         ↓
       Ocean / Weather              AIS Data
                ↓                         ↓
         Drift Engine              AIS Engine
                └────────────┬────────────┘
                             ↓
                      Origin Inference
                             ↓
                   Hypothesis Generator
                             ↓
                       Evidence Engine
                             ↓
                    Falsification Engine
                             ↓
                    Counterfactual Engine
                             ↓
                     Uncertainty Engine
                             ↓
             ┌───────────────┴──────────────┐
             ↓                              ↓
       Attribution                    Abstention
             ↓                              ↓
             └───────────────┬──────────────┘
                             ↓
                Next-Best-Evidence Engine
                             ↓
                       Investigation UI
```

---

# 13. BASELINE FIRST

Build a deliberately simple baseline.

Pipeline:

```text
Satellite
→ candidate oil slick
→ spill geometry
→ environmental data
→ backward drift
→ likely origin region
→ AIS candidate filtering
→ simple candidate ranking
```

Baseline ranking features may include:

* distance
* temporal compatibility
* trajectory intersection
* speed consistency
* course consistency
* origin probability

Keep it interpretable.

Document every formula and weighting assumption.

Create:

`reports/baseline_report.md`

---

# 14. SATELLITE INGESTION

Implement adapters for satellite sources.

Do not tie the system directly to one provider.

Use an abstraction:

```python
class SatelliteProvider:
    def search(self, query): ...
    def download(self, scene): ...
    def metadata(self, scene): ...
```

Store:

* acquisition timestamp
* orbit information if available
* bounds
* resolution
* source
* preprocessing status
* provenance

---

# 15. SATELLITE PREPROCESSING

Implement a reproducible preprocessing pipeline.

Depending on source:

* calibration
* clipping
* normalization
* denoising where justified
* geometric preprocessing
* masking where justified

Preserve original metadata.

Never silently transform data.

---

# 16. OIL-SPILL DETECTION

Create a pluggable detector API:

```python
class SpillDetector:
    def detect(self, scene) -> SpillDetectionResult:
        ...
```

Implement an initial baseline detector.

Then implement a more advanced ML detector if data supports it.

Possible outputs:

```text
spill_mask
spill_polygon
candidate_regions
confidence
lookalike_flags
quality_flags
```

Do not claim oil confirmation merely from low backscatter/dark pixels.

---

# 17. LOOK-ALIKE HANDLING

Explicitly account for possible false positives.

Investigate and model:

* low-wind areas
* natural phenomena
* sea-surface patterns
* wakes
* atmospheric effects
* other SAR dark features

Output:

```text
oil_likelihood
lookalike_risk
detection_quality
```

where supported by the available evidence.

---

# 18. SPILL CHARACTERIZATION

Compute:

* area
* perimeter
* centroid
* bounding box
* orientation
* elongation
* fragmentation
* compactness
* confidence

Do not manufacture an exact spill age unless validated.

---

# 19. ENVIRONMENTAL DATA ENGINE

Create a common environment interface:

```python
class EnvironmentalProvider:
    def get_currents(...)
    def get_wind(...)
    def get_waves(...)
```

Support historical retrieval and cached local data.

Every environmental field must include:

* timestamp
* coordinate system
* units
* spatial resolution
* temporal resolution
* source

---

# 20. DRIFT ENGINE

Implement a modular drift system.

First version:

Particle-based simplified transport model.

Conceptually:

```text
position(t+dt) =
position(t)
+
current_velocity * dt
+
wind_component * dt
+
stochastic_component
```

Document the approximation.

Do not call it a complete operational ocean model.

---

# 21. FORWARD DRIFT

Given a candidate source location/time:

simulate:

```text
source
→ trajectory
→ predicted slick distribution
```

Store:

* particles
* time
* positions
* environmental conditions
* parameters
* model version

---

# 22. BACKWARD DRIFT / HINDCAST

Given observed spill:

estimate:

```text
observed slick
→ candidate origin locations
→ candidate release times
```

Do not reduce the result to one point.

Produce an:

# Origin probability surface

Store as:

* raster
* contours
* vectorized region
* summary statistics

---

# 23. AIS INGESTION

Create:

```python
class AISProvider:
    def search_tracks(...)
    def load_messages(...)
    def load_vessel_metadata(...)
```

Support:

* MMSI
* timestamp
* latitude
* longitude
* speed
* course
* heading where available
* vessel type
* vessel name where available

---

# 24. AIS TRACK RECONSTRUCTION

Implement:

* sorting
* duplicate removal
* quality filtering
* interpolation where justified
* gap detection
* trajectory segmentation

Do NOT automatically mark AIS gaps as suspicious.

A gap means:

> insufficient observation/data quality

until evidence supports another interpretation.

---

# 25. CANDIDATE VESSEL GENERATION

Filter candidates based on:

1. spatial compatibility
2. temporal compatibility
3. movement feasibility
4. trajectory intersection with origin probability
5. data quality

Do not use distance alone.

---

# 26. HYPOTHESIS ENGINE

Create hypothesis objects.

Examples:

```text
Vessel A
Vessel B
Vessel C
Offshore infrastructure
Pipeline/shore source
Unknown
False positive
```

Each hypothesis has:

```text
id
type
subject
prior/initial belief
supporting evidence
contradicting evidence
uncertainty
status
```

---

# 27. EVIDENCE ENGINE

Every piece of evidence must be represented explicitly.

Example:

```json
{
  "type": "trajectory_consistency",
  "value": 0.84,
  "direction": "supports",
  "source": "AIS",
  "quality": 0.91,
  "explanation": "Track intersects the high-probability origin region during the inferred release window."
}
```

Evidence must always retain provenance.

---

# 28. EVIDENCE GRAPH

Represent:

```text
Incident
   ↓
Observation
   ↓
Origin
   ↓
Hypothesis
   ↓
Evidence
   ↓
Conclusion
```

Store relationships.

Expose them in the UI.

---

# 29. FALSIFICATION ENGINE

The most important innovation component.

For every leading hypothesis, ask:

## Spatial challenge

Does the candidate fit the origin distribution?

## Temporal challenge

Could the candidate physically have been there?

## Drift challenge

Would the observed spill be reachable from the candidate?

## Shape challenge

Does simulated morphology resemble the observation?

## AIS challenge

Is AIS coverage sufficient?

## Alternative-source challenge

Does another explanation fit equally well?

## Data-quality challenge

Does the conclusion depend excessively on uncertain data?

Output:

```json
{
  "hypothesis_id": "H1",
  "survives": true,
  "supporting": [],
  "contradicting": [],
  "failure_modes": [],
  "sensitivity": {}
}
```

---

# 30. COUNTERFACTUAL ENGINE

For each serious candidate:

> Assume this candidate is the source.

Run forward simulation.

Compare:

```text
predicted spill
vs
observed spill
```

Metrics may include:

* centroid error
* spatial overlap
* area error
* orientation difference
* shape similarity
* arrival-time error

Make all formulas explicit and testable.

---

# 31. UNCERTAINTY ENGINE

Quantify, where justified:

* detection uncertainty
* origin uncertainty
* time uncertainty
* drift uncertainty
* AIS data quality
* attribution uncertainty

Distinguish:

```text
Data uncertainty
Model uncertainty
Measurement uncertainty
Coverage uncertainty
```

Do not output false numerical precision.

---

# 32. ATTRIBUTION ENGINE

Create a transparent attribution layer.

It should aggregate evidence using a documented statistical or probabilistic method.

Possible approaches:

* likelihood ratios
* Bayesian updating
* calibrated classifier
* probabilistic graphical model

Do not choose a mathematically sophisticated method merely because it sounds impressive.

Benchmark it against simpler approaches.

---

# 33. ABSTENTION ENGINE

The system must be able to say:

# INSUFFICIENT EVIDENCE

Trigger based on validated criteria such as:

* competing hypotheses too close
* poor data quality
* insufficient AIS coverage
* drift uncertainty too large
* false-positive risk too high

Never hard-code a visually appealing threshold without evaluation.

---

# 34. NEXT-BEST-EVIDENCE ENGINE

This is a key research component.

Ask:

> What additional observation would reduce uncertainty the most?

Candidate actions:

* new SAR observation
* optical image
* higher-resolution imagery
* additional AIS analysis
* environmental data
* infrastructure verification
* alternate drift model

Formally estimate:

```text
Expected information gain
=
expected uncertainty before
-
expected uncertainty after hypothetical evidence
```

Possible uncertainty metrics:

* entropy
* posterior spread
* candidate ranking instability

The recommendation must be generated algorithmically.

---

# 35. CLOSED-LOOP UPDATE

When new evidence is added:

```text
new evidence
→ update hypotheses
→ re-run relevant analysis
→ update uncertainty
→ update attribution
→ update next-best-evidence
```

The investigation must maintain an audit trail.

---

# 36. INCIDENT OBJECT MODEL

Create a central investigation object:

```json
{
  "incident_id": "",
  "observations": [],
  "detections": [],
  "origin_estimate": {},
  "environment": {},
  "ais": {},
  "hypotheses": [],
  "evidence": [],
  "falsification_results": [],
  "counterfactuals": [],
  "attribution": {},
  "uncertainty": {},
  "next_best_evidence": [],
  "provenance": {}
}
```

---

# 37. DATABASE MODEL

Use PostgreSQL + PostGIS.

Tables/entities:

```text
incident
satellite_scene
spill_detection
spill_geometry
environmental_observation
drift_simulation
drift_particle
vessel
ais_message
ais_track
hypothesis
evidence
falsification_test
counterfactual_simulation
attribution_result
uncertainty_estimate
evidence_recommendation
experiment
provenance_record
```

Use migrations.

Add spatial indexes.

---

# 38. API

Implement FastAPI endpoints approximately:

```text
GET    /api/v1/incidents
POST   /api/v1/incidents

GET    /api/v1/incidents/{id}

POST   /api/v1/detection/run
POST   /api/v1/drift/backward
POST   /api/v1/drift/forward

POST   /api/v1/ais/search
POST   /api/v1/ais/reconstruct

POST   /api/v1/hypotheses/generate
POST   /api/v1/evidence/evaluate

POST   /api/v1/falsification/run
POST   /api/v1/counterfactual/run

POST   /api/v1/attribution/run
POST   /api/v1/uncertainty/run

POST   /api/v1/evidence-selection/run

GET    /api/v1/incidents/{id}/investigation
GET    /api/v1/incidents/{id}/provenance

GET    /api/v1/evaluation
GET    /api/v1/health
```

Generate OpenAPI documentation automatically.

---

# 39. FRONTEND

Use React + TypeScript.

Build a professional investigation workstation.

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

# 40. MAIN INVESTIGATION SCREEN

Design around a large geospatial canvas.

## MAP LAYERS

* satellite imagery
* spill segmentation
* spill boundary
* origin probability
* current vectors
* wind vectors
* AIS tracks
* candidate vessels
* infrastructure
* counterfactual trajectories
* uncertainty zones

---

# 41. EVIDENCE PANEL

For every candidate show:

```text
Candidate
Attribution support
Evidence quality
Confidence
Evidence FOR
Evidence AGAINST
Data gaps
Falsification status
```

---

# 42. WHY BUTTON

Every major conclusion must have:

# WHY?

Clicking should show:

```text
Evidence supporting
Evidence contradicting
Data quality
Assumptions
Model used
Relevant observations
```

---

# 43. ATTACK HYPOTHESIS BUTTON

Add:

# TRY TO DISPROVE

When clicked:

1. run falsification
2. run counterfactual if applicable
3. identify contradictions
4. update result
5. show exactly what changed

This must work in the actual product.

---

# 44. NEXT EVIDENCE PANEL

Show:

```text
NEXT BEST EVIDENCE

Recommended action
Why it matters
Which hypotheses it separates
Expected information gain
Current uncertainty
```

Do not hard-code textual recommendations.

---

# 45. ATTRIBUTION VIEW

Example:

```text
LEADING HYPOTHESIS

Vessel A

Support: Moderate
Evidence quality: Medium
Confidence: Not sufficient for definitive attribution

Supporting:
+ Temporal compatibility
+ Trajectory compatibility
+ Drift consistency

Contradicting:
- AIS gap
- Vessel B also plausible

Decision:
INSUFFICIENT EVIDENCE

Next:
Acquire / inspect evidence X
```

---

# 46. INVESTIGATION TIMELINE

Show:

```text
Satellite observation
AIS events
Estimated release window
Drift timeline
Vessel movements
Evidence updates
Hypothesis changes
```

Users should be able to scrub the timeline.

---

# 47. MAP INTERACTION

Support:

* pan
* zoom
* layer toggles
* candidate selection
* time slider
* trajectory animation
* origin heatmap
* evidence overlays
* uncertainty overlays

Do not overload the map.

---

# 48. DEMO MODE

Build a deterministic demo environment.

Environment variable:

```text
DEMO_MODE=true
```

Demo mode must function without live external APIs.

Pre-cache:

* satellite scene
* environmental data
* AIS sample
* historical case
* model outputs where appropriate

The UI must clearly indicate when demo data is being used.

---

# 49. DEMO SCRIPT

Target duration:

# 3–5 minutes

Suggested story:

```text
1. Choose incident
2. Show satellite image
3. Detect spill
4. Show origin reconstruction
5. Show vessel traffic
6. Generate competing hypotheses
7. Select leading candidate
8. Click TRY TO DISPROVE
9. Reveal contradictory evidence
10. Recalculate attribution
11. Show uncertainty
12. Trigger NEXT BEST EVIDENCE
13. Introduce additional evidence
14. Recalculate
15. Show final result
```

Do not rely on internet connectivity during the competition demo.

---

# 50. EXPERIMENT FRAMEWORK

Create reproducible experiment definitions.

Each experiment must contain:

```text
config.json
inputs/
outputs/
metrics.json
report.md
```

Record:

* data version
* model version
* code commit
* parameters
* random seeds
* runtime
* metrics
* conclusions

---

# 51. BENCHMARK

Compare at least:

## Baseline

```text
Simple spatial/temporal AIS ranking
```

versus:

## Proposed

```text
Hypotheses
+
Evidence
+
Falsification
+
Counterfactual
+
Uncertainty
+
Abstention
```

---

# 52. REQUIRED METRICS

## Detection

* precision
* recall
* F1
* IoU
* false positive rate

## Origin

* location error
* time error
* probability-region coverage

## Attribution

* Top-1 accuracy
* Top-3 accuracy
* MRR where appropriate
* false attribution rate

## Calibration

If probabilities are used:

* Brier score
* reliability curve
* calibration metrics

## Abstention

Measure:

* abstention rate
* correct abstention rate
* false attribution avoided

## Next-best-evidence

Measure:

* expected information gain
* realized uncertainty reduction where simulation permits

---

# 53. ABLATION STUDY

We must identify which components actually matter.

Run experiments such as:

```text
Baseline

Baseline + drift

Baseline + drift + evidence fusion

Baseline + drift + evidence fusion + falsification

Full system
```

This will tell us whether the "innovation" contributes real value.

---

# 54. ADVERSARIAL TESTING

Implement at least:

### Test A

Single obvious candidate.

### Test B

Two equally plausible vessels.

### Test C

Three nearby vessels.

### Test D

AIS gap.

### Test E

Poor satellite quality.

### Test F

Look-alike false positive.

### Test G

Non-vessel source.

### Test H

Conflicting environmental data.

### Test I

Multiple spills.

### Test J

No plausible candidate.

The system must not collapse into an arbitrary vessel selection.

---

# 55. FAILURE ANALYSIS

Create:

`reports/failure_analysis.md`

For every failed experiment:

```text
Case
Expected
Observed
Why it failed
Root cause
Impact
Potential fix
Whether fix is implemented
```

Never hide failures.

---

# 56. PROVENANCE

Every output should retain:

```text
dataset
source
timestamp
model
version
parameters
configuration
code version
random seed
```

Expose provenance where useful in the UI.

---

# 57. REPRODUCIBILITY

A new developer should be able to run:

```bash
git clone ...
cp .env.example .env
docker compose up --build
```

and reach the application.

README must include:

* prerequisites
* setup
* environment
* dataset setup
* migrations
* development
* testing
* demo mode
* troubleshooting

---

# 58. TESTING

## Unit tests

Cover:

* geospatial calculations
* coordinate transformations
* drift calculations
* AIS filtering
* evidence aggregation
* uncertainty calculations

## Integration tests

Cover:

```text
satellite → detection
detection → drift
drift → AIS
AIS → hypotheses
hypotheses → attribution
```

## End-to-end

At least one historical benchmark case.

## Frontend

Test:

* loading investigation
* map layers
* candidate selection
* hypothesis attack
* next-evidence recommendation
* timeline
* uncertainty display

---

# 59. SECURITY

Validate all external inputs.

Protect:

* file uploads
* GeoJSON
* raster metadata
* query parameters
* database queries
* API keys

Prevent:

* path traversal
* SQL injection
* XSS
* command injection
* credential exposure

Never commit secrets.

---

# 60. PERFORMANCE

Measure:

* satellite preprocessing
* inference
* drift simulation
* AIS query
* AIS reconstruction
* hypothesis evaluation
* counterfactual simulation
* API latency
* frontend rendering

Use:

* spatial indexes
* temporal indexes
* caching
* chunking
* vectorization
* asynchronous jobs

only when measurements justify them.

---

# 61. OBSERVABILITY

Use structured logging.

Log:

* request IDs
* pipeline stage
* execution time
* failures
* data source
* model version
* experiment ID

Do not log:

* secrets
* credentials
* unnecessary personal information

---

# 62. DOCUMENTATION ARTIFACTS

Maintain:

```text
docs/
├── sih_requirements.md
├── repository_audit.md
├── prior_art.md
├── data_registry.md
├── architecture.md
├── assumptions.md
├── risks.md
├── innovation_register.md
├── evaluation.md
├── demo_script.md
├── troubleshooting.md
└── scientific_methods.md
```

---

# 63. INNOVATION REGISTER

Create:

`docs/innovation_register.md`

For every innovation:

```text
Innovation
Existing prior art
What is different
Why the difference matters
How it will be measured
Current implementation status
Evidence supporting novelty/differentiation
```

Candidate innovations to investigate:

### A. Multi-hypothesis source attribution

### B. Self-falsification

### C. Counterfactual physical consistency

### D. Uncertainty-aware abstention

### E. Next-best-evidence selection

### F. Closed-loop investigation

Do not label any of these globally novel without evidence.

---

# 64. PRODUCT PRINCIPLES

The interface should feel like:

> a scientific investigation workstation

not:

> a generic AI startup dashboard.

Visual principles:

* map-first
* professional
* clear hierarchy
* restrained colors
* high readability
* evidence-centric
* minimal decoration

Avoid unnecessary animations and huge KPI cards.

---

# 65. OPTIONAL AI/LLM LAYER

An LLM may be used ONLY where it adds measurable value.

Possible legitimate uses:

* summarizing evidence
* converting scientific results into readable investigation notes
* generating reports from structured evidence
* answering questions over the investigation data

The LLM must never:

* invent evidence
* change numerical values
* override the scientific engine
* fabricate sources
* make unsupported attribution claims

Any generated text must reference the underlying structured evidence.

---

# 66. MODEL GOVERNANCE

Every ML model must have:

```text
model name
version
training data
test data
metrics
limitations
intended use
known failure modes
```

Never train and then report accuracy without dataset separation.

Avoid data leakage.

---

# 67. MACHINE LEARNING RULES

Do not automatically assume deep learning is best.

Test simple baselines first.

When training a model:

* split train/validation/test carefully
* avoid temporal leakage
* avoid spatial leakage where relevant
* document class imbalance
* report uncertainty
* evaluate on unseen cases

---

# 68. SCIENTIFIC VALIDATION RULES

For every scientific method:

Document:

```text
Assumptions
Input data
Equation/algorithm
Approximation
Validation
Failure mode
```

If the physics is simplified, state that clearly.

---

# 69. PHASED EXECUTION

You are authorized to build the complete system, but you MUST execute in logical gates.

## GATE 1 — Discovery

Produce:

```text
docs/repository_audit.md
docs/sih_requirements.md
docs/prior_art.md
docs/data_registry.md
docs/IMPLEMENTATION_PLAN.md
```

---

## GATE 2 — Data and benchmark

Produce:

* working data loaders
* 3 historical cases
* case metadata
* data validation scripts

---

## GATE 3 — Baseline

Produce:

```text
Satellite
→ Detection
→ Drift
→ AIS
→ Candidate ranking
```

with metrics.

---

## GATE 4 — Advanced reasoning

Produce:

```text
Hypothesis engine
Evidence engine
Falsification engine
Counterfactual engine
```

---

## GATE 5 — Uncertainty

Produce:

```text
Uncertainty
Abstention
Calibration
```

---

## GATE 6 — Next-best-evidence

Produce:

```text
Information gain
Evidence recommendations
Closed-loop updates
```

---

## GATE 7 — Product

Produce:

* FastAPI backend
* React frontend
* PostGIS database
* map interface
* investigation workflow

---

## GATE 8 — Validation

Produce:

* benchmark
* ablation
* adversarial tests
* failure analysis

---

## GATE 9 — Demo

Produce:

* deterministic demo case
* 3–5 minute demo script
* screenshots
* architecture diagram
* results

---

# 70. ARTIFACT REQUIREMENTS

After each major gate, generate a concise artifact:

```text
What changed
Files changed
Why
Tests run
Results
Limitations
Open risks
Recommended next step
```

Use markdown artifacts wherever practical.

Antigravity supports structured artifacts for implementation plans, code review, architecture diagrams and other deliverables, so use them as the project's checkpoints rather than hiding all progress inside raw code edits.

---

# 71. AGENT AUTONOMY RULES

Act autonomously on implementation decisions that do not change the product thesis.

For ambiguous requirements:

1. identify ambiguity
2. make the smallest defensible assumption
3. document it
4. proceed

For high-risk architectural decisions:

1. analyze alternatives
2. record tradeoffs
3. choose the simplest defensible option
4. document why

Do not stop unnecessarily for trivial decisions.

---

# 72. DO NOT ASK FOR PERMISSION FOR EVERY FILE

Proceed through the implementation gates autonomously.

However:

* do not delete large amounts of existing work without inspection
* do not expose secrets
* do not access unrelated personal files
* do not commit credentials
* do not fabricate research

---

# 73. GIT STRATEGY

Use small logical commits.

Example:

```text
chore: initialize project structure
docs: add SIH requirements and prior-art review
feat: add satellite ingestion
feat: add spill detection baseline
feat: add drift reconstruction
feat: add AIS candidate engine
feat: add hypothesis engine
feat: add falsification engine
feat: add uncertainty and abstention
feat: add next-best-evidence engine
feat: add investigation UI
test: add historical benchmark
docs: add evaluation results
```

Never make one gigantic unreviewable commit.

---

# 74. QUALITY BAR

The system is not considered complete merely because:

* the frontend renders
* APIs respond
* a model runs
* a demo screenshot exists

It is considered successful only when:

1. real/open data is loaded reproducibly
2. at least one real historical case runs end-to-end
3. baseline performance is measured
4. proposed reasoning system is measured
5. uncertainty is explicit
6. abstention works
7. next-best-evidence works
8. provenance works
9. failures are documented
10. the entire demo can run deterministically

---

# 75. DEFINITION OF DONE

The final product should allow an investigator to:

```text
1. Open a maritime incident
2. Review satellite observations
3. Inspect detected spill
4. Review spill geometry
5. Inspect environmental conditions
6. Review probable origin region
7. Inspect vessel traffic
8. Generate candidate hypotheses
9. Review supporting evidence
10. Review contradicting evidence
11. Attack a leading hypothesis
12. Run counterfactual consistency testing
13. Inspect uncertainty
14. Receive attribution or abstention
15. Request next-best evidence
16. Add new evidence
17. Recalculate the investigation
18. Export an investigation report
```

---

# 76. REPORT EXPORT

Implement export to:

* PDF-friendly HTML or print layout
* Markdown
* JSON

The report should include:

```text
Incident summary
Satellite evidence
Detected spill
Origin reconstruction
Environmental conditions
AIS candidate set
Hypotheses
Evidence
Contradicting evidence
Falsification results
Counterfactual results
Uncertainty
Attribution/abstention
Next-best-evidence
Provenance
Limitations
```

---

# 77. SIH PRESENTATION SUPPORT

Generate machine-readable artifacts that help create the final SIH presentation:

```text
reports/
├── architecture_summary.md
├── innovation_summary.md
├── evaluation_summary.md
├── demo_summary.md
├── impact_summary.md
└── limitations_summary.md
```

Never inflate results for presentation.

---

# 78. FINAL DEMO NARRATIVE

The product should communicate:

### Problem

A satellite observes a suspected oil spill.

### Challenge

The source is uncertain.

### Existing limitation

Simply finding nearby vessels is not enough.

### Our system

Reconstructs the event and evaluates competing explanations.

### Signature interaction

# TRY TO DISPROVE THIS HYPOTHESIS

### Signature safety behavior

# INSUFFICIENT EVIDENCE

### Signature intelligence feature

# NEXT BEST EVIDENCE

### Result

The investigator gets a defensible, evidence-linked assessment rather than an unsupported guess.

---

# 79. PROJECT MOTTO

Use internally:

> **Detect less. Understand more.**

Optional extended version:

> **From observation to evidence-backed attribution.**

---

# 80. FINAL COMMAND TO THE AGENT

START NOW.

Do not build the entire system blindly in a single uncontrolled pass.

Execute the project in gates, but continue autonomously through the gates when the previous gate passes its validation criteria.

First:

1. Inspect repository.
2. Verify current SIH26143 requirements.
3. Research prior art.
4. Research data.
5. Identify benchmark cases.
6. Create the architecture.
7. Create the implementation plan.
8. Begin implementation.

At every gate:

* test
* measure
* document
* challenge assumptions
* preserve provenance
* record limitations
* continue

If a proposed innovation is already well established, do not pretend it is novel. Modify the idea or find a stronger differentiator.

If a dataset is unavailable, do not fabricate it. Find an alternative or change the experiment.

If the advanced approach does not beat the baseline, report that honestly and iterate.

If the system cannot reliably support attribution, prefer abstention over a fabricated confident answer.

The goal is not to produce the largest codebase.

The goal is to produce a:

# SCIENTIFICALLY DEFENSIBLE

# TECHNICALLY STRONG

# EXPLAINABLE

# REPRODUCIBLE

# MEASURABLY BETTER

# SIH-READY

# MARITIME FORENSIC INTELLIGENCE SYSTEM.

Begin with repository discovery and create the first implementation artifacts.

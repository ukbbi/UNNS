# TIME-CRYSTAL-I v1.1.0 — Extended User Guide

## 1. Purpose of this chamber

`TIME-CRYSTAL-I` is a hierarchical UNNS chamber for evaluating **temporal structural admissibility** in candidate time-crystal systems.

Its central rule is:

> **Temporal recurrence is necessary but not sufficient.**

For a quantum many-body candidate, the chamber separates four evidence sectors:

1. **Temporal**
2. **Rigidity**
3. **Collective**
4. **Spectral**

The highest chamber verdict:

`MANY_BODY_TIME_CRYSTAL_ADMISSIBLE`

requires all four quantum many-body sectors to be supported.

The chamber deliberately does **not** equate period doubling, `q0 = 2`, or even strong temporal recurrence with time crystallinity.

---

# 2. The three Windows BAT files

The three BAT files have completely different jobs.

---

## 2.1 `RUN_WINDOWS.bat`

### Purpose

`RUN_WINDOWS.bat` is the **chamber self-validation / startup runner**.

Use it when you want to verify that the installed `TIME-CRYSTAL-I` chamber is internally healthy and still reproduces its original validation corpus.

It does **not** analyze a new outside experiment.

### What it does

The BAT file looks for these six sibling artifacts:

```text
TC_PHYS_v001
TC_CLOSURE_v001
TC_EXT_MI_v001
TC_CTRL_v001
TC_RIGIDITY_v001
TC_COLLECTIVE_v001
```

Each may exist either as an extracted folder or as its corresponding `.zip`.

It then:

1. changes into the chamber folder;
2. checks that all six required sibling artifacts exist;
3. runs the Python unit tests in `tests/`;
4. runs the initial 10-record validation corpus;
5. regenerates:
   - `outputs/validation_results.json`
   - `outputs/validation_summary.csv`
   - `outputs/RUN_LOG.txt`
   - `CHAMBER_DATA.js`
6. opens:
   - `TIME-CRYSTAL-I.html`

### When to use it

Use `RUN_WINDOWS.bat`:

- after copying the chamber to a new computer;
- after moving the chamber folder;
- after replacing one of its sibling source packages;
- when you want to confirm that the chamber still gives:
  `PASS_INITIAL_VALIDATION_CORPUS`;
- before starting serious external candidate work.

### Expected result

The key result should be:

```text
STATUS: PASS_INITIAL_VALIDATION_CORPUS
```

The expected initial classifications include:

```text
Mi MBL-DTC
→ MANY_BODY_TIME_CRYSTAL_ADMISSIBLE

Mi prethermal
→ TEMPORAL_RECURRENCE

Mi thermal
→ NO_TEMPORAL_ORDER

Exact classical 2T
→ RIGID_RECURRENCE
```

and the other validation controls listed in the HTML interface.

### Important

`RUN_WINDOWS.bat` evaluates the **known validation corpus**.

It is therefore a **chamber integrity check**, not a prospective blind experiment.

---

## 2.2 `RUN_EXTERNAL_WINDOWS.bat`

### Purpose

`RUN_EXTERNAL_WINDOWS.bat` is the **new-experiment runner**.

This is the BAT file to use when you want `TIME-CRYSTAL-I` to analyze a candidate experiment that was not part of the original chamber validation corpus.

It runs the chamber in **Blind Mode**.

### What it expects

It expects a standardized candidate evidence bundle, either:

```text
CANDIDATE.zip
```

or an extracted candidate folder.

Use:

```text
CANDIDATE_TEMPLATE.zip
```

as the canonical layout.

### What it does

The BAT file:

1. receives or asks for the candidate bundle path;
2. checks that Python can import NumPy;
3. runs:

```bat
python run_external.py "<candidate>" "<output>" --blind
```

4. produces a new blind-analysis output folder under:

```text
external_outputs\
```

5. writes the chamber verdict before any ground truth is revealed.

### Main outputs

A successful blind run creates:

```text
external_result.json
blind_verdict.json
analysis_lock.json
evidence_audit.json
EVIDENCE_AUDIT.md
RUN_LOG.txt
```

### Meaning of the outputs

#### `blind_verdict.json`

The canonical blind chamber result.

It contains:

- candidate ID;
- domain;
- calculated four-sector evidence;
- chamber verdict;
- verdict path;
- provenance.

#### `analysis_lock.json`

Cryptographically locks the analysis before the answer is revealed.

It records:

- evidence SHA-256;
- frozen temporal metric SHA-256;
- protocol SHA-256;
- verdict;
- chamber version;
- analysis-lock SHA-256.

This is the methodological firewall between analysis and reveal.

#### `EVIDENCE_AUDIT.md`

Human-readable report of:

- what evidence was found;
- what evidence was missing;
- which metrics were calculated;
- which sector gates passed or failed;
- which evidence is needed for a higher verdict.

#### `evidence_audit.json`

Machine-readable version of the same evidence audit.

### When to use it

Use `RUN_EXTERNAL_WINDOWS.bat` when asking:

> **What level of temporal structural admissibility does this new system possess?**

This is the normal entry point for a genuinely new candidate.

### Important distinction

`RUN_EXTERNAL_WINDOWS.bat` does **not** use the candidate's known physical label to determine the verdict.

The blind analyzer uses a neutral candidate ID and measured evidence.

---

## 2.3 `REVEAL_WINDOWS.bat`

### Purpose

`REVEAL_WINDOWS.bat` is **not an analysis runner**.

It is the **post-analysis reveal step**.

Use it only **after** a Blind Mode run has already produced:

```text
blind_verdict.json
analysis_lock.json
```

### Why it exists

If the physical identity or expected answer is shown to the chamber before analysis, the experiment is no longer blind.

The correct order is:

```text
candidate evidence
        ↓
blind analysis
        ↓
blind verdict
        ↓
analysis lock
        ↓
ONLY NOW reveal physical identity
```

`REVEAL_WINDOWS.bat` performs that final step.

### What it asks for

It asks for:

```text
Blind output folder:
```

and:

```text
Ground truth JSON path:
```

The ground truth file must be separate from the candidate bundle.

Example:

```json
{
  "candidate_id": "candidate_001",
  "physical_class": "known experimental classification",
  "expected_verdict": "MANY_BODY_TIME_CRYSTAL_ADMISSIBLE"
}
```

### What it runs

Internally:

```bat
python reveal_external.py "<blind_output>" "<ground_truth.json>"
```

### Output

It creates:

```text
posthoc_comparison.json
```

This records:

- the previously locked blind verdict;
- the revealed physical classification;
- the expected verdict;
- whether the blind verdict matched;
- the lock hash;
- the ground-truth SHA-256.

### Scientific meaning

`REVEAL_WINDOWS.bat` answers:

> Did the chamber's **already locked** structural verdict agree with the independently known physical identity?

It must never be run first.

---

# 3. The three BAT files in one sentence

```text
RUN_WINDOWS.bat
= Is the chamber itself still valid?

RUN_EXTERNAL_WINDOWS.bat
= What does the chamber say about a new candidate?

REVEAL_WINDOWS.bat
= After the answer is locked, did it agree with ground truth?
```

Or as a workflow:

```text
CHAMBER INSTALLATION
        │
        ▼
RUN_WINDOWS.bat
        │
        │ chamber passes
        ▼
NEW CANDIDATE
        │
        ▼
RUN_EXTERNAL_WINDOWS.bat
        │
        ▼
blind_verdict.json
analysis_lock.json
        │
        │ only now reveal answer
        ▼
REVEAL_WINDOWS.bat
        │
        ▼
posthoc_comparison.json
```

---

# 4. Recommended chamber folder layout

A practical project root is:

```text
Time_crystal\
│
├── TC_PHYS_v001\
├── TC_CLOSURE_v001\
├── TC_COLLECTIVE_v001\
├── TC_CTRL_v001\
├── TC_EXT_MI_v001\
├── TC_INGEST_v001\
├── TC_RIGIDITY_v001\
│
├── TIME-CRYSTAL-I_v1_1_0\
│
├── Data.zip
└── DTC_Data.zip
```

Inside:

```text
TIME-CRYSTAL-I_v1_1_0\
```

the important files are:

```text
frozen\
outputs\
protocols\
templates\
tests\

BLIND_PROTOCOL.md
CANDIDATE_TEMPLATE.zip
CHAMBER_DATA.js
CHANGELOG.md
DEMO_QMB_001.zip
DEMO_QMB_001_GROUND_TRUTH.json
EVIDENCE_AUDIT.md
EXTERNAL_ANALYSIS.md
README.md
RESULT_SUMMARY.md
RULES.json
run_chamber.py
run_external.py
RUN_EXTERNAL_WINDOWS.bat
RUN_WINDOWS.bat
SCHEMA.json
SOURCE_HASHES.json
SPEC.md
TIME-CRYSTAL-I.css
TIME-CRYSTAL-I.html
TIME-CRYSTAL-I.js
```

and:

```text
reveal_external.py
REVEAL_WINDOWS.bat
```

---

# 5. First-time setup

## 5.1 Python

Open Command Prompt and check:

```bat
python --version
```

A Python 3 installation is required.

## 5.2 External Analysis dependency

External Analysis Mode requires NumPy.

Install it with:

```bat
python -m pip install numpy
```

The main chamber validation itself uses the existing chamber artifacts and standard Python machinery, but the raw-evidence external analyzer uses NumPy.

---

# 6. First thing to do after installing the chamber

Run:

```text
RUN_WINDOWS.bat
```

Do not begin prospective analysis until the chamber reports:

```text
PASS_INITIAL_VALIDATION_CORPUS
```

Then the browser interface should open automatically.

---

# 7. The HTML / JavaScript interface

Open:

```text
TIME-CRYSTAL-I.html
```

The interface works locally and does not need an internet connection.

It shows:

- chamber status;
- validation corpus;
- domain;
- detected `q0`;
- temporal sector;
- rigidity sector;
- collective sector;
- spectral sector;
- final verdict;
- verdict path;
- evidence;
- provenance.

## Filtering

The verdict selector can display:

```text
NO_TEMPORAL_ORDER
TEMPORAL_RECURRENCE
RIGID_RECURRENCE
COLLECTIVE_TEMPORAL_ORDER
MANY_BODY_TIME_CRYSTAL_ADMISSIBLE
INSUFFICIENT_DOMAIN_EVIDENCE
```

## Loading an analysis result

After an external run, use:

```text
Load result / candidate JSON
```

and load:

```text
blind_verdict.json
```

or:

```text
external_result.json
```

The chamber page will display the outside candidate using the same visual sector structure.

## Exporting for outside analysis

Use:

```text
Export ▾
```

Available exports include:

- selected result JSON;
- selected Markdown report;
- visible/filtered table CSV;
- full chamber result JSON;
- full corpus CSV.

These browser exports are generated locally.

---

# 8. Preparing a new external candidate

Start from:

```text
CANDIDATE_TEMPLATE.zip
```

The canonical structure is:

```text
TC_CANDIDATE\
│
├── manifest.json
│
├── temporal\
│   └── trajectories.csv
│
├── rigidity\
│   ├── initial_state_trajectories.csv
│   └── perturbation_scan.csv
│
├── collective\
│   ├── size_scaling.csv
│   ├── initial_state_order.csv
│   └── perturbation_profile.csv
│
└── spectral\
    └── typicality.csv
```

Not every higher-sector file must exist.

The chamber must never invent missing evidence.

Missing quantum evidence is recorded as:

```text
NOT_TESTED
```

For a classical/generic system, quantum-only sectors may correctly be:

```text
N/A
```

---

# 9. `manifest.json`

A minimal manifest is:

```json
{
  "candidate_id": "candidate_001",
  "label": "Candidate 001",
  "domain": "quantum_many_body",
  "protocol": "quantum_dtc_v1_1_0"
}
```

For a genuine blind test, do not put the known physical classification or expected verdict into this bundle.

Keep that information in a separate ground-truth file.

---

# 10. Temporal evidence

File:

```text
temporal\trajectories.csv
```

Format:

```csv
t,x0,x1,x2,x3
0,1.00,0.91,0.84,0.79
1,-0.99,-0.89,-0.82,-0.77
2,0.98,0.90,0.81,0.76
```

Rules:

- first column = time / Floquet cycle / sample index;
- all remaining columns = simultaneous state coordinates;
- do not pre-align signs to force period doubling;
- do not smooth specifically to create a desired `q0`;
- preserve the actual experimental trajectory.

The chamber sends this evidence to the frozen temporal-closure implementation.

The frozen metric SHA-256 is:

```text
06344c8641aa14e6663cc3cba65d86fcdb9e37857909e85da6bc0d689e5b2553
```

---

# 11. Rigidity evidence

Two evidence forms are supported.

## 11.1 Initial-state trajectories

```text
rigidity\initial_state_trajectories.csv
```

Example:

```csv
t,state_A,state_B,state_C
0,1.0,0.91,0.82
1,-0.98,-0.90,-0.80
2,0.97,0.89,0.79
```

The chamber evaluates all pairwise combinations.

It measures:

- recurrence-family contrast;
- temporal-order shuffle significance;
- pairwise universality.

## 11.2 Perturbation scan

```text
rigidity\perturbation_scan.csv
```

Format:

```csv
perturbation,family_contrast
0.00,0.82
0.02,0.81
0.04,0.80
0.06,0.74
0.08,0.42
```

The frozen basin-exit rule is applied.

Do not rename the required columns.

---

# 12. Collective evidence

## 12.1 Finite-size scaling

```text
collective\size_scaling.csv
```

Format:

```csv
size,order
8,0.20
12,0.28
16,0.35
20,0.42
```

The chamber calculates the finite-size scaling exponent.

## 12.2 Broad initial-state order

```text
collective\initial_state_order.csv
```

Format:

```csv
state_id,order
0,0.41
1,0.39
2,0.40
```

This sector evaluates:

- mean absolute order;
- standard deviation;
- coefficient of variation;
- breadth across states.

## 12.3 Perturbation profile

Optional:

```text
collective\perturbation_profile.csv
```

Format:

```csv
position,response
0,0.01
1,0.04
2,0.91
3,0.04
4,0.01
```

The chamber can calculate:

- IPR;
- effective number of sites.

This is supporting evidence only.

It is not sufficient by itself to establish a many-body time-crystal verdict.

---

# 13. Spectral / typicality evidence

File:

```text
spectral\typicality.csv
```

Long format:

```csv
K,value
0,0.41
0,0.40
0,0.39
20,0.38
20,0.37
20,0.39
```

`K` is the scrambling depth or corresponding experimental spectral-breadth coordinate.

The chamber compares initial and final typical-state response.

For classical systems this quantum-only sector is not artificially scored zero.

It is:

```text
N/A
```

---

# 14. Running a new candidate

There are two easy Windows methods.

## Method A — drag and drop

Drag:

```text
candidate.zip
```

onto:

```text
RUN_EXTERNAL_WINDOWS.bat
```

This supplies the candidate path as a BAT argument.

## Method B — double-click

Double-click:

```text
RUN_EXTERNAL_WINDOWS.bat
```

The terminal will ask:

```text
Candidate bundle path:
```

Paste or type the full path.

### Small Windows naming detail

When the candidate is supplied by drag-and-drop, the output folder is normally
named after the candidate file.

When the BAT is opened first and the path is entered interactively, the current
BAT implementation may use the generic output name:

```text
external_outputs\candidate\
```

This does not affect the scientific result.

---

# 15. Reading the external output

A typical output folder is:

```text
external_outputs\candidate_name\
```

Inside:

```text
blind_verdict.json
analysis_lock.json
external_result.json
evidence_audit.json
EVIDENCE_AUDIT.md
RUN_LOG.txt
```

Recommended reading order:

```text
1. RUN_LOG.txt
2. EVIDENCE_AUDIT.md
3. blind_verdict.json
4. analysis_lock.json
```

Do not reveal the ground truth yet.

---

# 16. Evidence Audit interpretation

The audit should be treated as part of the result.

Example:

```text
Temporal
SUPPORTED

Rigidity
SUPPORTED

Collective
NOT_TESTED

Spectral
NOT_TESTED
```

This is not equivalent to:

```text
Collective = failed
Spectral = failed
```

It means:

> The experiment has not supplied the evidence needed to answer those chamber questions.

This distinction is the reason `INSUFFICIENT_DOMAIN_EVIDENCE` exists.

---

# 17. Blind Mode

The methodological sequence is:

```text
MEASURED EVIDENCE
        ↓
RUN_EXTERNAL_WINDOWS.bat
        ↓
BLIND VERDICT
        ↓
ANALYSIS LOCK
        ↓
STOP
```

At this point the chamber result is fixed.

Only then should the known identity be revealed.

The candidate bundle should contain neutral information such as:

```text
candidate_id = experiment_007
```

rather than:

```text
label = known_MBL_DTC_positive
```

The chamber ignores descriptive labels in Blind Mode, but keeping the bundle neutral is still the cleanest procedure.

---

# 18. Ground-truth file

Keep a file such as:

```text
GROUND_TRUTH_candidate_007.json
```

outside the candidate evidence ZIP.

Example:

```json
{
  "candidate_id": "candidate_007",
  "physical_class": "independently known physical classification",
  "expected_verdict": "MANY_BODY_TIME_CRYSTAL_ADMISSIBLE"
}
```

The `candidate_id` must match the blind candidate.

---

# 19. Revealing the answer

After the blind output is locked:

Double-click:

```text
REVEAL_WINDOWS.bat
```

Enter the blind output folder, for example:

```text
C:\...\TIME-CRYSTAL-I_v1_1_0\external_outputs\candidate_007
```

Then enter the ground-truth file:

```text
C:\...\GROUND_TRUTH_candidate_007.json
```

The program writes:

```text
posthoc_comparison.json
```

Read it only after the blind result exists.

---

# 20. `posthoc_comparison.json`

Typical structure:

```json
{
  "status": "POSTHOC_REVEAL_COMPLETE",
  "candidate_id": "candidate_007",
  "physical_class": "...",
  "expected_verdict": "...",
  "observed_blind_verdict": "...",
  "verdict_match": true
}
```

A mismatch is scientifically useful.

Do not modify chamber thresholds after seeing a mismatch and rerun the same candidate as if it were still blind.

A mismatch should instead become:

- a falsification result;
- a documented limitation;
- or motivation for a future chamber version tested on a new prospective corpus.

---

# 21. Included demonstration

The chamber contains:

```text
DEMO_QMB_001.zip
```

and separately:

```text
DEMO_QMB_001_GROUND_TRUTH.json
```

The demo is an end-to-end example of the blind workflow.

You can test External Analysis Mode by dragging:

```text
DEMO_QMB_001.zip
```

onto:

```text
RUN_EXTERNAL_WINDOWS.bat
```

Then inspect the blind result.

Only afterward use:

```text
REVEAL_WINDOWS.bat
```

with:

```text
DEMO_QMB_001_GROUND_TRUTH.json
```

The included validated demo should produce the Level-4 result:

```text
MANY_BODY_TIME_CRYSTAL_ADMISSIBLE
```

and the posthoc comparison should match its separately stored ground truth.

---

# 22. Chamber verdicts

## Level 0 — `NO_TEMPORAL_ORDER`

Meaning:

Temporal recurrence is not supported.

Examples in the validation corpus include thermal, chaotic and random negative controls.

---

## Level 1 — `TEMPORAL_RECURRENCE`

Meaning:

A recurrence family exists, but higher recurrence rigidity is not established.

This includes ordinary periodic systems.

It is **not** a time-crystal verdict.

---

## Level 2 — `RIGID_RECURRENCE`

Meaning:

The recurrence persists under sufficient variation, but this still does not establish a quantum many-body time crystal.

A strong classical two-cycle can reach this level.

---

## Level 3 — `COLLECTIVE_TEMPORAL_ORDER`

Meaning:

A quantum many-body candidate has:

- temporal recurrence;
- rigidity;
- collective structure;

but its many-body spectral/eigenstate breadth is not fully supported.

---

## Level 4 — `MANY_BODY_TIME_CRYSTAL_ADMISSIBLE`

Meaning:

All four required quantum many-body sectors are supported:

```text
Temporal   SUPPORTED
Rigidity   SUPPORTED
Collective SUPPORTED
Spectral   SUPPORTED
```

This is the chamber's highest admissibility verdict.

---

## Protective verdict — `INSUFFICIENT_DOMAIN_EVIDENCE`

Meaning:

A quantum candidate has progressed structurally, but evidence required for the higher chamber gates is missing.

This is not a negative physical classification.

It is a statement about the available evidence.

---

# 23. Scientific firewall

The chamber's most important methodological rules are:

1. **Do not change the frozen temporal metric for a new candidate.**
2. **Do not tune thresholds after seeing the candidate's known physical class.**
3. **Do not put ground truth inside the candidate evidence bundle.**
4. **Do not reveal the answer before `analysis_lock.json` exists.**
5. **Do not treat missing evidence as failed evidence.**
6. **Do not give classical systems an artificial zero on quantum-only coordinates.**
7. **Do not equate `q0 = 2` with time crystallinity.**

---

# 24. Frozen prospective thresholds

The External Analysis Mode thresholds are stored in:

```text
protocols\external_quantum_dtc.json
```

These are part of the v1.1.0 prospective protocol.

They should remain unchanged during a blind validation campaign.

If later research demonstrates that they need modification, that should become a new chamber version, for example:

```text
TIME-CRYSTAL-I_v1_2_0
```

and should be tested on new unseen candidates.

---

# 25. Frozen temporal dependency

The byte-identical temporal closure implementation is stored under:

```text
frozen\tc_closure.py
```

The required SHA-256 is:

```text
06344c8641aa14e6663cc3cba65d86fcdb9e37857909e85da6bc0d689e5b2553
```

If the hash changes, the prospective validation lineage is broken.

Do not edit this file.

---

# 26. Files that are primarily documentation

```text
README.md
SPEC.md
EXTERNAL_ANALYSIS.md
BLIND_PROTOCOL.md
EVIDENCE_AUDIT.md
RESULT_SUMMARY.md
CHANGELOG.md
GUIDE.md
```

Their roles are:

```text
README.md
= quick package overview

SPEC.md
= chamber scientific architecture

EXTERNAL_ANALYSIS.md
= outside evidence format

BLIND_PROTOCOL.md
= blind/reveal methodology

EVIDENCE_AUDIT.md
= meaning of evidence auditing

RESULT_SUMMARY.md
= current validation status

CHANGELOG.md
= version history

GUIDE.md
= complete operational manual
```

---

# 27. Files that should normally not be edited

For normal research use, do not edit:

```text
frozen\tc_closure.py
protocols\external_quantum_dtc.json
chamber\verdict.py
chamber\runner.py
external\analyzer.py
```

Changing these changes the scientific instrument.

If modification becomes scientifically justified, create a new version instead of silently altering `v1.1.0`.

---

# 28. Reproducing chamber validation

To revalidate the installed chamber:

```text
RUN_WINDOWS.bat
```

Then inspect:

```text
outputs\RUN_LOG.txt
outputs\validation_results.json
outputs\validation_summary.csv
```

Expected:

```text
PASS_INITIAL_VALIDATION_CORPUS
```

---

# 29. Typical prospective research workflow

For each new candidate:

```text
1. Collect experimental data.

2. Convert it into CANDIDATE_TEMPLATE format.

3. Give it a neutral candidate ID.

4. Put the known physical classification in a separate ground-truth JSON.

5. Run RUN_EXTERNAL_WINDOWS.bat.

6. Inspect EVIDENCE_AUDIT.md.

7. Record blind_verdict.json.

8. Preserve analysis_lock.json.

9. Do not change the chamber.

10. Run REVEAL_WINDOWS.bat.

11. Inspect posthoc_comparison.json.

12. Add the locked result to the prospective validation registry.
```

For multiple candidates, repeat exactly the same procedure without changing chamber thresholds between candidates.

---

# 30. Recommended storage of external runs

A clean project structure is:

```text
Time_crystal\
│
├── TIME-CRYSTAL-I_v1_1_0\
│
├── candidates\
│   ├── TC_CAND_001.zip
│   ├── TC_CAND_002.zip
│   └── TC_CAND_003.zip
│
├── ground_truth\
│   ├── GT_001.json
│   ├── GT_002.json
│   └── GT_003.json
│
└── validation_registry\
    ├── CAND_001\
    ├── CAND_002\
    └── CAND_003\
```

Never place ground truth inside the candidate bundle.

---

# 31. Troubleshooting

## `ERROR: Missing required sibling artifact`

This belongs to:

```text
RUN_WINDOWS.bat
```

It means the initial-validation dependencies are not all beside the chamber.

Check:

```text
TC_PHYS_v001
TC_CLOSURE_v001
TC_EXT_MI_v001
TC_CTRL_v001
TC_RIGIDITY_v001
TC_COLLECTIVE_v001
```

Folders or ZIPs are accepted.

---

## `NumPy is required for External Analysis Mode`

Run:

```bat
python -m pip install numpy
```

Then retry:

```text
RUN_EXTERNAL_WINDOWS.bat
```

---

## Candidate bundle path not accepted

Try dragging the ZIP directly onto:

```text
RUN_EXTERNAL_WINDOWS.bat
```

or enter the full absolute Windows path.

---

## Candidate receives `NOT_TESTED`

Read:

```text
EVIDENCE_AUDIT.md
```

This normally means required evidence was absent from the candidate bundle.

It is not necessarily a chamber failure.

---

## Candidate receives `N/A`

This normally means the sector is not applicable to the declared domain.

For example, a classical period-doubled oscillator does not receive an artificial Hilbert-space spectral score.

---

## Blind verdict differs from known physical class

Do not retune immediately.

Preserve:

```text
blind_verdict.json
analysis_lock.json
posthoc_comparison.json
```

The discrepancy is part of the research evidence.

---

# 32. Current cosmetic note

The present `RUN_WINDOWS.bat` in the v1.1.0 package still prints the completion line:

```text
TIME-CRYSTAL-I v1.0.0 validation complete.
```

This is only a console-text version-label mismatch.

The chamber data and actual package are v1.1.0, and this line does not affect calculations or verdicts.

It can be corrected in a later maintenance revision without changing scientific logic.

---

# 33. Quick-reference table

| Goal | Use |
|---|---|
| Verify chamber installation | `RUN_WINDOWS.bat` |
| Open chamber interface | `TIME-CRYSTAL-I.html` |
| Analyze a new candidate | `RUN_EXTERNAL_WINDOWS.bat` |
| Inspect missing evidence | `EVIDENCE_AUDIT.md` in the candidate output |
| Preserve blind result | `blind_verdict.json` + `analysis_lock.json` |
| Reveal known answer | `REVEAL_WINDOWS.bat` |
| Compare blind result with truth | `posthoc_comparison.json` |
| Prepare a candidate | `CANDIDATE_TEMPLATE.zip` |
| Test workflow | `DEMO_QMB_001.zip` |
| Export browser results | `Export ▾` in HTML |

---

# 34. The chamber in one workflow

```text
                    TIME-CRYSTAL-I v1.1.0

                       INSTALLATION
                            │
                            ▼
                    RUN_WINDOWS.bat
                            │
            PASS_INITIAL_VALIDATION_CORPUS
                            │
                            ▼
                    NEW EXPERIMENT
                            │
                            ▼
                 STANDARDIZE EVIDENCE
                 CANDIDATE_TEMPLATE
                            │
                            ▼
               RUN_EXTERNAL_WINDOWS.bat
                            │
                            ▼
                    EVIDENCE AUDIT
                            │
                            ▼
                     BLIND VERDICT
                            │
                            ▼
                     ANALYSIS LOCK
                            │
                     ───── STOP ─────
                            │
                    reveal only now
                            ▼
                   REVEAL_WINDOWS.bat
                            │
                            ▼
                 POSTHOC COMPARISON
                            │
                            ▼
                PROSPECTIVE VALIDATION
```

The methodological point is simple:

> `RUN_WINDOWS.bat` validates the instrument.  
> `RUN_EXTERNAL_WINDOWS.bat` uses the instrument.  
> `REVEAL_WINDOWS.bat` checks the already locked answer against reality.

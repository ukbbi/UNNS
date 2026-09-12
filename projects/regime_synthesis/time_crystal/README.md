# Time Crystal — Frozen Temporal Grammar and Prospective Validation

This directory contains the complete research record for the **UNNS Time-Crystal program**, including source data, physics reconstruction, temporal-closure development, classical controls, rigidity and collective-sector tests, the integrated **TIME-CRYSTAL-I v1.1.0** chamber, and the prospective blind-validation campaign.

The project asks a deliberately stricter question than “does the signal oscillate?”:

> **Can a frozen structural grammar distinguish supported temporal recurrence from transient, classical, control, and out-of-domain temporal order without being retuned after seeing the answer?**

The research therefore separates several layers that are often conflated:

```text
periodicity
≠
supported temporal recurrence
≠
rigid recurrence
≠
collective many-body order
≠
many-body time-crystal admissibility
```

A major outcome of the completed prospective campaign is that the frozen chamber successfully recognizes unseen integer-depth recurrence at `q0 = 2` and `q0 = 4`, rejects matched controls, and also reveals a clear domain boundary: a robust discrete time quasi-crystal does **not** satisfy the same integer-depth recurrence grammar.

## Public research reference

The associated public UNNS article is:

**[Organized or Accidental? How a Frozen Grammar Reads Time-Crystalline Recurrence](https://unns.tech/research/organized-or-accidental-how-a-frozen-grammar-reads-time-crystalline-recurrence)**

This article provides the public-facing synthesis of the frozen-grammar, blind-validation, and domain-boundary results preserved in this directory.

---

# Main research artifacts

### `Prospective_Structural_Classification_of_Discrete_Time-Crystalline_Recurrence.pdf`

Primary manuscript for the prospective structural-classification program.

### `Realization of a discrete time crystal on 57 qubits of a quantum computer.pdf`

Primary source paper retained with the project for the experimental IBM/Frey–Rachel data branch.

### `img_tc1.png` … `img_tc5.png`

Figures associated with the manuscript and public synthesis.

---

# Core project workspace

The main research corpus is stored under:

```text
time_crystal/
```

Its top-level scientific contents include:

```text
4T-DTC_upload.tar
Data.zip
DTC_Data.zip
DTC_qiskit.ipynb.zip
rawdata.xls

README_REPRODUCTION.md
TC_RESEARCH_OVERVIEW.md

TC_INGEST_v001/
TC_PHYS_v001/
TC_CLOSURE_v001/
TC_CTRL_v001/
TC_RIGIDITY_v001/
TC_COLLECTIVE_v001/
TC_EXT_MI_v001/

TIME-CRYSTAL-I_v1_1_0/
TIME-CRYSTAL-I_v1_1_0.zip

TC_PROSPECTIVE_01_research_folder/
```

The archive preserves both the development path and the final prospective-validation layer.

---

# Research architecture

The program evolved through a strict sequence:

```text
raw experimental data
    ↓
source ingestion
    ↓
independent physics reconstruction
    ↓
temporal closure
    ↓
classical/control challenge
    ↓
rigidity analysis
    ↓
collective many-body analysis
    ↓
integrated chamber
    ↓
blind external analysis
    ↓
prospective candidate campaign
```

Each stage was designed to answer a stronger question without retroactively modifying the earlier metric to fit later results.

---

# 1. Source ingestion — `TC_INGEST_v001`

The first stage verifies that the supplied experimental archive is read correctly before any UNNS quantity is introduced.

The preserved inspection report records:

```text
Status: PASS
Validated .dat files: 84 / 84
Decoded binary shape: 5 × 51 × 57 float32
epsilon values: 30, spanning 0.00 to 1.00
devices: Brooklyn 54, Manhattan 30
```

The raw data already separate a representative low-ε DTC-like run from the ε=0.5 thermal run strongly enough to validate the ingestion path.

The representative raw half-frequency-amplitude ratio is:

```text
11.73×
```

The purpose of this stage is purely:

```text
source integrity
+
format validation
+
basic physics sanity check
```

No UNNS temporal closure is calculated here.

---

# 2. Independent physics reconstruction — `TC_PHYS_v001`

Before defining a structural time-crystal metric, the project reconstructs the known physical transition from the experimental data.

The reproduction guide is:

```text
README_REPRODUCTION.md
```

The accepted result is:

```text
PASS_PHYSICS_RECONSTRUCTION
```

Key values:

```text
raw variance maximum               ε = 0.090
grid-smoothed variance peak        ε = 0.0755
segmented depolarization break     ε = 0.080
two-indicator consensus            ε = 0.07775
published reference                εc ≈ 0.075
absolute consensus difference      0.00275
```

The reconstructed DTC/thermal half-frequency response ratio is approximately:

```text
31.53
```

The package explicitly records that the raw discrete fluctuation maximum is at `ε = 0.09`, while the value near `0.075` emerges only after light grid-derived smoothing.

That qualification is retained rather than hidden.

The physics stage therefore establishes a **firewall**:

> the known physical transition must be independently reconstructed before the UNNS temporal metric is introduced.

---

# 3. Temporal closure — `TC_CLOSURE_v001`

The temporal-closure stage introduces the recurrence spectrum:

```text
C(q)
```

and searches recurrence depths:

```text
q = 1 … 10
```

without inserting `q = 2` as a target.

The first structural result independently selects:

```text
q0 = 2
```

with low-perturbation local spectral contrast:

```text
0.765595
```

Using the frozen plateau-exit rule, the recurrence-family basin leaves its low-perturbation regime at:

```text
ε = 0.070
```

The independently frozen physical reference is:

```text
εc ≈ 0.075
```

giving a grid-level difference:

```text
0.005
```

For the representative `ε = 0.05` record:

```text
observed C(q0)         = 0.681821
shuffle-null mean      = 0.284335
null 99th percentile  = 0.393027
empirical p            = 0.004975
```

The key interpretation is:

> temporal ordering matters; the closure signal is not reproduced by a shuffled-time surrogate.

This result remained exploratory until challenged by classical controls and independent data.

---

# 4. Classical and synthetic controls — `TC_CTRL_v001`

The control package is one of the most important parts of the project because it establishes what the temporal metric **cannot** claim.

The exact frozen metric was applied to:

- exact synthetic period-2 recurrence;
- logistic-map period-2;
- logistic-map period-4;
- chaotic logistic dynamics;
- IID random sequences;
- damped / transient period doubling;
- noisy recurrence.

Representative results:

### Exact synthetic 2T

```text
q0 = 2
C(2) = 1.000000
family contrast = 1.000000
shuffle p = 0.004975
```

### Classical logistic period-2, `r = 3.20`

```text
q0 = 2
C(2) = 1.000000
family contrast = 0.213201
shuffle p = 0.004975
```

### Classical logistic period-4, `r = 3.50`

```text
q0 = 4
C(q0) = 0.987293
shuffle p = 0.004975
```

### Chaotic logistic control, `r = 4.00`

```text
q0 = 8
local spectral contrast = 0.015997
family contrast = 0.019559
shuffle p = 0.393035
```

The decisive conclusion is:

> **Temporal closure is not unique to a discrete time crystal.**

A classical periodic attractor can produce strong supported recurrence.

Therefore:

```text
C(q)
```

is interpreted as a structural observable of **temporal recurrence**, not as a time-crystal order parameter by itself.

The archive also preserves a known limitation: near-exact noisy 2T signals can exhibit **harmonic ambiguity**, causing the local detector to promote a higher even recurrence depth. This was documented rather than repaired after inspection.

---

# 5. Rigidity — `TC_RIGIDITY_v001`

The rigidity stage asks whether recurrence geometry alone can separate quantum DTC order from ordinary periodic classical structure.

Its preserved verdict is:

```text
DTC_SPECIFICITY_NOT_ESTABLISHED
```

This is an important negative result.

The site-resolved MBL-DTC closure spectrum and an exact classical 2T spectrum are almost geometrically identical:

```text
cosine similarity          = 0.999988952
normalized RMS distance    = 0.005819179
```

Initial-state universality also fails as a unique discriminator:

```text
Mi MBL-DTC universality    = 0.986036
Mi prethermal              = 0.844370
classical sign-flip map    = 1.000000
```

Perturbation-basin retention is stronger for the tested DTC than for some controls:

```text
Frey MBL-DTC                       0.982069
classical exact 2T + noise         0.923071
classical exact 2T + damping       0.669981
```

but this remains quantitative rather than categorical separation.

The archive therefore records:

> **No monotone scalar reweighting of closure, family contrast, shuffle support, and initial-state universality is justified as a DTC-specific order parameter.**

This result motivates the collective / many-body sector.

---

# 6. Collective many-body sector — `TC_COLLECTIVE_v001`

The collective stage introduces genuinely many-body coordinates.

The preserved verdict is:

```text
QUANTUM_MANY_BODY_SECTOR_ESTABLISHED_WITH_CLASSICAL_SCOPE_LIMIT
```

Important results include:

### Finite-size spin-glass order

The finite-size exponent changes from non-positive to positive between:

```text
g = 0.86 and 0.88
```

near the experimentally reported MBL-DTC transition region.

### Perturbation localization

Late-time localization:

```text
MBL-DTC:
IPR   = 0.177184
N_eff = 5.644

prethermal:
IPR   = 0.065154
N_eff = 15.348
```

### Breadth over 500 bit-string states

```text
MBL-DTC mean |A|       = 0.390873
prethermal mean |A|    = 0.139797

MBL coefficient of variation        = 0.038062
prethermal coefficient of variation = 0.129036
```

### Quantum typicality / spectral breadth

At the deepest released scrambling level:

```text
MBL-DTC       mean |Aψ| = 0.396420
prethermal    mean |Aψ| = 0.183400
thermal       mean |Aψ| = 0.006117
```

giving:

```text
MBL-DTC > prethermal > thermal
```

The archive explicitly notes that some classical systems can mimic pair-order or localization individually.

The genuinely new coordinate is **quantum typicality**, which probes highly scrambled entangled states and has no directly equivalent ordinary classical periodic-attractor coordinate.

The conclusion remains domain-qualified rather than universal.

---

# 7. Independent external validation — `TC_EXT_MI_v001`

The frozen temporal metric was then applied to an independent dataset.

For the site-resolved MBL-DTC case:

```text
q0 = 2
C(q0) = 0.954047
family contrast = 0.947453
shuffle p = 0.004975
```

For the thermal control:

```text
q0 = 2
C(q0) = 0.289673
family contrast = 0.245186
shuffle p = 0.298507
```

For the MBL-DTC / prethermal comparison:

```text
MBL-DTC:
C(q0) = 0.448274
family contrast = 0.395113
shuffle p = 0.004975

prethermal:
C(q0) = 0.292554
family contrast = 0.231031
shuffle p = 0.084577
```

The important observation is again:

```text
q0 = 2
```

appears in multiple physical regimes.

The separation is carried by:

```text
closure strength
+
family contrast
+
temporal-order significance
+
cross-initial-state consistency
```

The package calls this a positive external validation of the frozen closure concept, with the explicit qualification that the dataset adapter was constructed after inspecting the public CSV layout.

---

# 8. TIME-CRYSTAL-I v1.1.0

The integrated chamber is:

```text
TIME-CRYSTAL-I_v1_1_0/
```

Its hierarchy is evidence based.

## Level 0

```text
NO_TEMPORAL_ORDER
```

No supported temporal recurrence family.

## Level 1

```text
TEMPORAL_RECURRENCE
```

A supported recurrence family exists at some detected `q0`.

## Level 2

```text
RIGID_RECURRENCE
```

The recurrence survives perturbation and/or initial-state tests.

## Level 3

```text
COLLECTIVE_TEMPORAL_ORDER
```

The recurrence is supported by collective / many-body evidence.

## Level 4

```text
MANY_BODY_TIME_CRYSTAL_ADMISSIBLE
```

Temporal, rigidity, collective, and required many-body spectral evidence are all supported.

A protective verdict is also retained:

```text
INSUFFICIENT_DOMAIN_EVIDENCE
```

for candidates that cannot legitimately be elevated because required higher-sector evidence is absent.

---

# External Analysis Mode

TIME-CRYSTAL-I v1.1.0 introduced a standardized prospective workflow:

```text
candidate evidence bundle
    ↓
Evidence Audit
    ↓
Blind verdict
    ↓
analysis lock
    ↓
manual inspection
    ↓
ground-truth reveal
    ↓
posthoc comparison
```

The chamber supports:

- standardized external evidence bundles;
- raw temporal trajectory analysis;
- recurrence-rigidity evidence;
- collective finite-size / broad-state evidence;
- spectral typicality;
- Evidence Audit;
- Blind Mode;
- cryptographic analysis locking;
- posthoc reveal;
- HTML inspection and export.

The initial standardized external demonstration produced:

```text
temporal    SUPPORTED
rigidity    SUPPORTED
collective  SUPPORTED
spectral    SUPPORTED
```

with locked verdict:

```text
MANY_BODY_TIME_CRYSTAL_ADMISSIBLE
```

for a neutral Mi MBL-DTC evidence package, matching the revealed physical class afterward.

This validates the chamber workflow on the initial validation corpus, but it is distinct from the later **prospective** campaign.

---

# 9. Prospective campaign — `TC_PROSPECTIVE_01`

The prospective campaign is the strongest methodological layer in the archive.

Its governing rule is:

> **Analyze first, lock second, reveal third, interpret fourth.**

The chamber is not told:

- the physical identity;
- the expected recurrence period;
- the expected chamber verdict;
- which sector should pass;
- which control should fail.

Candidate IDs remain neutral:

```text
TC_P01_C001
TC_P01_C002
TC_P01_C003
```

Physical ground truth is stored separately.

Canonical locked-run records include:

```text
analysis_lock.json
blind_verdict.json
evidence_audit.json
EVIDENCE_AUDIT.md
external_result.json
RUN_LOG.txt
posthoc_comparison.json
```

---

# C001 — prospective 4T recurrence

C001 tests whether the frozen temporal grammar generalizes beyond its predominantly 2T development lineage.

Blind result:

```text
q0 = 4
C(4) = 0.5482967314
F = 0.3616570847
p = 0.01492537

TEMPORAL_RECURRENCE
Level 1
```

Matched no-recompilation control:

```text
q0 = 6
F ≈ -0.003452
p ≈ 0.995025

NO_TEMPORAL_ORDER
```

After the result was locked, the candidate was revealed as a reported large-period DTC / digital quantum-computer signature.

Higher sectors remained:

```text
Rigidity     NOT_TESTED
Collective   NOT_TESTED
Spectral     NOT_TESTED
```

Therefore the candidate remains permanently classified prospectively as:

```text
TEMPORAL_RECURRENCE
```

rather than being promoted after reveal.

Principal result:

> the frozen chamber prospectively recovered **period quadrupling** without a target-period hint.

---

# C002 — prospective 2T numerical candidate

C002 uses a signed exact 14-spin numerical trajectory with a matched numerical control.

The neutral adapter performs only the documented:

```text
N = 300
```

stroboscopic reduction.

It does **not** insert alternating signs, target periods, Fourier filters, smoothing, or favorable time windows.

Candidate blind result:

```text
q0 = 2
C(2) = 0.5191138467
F = 0.5063987992
p = 0.0049751244

TEMPORAL_RECURRENCE
Level 1
```

Matched control:

```text
q0 = 6
C(6) = 0.6250288825
F = 0.0012356529
p = 0.7960199005

NO_TEMPORAL_ORDER
Level 0
```

An important structural observation is:

```text
C_control > C_candidate
```

yet the control is rejected because closure magnitude alone is not the decision rule.

After reveal, the candidate was identified as an exact prethermal-DTC simulation near `epsilon = π`, while the matched control was the corresponding `epsilon = 0` trajectory.

Again, higher sectors were not supplied and were not retroactively invented.

---

# C003 — prospective domain-boundary result

C003 deliberately tests a different kind of temporal order:

```text
discrete time quasi-crystal
```

The source contains two incommensurate drive clocks.

A direct scalar ingestion was rejected because the frozen chamber requires at least two accepted coordinates.

The project refused to:

- duplicate one signal;
- use error bars as a fake coordinate;
- invent an observable;
- modify the chamber.

Instead, a physically grounded dual-clock adapter was constructed:

```text
X_n = [Sx(nτ1), Sx(nτ2)]
```

using only measured data.

The drive-time ratio is:

```text
τ2 / τ1 = 1.618
```

Candidate blind result:

```text
q0 = 6
C(6) = 0.1987652678
F = 0.0934328447
p = 0.9601990050

NO_TEMPORAL_ORDER
Level 0
```

Matched control:

```text
q0 = 6
C(6) = 0.0946396893
F = 0.0308741990
p = 0.9950248756

NO_TEMPORAL_ORDER
Level 0
```

Only after both analyses were locked was the candidate revealed as:

```text
Experimental Z2 discrete time quasi-crystal,
robust long-interaction regime
```

and the control as a matched short-interaction regime with DTQC breakdown.

The correct conclusion is **not**:

```text
the DTQC has no temporal order
```

The correct conclusion is:

> **the frozen integer-depth temporal grammar does not recognize this robust quasi-periodic regime as supported integer-depth recurrence.**

This is the first prospective **domain-boundary result** of TIME-CRYSTAL-I.

---

# 10. Three-candidate prospective picture

The closed prospective campaign currently contains:

```text
C001 → supported q0 = 4 recurrence
C002 → supported q0 = 2 recurrence
C003 → robust quasi-periodic order outside the supported integer-depth class
```

with matched controls rejected under the same frozen procedures.

This is more informative than a sequence of only positive tests.

It establishes both:

```text
what the chamber recognizes
```

and:

```text
where its present grammar stops
```

The strongest bounded interpretation is:

> **TIME-CRYSTAL-I v1.1.0 classifies a validated class of persistent integer-depth temporal recurrence; it is not a universal detector of arbitrary temporal order.**

---

# Frozen metric and prospective discipline

The temporal metric used in the prospective campaign is cryptographically identified by:

```text
SHA-256:
06344c8641aa14e6663cc3cba65d86fcdb9e37857909e85da6bc0d689e5b2553
```

The prospective protocol is also frozen.

The project explicitly prohibits changing the closed v1.1.0 chamber to make C003 positive.

Any future quasi-periodic extension must become:

```text
a new chamber version
or
a separate temporal-closure branch
```

and must be tested on new unseen data.

Candidate C003 must remain associated with the original frozen result.

---

# Reproducibility and analysis locks

The campaign preserves cryptographic locks before ground-truth reveal.

Authoritative Windows locks include:

```text
C001
5deef733c2f71683868fa55ac71cd9f92e8118e2a8f30937119e50e65f035c16

C002
1404bdcf53eab11671376908a75861ce9a822509d2ee841914bbb200cc245e61

C002 control
7a9b544919219cea0d46ec1c640049886ee0202754457aea01bb820737297f3b

C003
2cce593284bf3416334871fae27c4bdaf54b702c3413af7233fa7182c1e0c066

C003 control
561ed97513e009cff5865761a5bf098777957eafee77cc76020d099741e4d18e
```

The archive also documents a cross-platform hashing issue:

```text
scientific reproducibility
≠
byte-for-byte serialization identity
```

Scientific quantities reproduce, but evidence hashes can differ between Windows and Linux because of serialization / line-ending differences.

The locally generated Windows locks are therefore treated as the authoritative campaign records.

A future maintenance version may canonicalize serialization, but must not alter the scientific metric.

---

# Campaign shell vs chamber

The project includes two distinct browser interfaces.

```text
TIME-CRYSTAL-I.html
```

is the scientific chamber / instrument.

```text
TC_P01.html
```

is the prospective-campaign registry and record viewer.

The campaign shell is designed not to read unrevealed ground-truth files.

A physical identity appears only after:

```text
posthoc_comparison.json
```

exists for the relevant locked run.

This separation is part of the blindness firewall.

---

# Logical directory map

```text
time_crystal/
│
├── Prospective_Structural_Classification_of_Discrete_Time-Crystalline_Recurrence.pdf
├── img_tc1.png ... img_tc5.png
│
└── time_crystal/
    ├── Data.zip
    ├── DTC_Data.zip
    ├── DTC_qiskit.ipynb.zip
    ├── 4T-DTC_upload.tar
    ├── rawdata.xls
    ├── Realization of a discrete time crystal on 57 qubits of a quantum computer.pdf
    │
    ├── README_REPRODUCTION.md
    ├── TC_RESEARCH_OVERVIEW.md
    │
    ├── TC_INGEST_v001/
    ├── TC_PHYS_v001/
    ├── TC_CLOSURE_v001/
    ├── TC_CTRL_v001/
    ├── TC_RIGIDITY_v001/
    ├── TC_COLLECTIVE_v001/
    ├── TC_EXT_MI_v001/
    │
    ├── TIME-CRYSTAL-I_v1_1_0/
    ├── TIME-CRYSTAL-I_v1_1_0.zip
    │
    └── TC_PROSPECTIVE_01_research_folder/
        ├── candidates/
        ├── ground_truth/
        ├── locked_runs/
        ├── registry/
        ├── reports/
        ├── tools/
        ├── C001_RESULTS_SUMMARY.md
        ├── C002_RESULTS_SUMMARY.md
        ├── C003_RESULTS_SUMMARY.md
        └── TC_P01_MANUAL.md
```

---

# Reproducibility flow

The intended development / validation sequence is:

```text
Data.zip
    ↓
TC_INGEST_v001
    ↓
TC_PHYS_v001
    ↓
PASS_PHYSICS_RECONSTRUCTION
    ↓
TC_CLOSURE_v001
    ↓
freeze C(q)
    ↓
TC_CTRL_v001
    ↓
establish recurrence ≠ DTC specificity
    ↓
TC_RIGIDITY_v001
    ↓
negative specificity result
    ↓
TC_COLLECTIVE_v001
    ↓
many-body sector
    ↓
TC_EXT_MI_v001
    ↓
external frozen-metric validation
    ↓
TIME-CRYSTAL-I v1.1.0
    ↓
External Analysis Mode
    ↓
TC_PROSPECTIVE_01
    ↓
C001 → C002 → C003
```

For the physics-reconstruction stage, follow:

```text
README_REPRODUCTION.md
```

For the prospective campaign, follow:

```text
TC_PROSPECTIVE_01_research_folder/TC_P01_MANUAL.md
```

---

# Prospective evidence rules

The campaign preserves several methodological rules that should remain fixed.

## Ground truth must remain separate

Physical identity belongs under:

```text
ground_truth/
```

not inside the blind candidate bundle.

## Missing evidence means `NOT_TESTED`

It does **not** mean:

```text
NOT_SUPPORTED
```

and must not be fabricated.

## A detected integer `q0` is not automatically a positive result

The verdict also requires sufficient recurrence-family contrast and null-model separation.

## No post-reveal promotion

A candidate cannot be raised to a higher chamber level using evidence discovered only after its identity is revealed.

## Controls remain independent

Candidate and control must pass through the same frozen procedure without being merged.

---

# What this research establishes

The preserved project supports the following conclusions:

1. the original experimental data can be reproduced through an independent physics-validation gate;

2. a frozen recurrence spectrum can recover the expected 2-step recurrence without inserting `q = 2`;

3. classical periodic systems can also satisfy strong temporal closure;

4. temporal recurrence therefore does not uniquely identify a time crystal;

5. recurrence rigidity by itself is also not DTC-specific;

6. genuinely many-body coordinates are required for a higher-level classification;

7. TIME-CRYSTAL-I implements this as an explicit evidence hierarchy;

8. under blind prospective testing, the frozen temporal sector recovered unseen supported `q0 = 4` and `q0 = 2` recurrence;

9. matched controls for those candidates failed the temporal-order gate;

10. a robust experimental DTQC candidate fell outside the supported integer-depth recurrence class;

11. that negative / boundary result was retained rather than tuned away.

---

# What this research does not establish

The archive does **not** establish that:

- every periodic DTC will pass the temporal sector;
- every DTQC will fail it;
- `q0` alone is a time-crystal identifier;
- large `C(q0)` alone implies admissibility;
- classical periodic order is equivalent to quantum many-body time-crystalline order;
- the full Level-4 hierarchy has been prospectively generalized across arbitrary unseen systems;
- the current chamber is a universal detector of all temporal order;
- the quasi-periodic branch should be retrofitted into v1.1.0.

The strongest claim is more precise:

> the frozen chamber identifies one empirically supported structural class — persistent integer-depth recurrence — and the prospective campaign has also found a physically meaningful temporal-order regime outside that class.

---

# Natural next research direction

The C003 result motivates a future, separate quasi-periodic branch.

Possible research coordinates mentioned in the project include:

```text
two-clock closure
vector recurrence depth
toroidal phase closure
irrational / incommensurate recurrence coordinates
multi-frequency closure families
```

These are future hypotheses, not results of the current chamber.

Any such branch should have:

- a new metric specification;
- frozen adapter rules;
- its own controls;
- a new null model;
- unseen DTQC candidates;
- explicit tests against ordinary periodic and quasi-periodic alternatives.

The closed TIME-CRYSTAL-I v1.1.0 prospective record should remain unchanged.

---

# Scope

This directory is not merely a collection of time-crystal datasets.

It is a **research record of a frozen structural grammar being developed, challenged, externally validated, and then tested prospectively**.

The key scientific progression is:

```text
known physics
    ↓
recurrence metric
    ↓
classical falsification
    ↓
rigidity limit
    ↓
many-body extension
    ↓
blind chamber
    ↓
prospective success
    ↓
prospective domain boundary
```

The central methodological lesson is that a useful classifier should reveal not only where it succeeds, but also where its own representation ceases to apply.

For the public synthesis of this research branch, see:

**[Organized or Accidental? How a Frozen Grammar Reads Time-Crystalline Recurrence](https://unns.tech/research/organized-or-accidental-how-a-frozen-grammar-reads-time-crystalline-recurrence)**


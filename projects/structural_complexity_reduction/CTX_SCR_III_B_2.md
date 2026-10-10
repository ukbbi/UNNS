# CTX_SCR_III_B_2

**Project:** Structural Complexity Reduction (SCR)  
**Transition:** SCR-III-A v002 → SCR-III-B Physical Transfer  
**Context date:** 2026-10-08  
**Purpose:** Carry the exact scientific state, canonical files, frozen decisions, and next acquisition tasks into a new conversation without losing continuity.

---

## 1. Current project position

SCR-III-A is complete and frozen.

```text
SCR-III-A v001
→ CLOSED_PRE_PRIMARY — COUPLING_NOT_INDUCED
→ retained as a historical audit-design closure

SCR-III-A v002
→ VALIDATED
→ ACCEPTANCE PREFLIGHT
→ AUDIT PASS
→ AUDIT FROZEN
→ PRIMARY COMPLETE
→ NULLS COMPLETE
→ ESTIMATORS COMPLETE
→ SUMMARY
→ COUPLING_MAP_ONLY
→ FROZEN
```

The active scientific phase is now:

```text
SCR-III-B — Physical Transfer
```

No further SCR-III-A v002 tuning, rerun, q-extension, sigma-extension, threshold change, estimator rescue, or seed replacement is authorized.

---

## 2. Frozen SCR-III-A v002 result

Final study verdict:

```text
COUPLING_MAP_ONLY
```

Frozen hypothesis/status record:

```text
H1 realized-C dose response: PASS
H3a construction anchor: PASS
H3b free-rejecting-layer prediction: PASS
H4 applicability estimators: FAIL
H5 controls: PASS
C1 exact control: PASS
TRANSFER_CONFIRMED: false
COUPLING_LAW_CANDIDATE: false
```

Primary accounting:

```text
planned main cells: 900
generated main cells: 660

accepted families:
d=14: 24/30
d=16: 21/30
d=18: 21/30
```

No primary condition reached:

```text
VALID_STRUCTURAL_REDUCTION
HIGH_RELIABILITY_REDUCTION
TRANSFER_CONFIRMED
```

All six realized-C primary panels were dose-informative and passed the preregistered within-family dose-response test.

Global descriptive result:

```text
Spearman(C, recall) ≈ 0.36715
```

Frozen interpretation:

> Realized structural coupling changes target preservation reproducibly, but the tested synthetic coupling range does not produce preservation-valid, materially reducing, net-faster SCR under the frozen exact criterion.

---

## 3. Estimator result carried forward

### E1 — family/regime estimator

```text
MAE ≈ 0.15661
Spearman ≈ 0.59911
PASS = false
```

Frozen role:

```text
negative / secondary baseline only
```

E1 is not the primary deployment estimator for SCR-III-B.

### E2 — charged instance-level estimator

```text
MAE ≈ 0.07372
Spearman ≈ 0.89962
PASS = true
```

E2 is the preferred SCR-III-B applicability estimator.

Important rule:

```text
E2 cost must be charged explicitly.
```

Do not treat E2 as free preprocessing.

The frozen interpretation is:

```text
family-transfer estimator insufficient;
local sampled estimator viable
```

---

## 4. Controls carried forward

SCR-III-A v002 controls passed.

Reference behavior:

```text
H5 = PASS
C1 = PASS
Z0 = PASS
N1 mean EI ≈ 0
N4 median EI < 0
```

Interpretation:

- N1 is effectively neutral.
- N4 has the correct anti-coupled sign.
- C1 proves problem-aligned exact pruning can preserve the target.
- Z0 confirms the no-contraction anchor.

Retain the same conceptual control discipline in SCR-III-B where physically meaningful.

---

## 5. Canonical SCR-III-A files

At the project root:

```text
structural_complexity_reduction\
│
├─ SCR_III_COUPLING_SPEC_v001.md
├─ SCR_III_STRUCTURE_v001.md
├─ SCR_III_COUPLING_SPEC_v002.md
├─ SCR_III_STRUCTURE_v002.md
├─ SCR_III_PIPELINE_GUIDE.md
├─ CTX_SCR_III_B.md
├─ CTX_SCR_III_B_2.md
│
├─ scr_iii\
└─ scr_iii_b\
```

Completed v002 result/freeze records:

```text
scr_iii\
└─ output\
   └─ v002\
      └─ reports\
         ├─ FINAL_ANALYSIS_v002.json
         ├─ SUMMARY_v002.md
         ├─ SCR_III_A_RESULT_v002.md
         └─ SCR_III_A_FREEZE_v002.json
```

The reproduction guide is:

```text
SCR_III_PIPELINE_GUIDE.md
```

It documents v001/v002 runner order, validation, acceptance preflight, audit, audit freeze, primary, nulls, estimators, summary, final freeze, status meanings, anti-tuning rules, and long-run notes.

---

## 6. SCR-III-B structure already created

New additive branch:

```text
scr_iii_b\
│
├─ README.md
├─ STRUCTURE.md
├─ MANIFEST_SHA256.txt
│
├─ references\
│  ├─ square_ice_model\
│  ├─ public_code\
│  ├─ public_data\
│  └─ papers\
│
├─ data\
│  ├─ raw\
│  ├─ derived\
│  └─ manifests\
│
├─ adapters\
├─ models\
├─ solvers\
├─ controls\
├─ estimators\
├─ analysis\
├─ scripts\
├─ tests\
├─ config\
├─ schemas\
├─ prereg\
│
├─ output\
│  ├─ acquisition\
│  ├─ validation\
│  ├─ audit\
│  ├─ primary\
│  ├─ controls\
│  ├─ estimators\
│  └─ reports\
│
└─ archive\
```

Current SCR-III-B status:

```text
PRE-SPEC / MATERIAL ACQUISITION
```

No SCR-III-B spec, preregistration, engine, seed block, Hamiltonian, patch family, energy-window rule, or preservation threshold is frozen yet.

---

## 7. Immediate active folders

Before `SCR_III_B_SPEC_v001.md` is written, use only:

```text
scr_iii_b\
├─ references\
│  ├─ square_ice_model\
│  ├─ public_code\
│  ├─ public_data\
│  └─ papers\
│
├─ data\
│  ├─ raw\
│  └─ manifests\
│
└─ output\
   └─ acquisition\
```

Do not prematurely build/freeze the physical model, solvers, preregistration, seeds, or engine.

---

## 8. First physical benchmark candidate

Current recommended first benchmark:

```text
finite square artificial spin ice / square-ice patch
```

Current validated direction:

```text
geometry: square ice only for v001
target: exact energy-window set
HP lattice protein: named backup
kagome: deferred
primary grammar: local 2-in / 2-out vertex admissibility
target solver: independent exact full-Hamiltonian solver
C1: Hamiltonian-aware exact pruning / branch-and-bound
preferred applicability estimator: E2
E1: negative/secondary baseline
```

These are still provisional until material availability and model executability are confirmed.

---

## 9. Intended square-ice separation

The intended structural separation is:

```text
G = local square-ice vertex grammar
```

versus:

```text
T(W) = { s : H_full(s) <= E0 + W }
```

The target must not be:

```text
"is this an ice-rule state?"
```

because that would be tautological.

Instead:

- G knows only local vertex geometry/admissibility.
- T comes from an independently solved full Hamiltonian.
- W is frozen before primary target solving.
- The full Hamiltonian may include competing longer-range / dipolar / J2-like terms.
- Non-ice states must remain real members of the baseline physical state space.

A finite square 16-vertex / artificial-spin-ice style model is preferable to an idealized model that removes defect states by definition.

---

## 10. Tautology guard

Mandatory rule:

If G is based on 2-in/2-out vertex admissibility, T may not simply ask whether that same rule holds.

Safer independent targets include:

```text
exact low-energy sector
energy-window state set
independently solved correlation class
transition / relaxation outcome
```

For the first benchmark, the preferred target is:

```text
exact energy-window set
```

with strict preservation:

```text
S_T^SCR = S_T^baseline
```

---

## 11. Energetic-regime refinement

A Hamiltonian-side ratio may be useful, but the spec must distinguish:

```text
guaranteed-aligned anchor
intermediate / ambiguous regime
defect-accessible / adversarial regime
```

If a rigorous energetic lower bound already guarantees that every non-ice state lies above W, then preservation is a correctness/null anchor only.

The scientific information is in the boundary region where energetic safety is not guaranteed.

At least one preregistered regime should be expected to fail.

This prevents SCR-III-B from becoming a tautological confirmation.

---

## 12. Net-gain doctrine

Do not weaken SCR criteria because small physical patches may have cheap baseline enumeration.

Separate:

```text
physical preservation transfer
```

from:

```text
valid computational SCR
```

A small-N benchmark may establish physical preservation transfer even if runtime gain is absent.

But `VALID_STRUCTURAL_REDUCTION` still requires preservation + material contraction + net gain.

Important scale note:

```text
N = 28 spins → 2^28 = 268,435,456 states
```

This is far larger than SCR-III-A depth 18.

Therefore the exact feasible size ceiling must be benchmarked, not assumed.

---

## 13. Population-V expectation

For the physical benchmark define:

```text
L = |S_G|
m = |S_T|
```

Retain the capacity requirement:

```text
L >= m
```

Do not assume Population V is automatically full.

A large V population may be an expectation in favorable regimes, but it must be measured from the frozen physical benchmark.

---

## 14. Physical structural null

Keep the physical Hamiltonian and physical geometry fixed.

Do not rewire the physical system itself.

Null only the grammar incidence relation:

```text
G_physical
vs
G_rewired_null
```

The null should preserve local degree/rule density while destroying the true geometry–grammar correspondence.

This gives a structural null on the same target T.

---

## 15. Material-availability conclusion

Current conclusion:

```text
DATA / CODE / MODEL AVAILABILITY IS NOT EXPECTED TO BE A BLOCKER
```

Public resources exist in several categories:

- published square-ice / artificial-spin-ice Hamiltonians;
- public simulation code;
- public configuration/simulation datasets;
- experimental datasets suitable for cross-checking;
- open square-artificial-spin-ice software.

However, the exact SCR target set should not be taken directly from a public dataset.

Intended workflow:

```text
published physical model / parameters
→ frozen finite patch
→ independent exact solver
→ exact target set T
```

Public data/code are for:

1. physical anchoring;
2. implementation cross-checking;
3. external validation;
4. parameter verification.

---

## 16. Immediate next task

Do not write `SCR_III_B_SPEC_v001.md` yet.

First perform:

```text
SCR-III-B MATERIAL ACQUISITION
```

Select the minimum defensible public resource set:

```text
1 authoritative physical/model reference
1 public/open implementation
1 public dataset with configurations or vertex outputs
1 parameter source sufficient for reproducible finite patches
```

For each source record:

```text
title
DOI / URL
why it is needed
exact files to download
license / attribution
expected local destination
SHA-256 after download
normative or cross-check-only status
```

Place acquired material under:

```text
scr_iii_b\references\
scr_iii_b\data\raw\
scr_iii_b\data\manifests\
scr_iii_b\output\acquisition\
```

---

## 17. Acquisition questions that must be answered

Before writing the spec, establish:

1. Can we obtain an authoritative square-ice physical Hamiltonian/model?
2. Can we reproduce its geometry and parameters locally?
3. Can we obtain at least one independent implementation for energy cross-checking?
4. Can we obtain public configurations/data for external validation?
5. Can we build an independent exact baseline solver for finite patches?
6. What patch sizes are actually feasible for exact target construction?
7. Can G be frozen without target energy or membership leakage?
8. Can a non-tautological energy-window target be defined?
9. Can we define a C1 Hamiltonian-aware pruning control?
10. Can E2 sample subtrees meaningfully in the chosen physical encoding?
11. What regimes serve as aligned anchor, ambiguous boundary, and expected-failure control?
12. What result would falsify physical transfer before the experiment is run?

---

## 18. Falsification doctrine for SCR-III-B

A physical-transfer claim should fail if, for example:

```text
preservation fails in a preregistered physically safe but non-tautological regime;
the favorable result exists only where W mathematically excludes every grammar-violating state;
E2 fails the frozen applicability criterion on held-out physical instances;
a physical structural null performs as well as the real grammar;
C1 succeeds while the structural grammar systematically destroys the target;
G requires target information to be defined.
```

These failure modes must be frozen before primary execution.

---

## 19. Files to bring into the next conversation

Minimum recommended set:

```text
CTX_SCR_III_B_2.md
CTX_SCR_III_B.md
SCR_III_A_RESULT_v002.md
SCR_III_A_FREEZE_v002.json
SCR_III_B_STRUCTURE_v001.md
SCR_III_PIPELINE_GUIDE.md
```

Useful numerical records if direct verification is needed:

```text
FINAL_ANALYSIS_v002.json
SUMMARY_v002.md
ESTIMATOR_RESULT_v002.json
NULL_RESULT_v002.json
```

For implementation/reproduction work, keep locally available:

```text
SCR_III_COUPLING_SPEC_v002.md
SCR_III_STRUCTURE_v002.md
scr_iii\SCR_III_PREREG_v002\
SCR_III_ENGINE_v002 source/package
```

Do not re-upload large frozen outputs unless directly needed.

---

## 20. Files that must remain frozen

Do not edit:

```text
SCR_III_COUPLING_SPEC_v001.md
SCR_III_STRUCTURE_v001.md
scr_iii\SCR_III_PREREG_v001\
all v001 frozen outputs

SCR_III_COUPLING_SPEC_v002.md
SCR_III_STRUCTURE_v002.md
scr_iii\SCR_III_PREREG_v002\
all v002 preflight/audit/primary/null/estimator/report outputs

SCR_III_A_RESULT_v002.md
SCR_III_A_FREEZE_v002.json
SCR_III_PIPELINE_GUIDE.md
```

SCR-III-B is additive.

---

## 21. Files not yet authorized

Do not create/freeze these until acquisition is complete:

```text
SCR_III_B_SPEC_v001.md
SCR_III_B_PREREG_v001.md
SEEDS_SCR_III_B_v001.json
SCR_III_B_ENGINE_v001
```

They belong after model/data availability, exact-solver feasibility, regime definition, and target independence are established.

---

## 22. Working scientific statement entering SCR-III-B

The strongest defensible statement carried forward is:

```text
Controlled grammar–target coupling reproducibly changes preservation,
but physical transfer remains untested.
```

SCR-III-B therefore asks:

```text
Does a real physical system naturally exhibit enough grammar–target alignment
for structural pruning to preserve its independently defined target?
```

The first candidate system is finite square artificial spin ice / square-ice patches.

The next action is **material acquisition and feasibility verification**, not coding and not preregistration.

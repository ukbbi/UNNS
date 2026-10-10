# SCR_III_B_STRUCTURE_v001

**Project:** Structural Complexity Reduction (SCR)  
**Phase:** SCR-III-B — Physical Transfer  
**Status:** `PRE_SPEC_STRUCTURE`  
**Purpose:** Establish the physical-transfer workspace before freezing `SCR_III_B_SPEC_v001`.

## 1. Scientific role

SCR-III-B is the first physical-transfer phase after SCR-III-A v002 closed at:

```text
COUPLING_MAP_ONLY
```

The immediate task is **material acquisition and benchmark validation**, not yet hypothesis freezing or primary execution.

The first candidate benchmark is finite square artificial spin ice / square-ice patches with:

- a target-blind local structural grammar based on vertex admissibility;
- an independently solved full-Hamiltonian target;
- a conventional Hamiltonian-aware C1 control;
- E2 as the preferred charged applicability estimator;
- E1 retained only as a negative/secondary baseline.

No benchmark choice, Hamiltonian, window rule, patch size, or preservation threshold is frozen by this structure file.

---

## 2. Canonical folder

Create under the existing project root:

```text
structural_complexity_reduction\
└─ scr_iii_b\
```

SCR-III-A remains frozen under `scr_iii\` and is not modified.

---

## 3. Folder structure

```text
scr_iii_b\
│
├─ README.md
├─ STRUCTURE.md
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

---

## 4. Folder purposes

### `references\`

External scientific and implementation material.

```text
references\
├─ square_ice_model\
├─ public_code\
├─ public_data\
└─ papers\
```

- `square_ice_model\` — authoritative model definitions, parameter tables, Hamiltonian notes, geometry descriptions.
- `public_code\` — external/open implementations retained for cross-checking only.
- `public_data\` — downloaded public configurations, vertex states, simulation outputs, or experimental files.
- `papers\` — PDF/reference material directly relevant to benchmark definition.

Nothing in `references\` is automatically treated as frozen ground truth. Every acquired item must be logged in `data\manifests\`.

### `data\`

```text
data\
├─ raw\
├─ derived\
└─ manifests\
```

- `raw\` — untouched acquired data.
- `derived\` — deterministic conversions, finite-patch extracts, normalized tables, and benchmark-ready inputs.
- `manifests\` — source URL/DOI, retrieval date, filename, SHA-256, license/attribution note, transformation lineage.

Raw files are never edited in place.

### `adapters\`

Converters from public or generated physical data into the SCR-III-B benchmark representation.

Examples later may include:

```text
square_ice_to_patch.py
vertex_state_adapter.py
```

No adapter is created until the external material and model conventions are fixed.

### `models\`

Physical model definitions only.

Expected later contents may include:

```text
square_ice_geometry.py
hamiltonian.py
vertex_rules.py
```

`vertex_rules.py` belongs here because it defines the candidate physical grammar object, not because it is yet frozen.

### `solvers\`

Independent target and control solvers.

Expected later separation:

```text
baseline_exact.py
c1_energy_bound.py
```

The baseline solver and C1 must remain logically distinct from the structural grammar.

### `controls\`

Physical-transfer nulls and controls.

Expected later classes:

- rate-matched random retention;
- grammar-incidence rewiring/permutation on fixed physical geometry;
- any preregistered anti-aligned or problem-aligned controls.

### `estimators\`

SCR applicability estimators.

E2 is the preferred candidate carried forward from SCR-III-A.

E1 may be retained only as a secondary/negative baseline.

### `analysis\`

Post-run metrics, preservation accounting, frontier analysis, and cross-regime comparison.

No scientific threshold belongs only in an analysis script; thresholds must ultimately be frozen in the preregistration.

### `scripts\`

Windows/Python orchestration.

Future runners should stay short and versioned, for example:

```text
RUN_ACQUIRE.bat
RUN_VALIDATE.bat
RUN_AUDIT.bat
RUN_PRIMARY.bat
```

Exact runner names are not frozen yet.

### `tests\`

Unit/integration tests for:

- geometry;
- Hamiltonian;
- grammar blindness;
- solver agreement;
- target independence;
- deterministic seeds;
- E2 sampling;
- controls;
- source/hash locks.

### `config\`

Machine-readable benchmark and run configuration after the spec is frozen.

### `schemas\`

JSON/CSV schemas for benchmark instances and outputs.

### `prereg\`

Reserved for the future frozen physical-transfer preregistration.

Do **not** create `SCR_III_B_PREREG_v001` until the benchmark/model/data acquisition phase is complete and the spec is ratified.

### `output\`

```text
output\
├─ acquisition\
├─ validation\
├─ audit\
├─ primary\
├─ controls\
├─ estimators\
└─ reports\
```

- `acquisition\` — material-availability checks, download manifests, source-validation records.
- `validation\` — model/solver cross-checks before preregistration.
- `audit\` — future preregistered audit outputs.
- `primary\` — future primary outputs.
- `controls\` — C1/null outputs.
- `estimators\` — E2/E1 results.
- `reports\` — final synthesis/result/freeze records.

### `archive\`

Superseded acquisition notes, retired candidate-model experiments, or frozen deprecated material.

Do not place active canonical files here.

---

## 5. Files created at this stage

Only two operational documents are created now:

```text
scr_iii_b\README.md
scr_iii_b\STRUCTURE.md
```

No spec, preregistration, engine, seed block, Hamiltonian, or preservation threshold is frozen yet.

---

## 6. Immediate acquisition phase

Before writing `SCR_III_B_SPEC_v001`, populate only:

```text
references\
data\raw\
data\manifests\
output\acquisition\
```

The acquisition phase must answer:

1. Can we obtain an authoritative square-ice physical model?
2. Can we obtain enough parameters to construct finite patches reproducibly?
3. Can we obtain at least one independent public implementation for cross-checking?
4. Can we obtain public configurations/data for external validation?
5. Can we build an independent exact baseline target solver for the intended small patches?
6. What patch sizes remain computationally practical for exact target construction?
7. Can the grammar be frozen without using target energies or target membership?
8. Can a non-tautological target regime be defined?

Only after these are answered should the physical spec be written.

---

## 7. Canonicality rule

`SCR_III_B_SPEC_v001.md` will eventually live at the **project root**, not inside `scr_iii_b\`, matching the SCR-III-A convention for canonical phase specifications.

Likewise, the future high-level structure/spec lineage should remain visible from:

```text
structural_complexity_reduction\
```

while implementations/data/outputs live under:

```text
scr_iii_b\
```

---

## 8. Frozen predecessor boundary

Do not modify:

```text
scr_iii\
SCR_III_COUPLING_SPEC_v001.md
SCR_III_STRUCTURE_v001.md
SCR_III_COUPLING_SPEC_v002.md
SCR_III_STRUCTURE_v002.md
SCR_III_PIPELINE_GUIDE.md
CTX_SCR_III_B.md
```

SCR-III-B is additive.

---

## 9. Next move

After this structure is installed, the next task is:

```text
SCR-III-B MATERIAL ACQUISITION
```

Specifically, identify and download the smallest defensible set of public square-ice references/code/data needed to prove that the proposed physical benchmark is materially executable.

Do not write `SCR_III_B_SPEC_v001.md` before that check is complete.

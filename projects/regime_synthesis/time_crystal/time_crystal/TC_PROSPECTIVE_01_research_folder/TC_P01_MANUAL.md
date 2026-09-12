# TC_PROSPECTIVE_01 — Extended Manual

## Purpose

`TC_PROSPECTIVE_01` is the prospective-validation campaign for `TIME-CRYSTAL-I v1.1.0`.

Its purpose is to test the chamber on **genuinely unseen candidates** without changing the chamber between candidates.

The campaign is governed by one methodological rule:

> **The chamber must reach and lock its verdict from measured evidence before the physical identity or expected answer is revealed.**

The campaign therefore separates:

1. source preservation;
2. neutral candidate construction;
3. blind chamber analysis;
4. evidence audit;
5. cryptographic locking;
6. manual inspection;
7. posthoc reveal;
8. closeout and registry entry.

---

# 1. Core campaign principle

The chamber should answer:

> **What level of temporal structural admissibility does this system actually possess?**

The answer must come from the candidate evidence alone.

The chamber must not be told:

- that the candidate is believed to be a time crystal;
- that its expected recurrence is `2T`, `4T`, or another period;
- the expected chamber verdict;
- which sector is supposed to pass;
- which control is expected to fail.

The known physical identity is stored separately and revealed only after the blind analysis lock exists.

---

# 2. Frozen instrument

The campaign uses:

`TIME-CRYSTAL-I v1.1.0`

The frozen temporal metric is:

`TC_CLOSURE_LOCK_v001`

with SHA-256:

```text
06344c8641aa14e6663cc3cba65d86fcdb9e37857909e85da6bc0d689e5b2553
```

This temporal implementation must not be edited during `TC_PROSPECTIVE_01`.

The chamber protocol, thresholds, verdict hierarchy, and sector logic must also remain unchanged during the campaign.

If later evidence demonstrates that a rule must change, the change belongs in a future chamber version and must be tested on new unseen candidates.

---

# 3. Campaign folder structure

Recommended root:

```text
Time_crystal\
│
├── TIME-CRYSTAL-I_v1_1_0\
├── TC_PROSPECTIVE_01_research_folder\
├── 4T-DTC_upload.tar
└── other source archives...
```

Inside:

```text
TC_PROSPECTIVE_01_research_folder\
│
├── candidates\
├── ground_truth\
├── locked_runs\
├── registry\
├── reports\
├── tools\
│
├── RUN_C001_WINDOWS.bat
├── README_C001.md
└── MANIFEST_C001.json
```

As the campaign grows:

```text
candidates\
├── TC_P01_C001.zip
├── TC_P01_C002.zip
└── TC_P01_C003.zip

ground_truth\
├── TC_P01_C001_GT.json
├── TC_P01_C002_GT.json
└── TC_P01_C003_GT.json

locked_runs\
├── C001\
├── C002\
└── C003\

registry\
├── TC_P01_REGISTRY.json
└── SOURCE_HASHES.json

reports\
├── C001_CLOSEOUT.md
├── C002_CLOSEOUT.md
└── ...
```

---

# 4. Candidate numbering

Use stable neutral IDs:

```text
TC_P01_C001
TC_P01_C002
TC_P01_C003
...
```

Controls should also use neutral IDs, for example:

```text
TC_P01_NRCTRL
```

Do not include physical labels such as:

```text
4T_DTC_positive
prethermal_control
thermal_negative
```

inside the blind candidate manifest.

The candidate ID should reveal nothing about the intended answer.

---

# 5. Step 1 — Preserve the original source

Before adapting anything:

1. keep the downloaded source archive unchanged;
2. record its exact file name;
3. record its byte size;
4. calculate SHA-256;
5. store the hash in the campaign registry.

For C001:

```text
Source:
4T-DTC_upload.tar
```

Recorded SHA-256:

```text
380f112980ac149a791b71f0553b776a82659da08dc60d69b242baf8c6712011
```

The original archive must never be overwritten by converted data.

---

# 6. Step 2 — Raw-format reconnaissance

Before building the candidate:

- inventory the archive;
- identify experimental data;
- identify theoretical/simulation data;
- identify mitigation variants;
- identify controls;
- identify code/notebooks;
- determine which files can be mapped into existing chamber evidence formats without changing chamber logic.

For every source file ask:

> Is this genuinely an independent measured coordinate, or is it an alternative representation / mitigation / preprocessing of another measurement?

Do not mix alternative representations as if they were independent state coordinates.

---

# 7. Step 3 — Build a neutral adapter

The adapter may:

- read raw files;
- transpose data;
- align the same cycle/time index;
- select a physically coherent set of equivalent observables;
- stack independent runs as coordinates;
- preserve provenance;
- convert to the standardized TIME-CRYSTAL-I candidate layout.

The adapter may not:

- tell the chamber the expected recurrence period;
- align signs to force a target period;
- Fourier-filter toward the expected frequency;
- smooth specifically to improve closure;
- interpolate toward a known transition;
- tune chamber thresholds;
- change `qmax`;
- alter the frozen temporal metric;
- manufacture missing collective/spectral evidence.

The adapter itself must be versioned and stored under:

```text
tools\
```

For C001:

```text
tools\build_4t_candidate.py
```

---

# 8. Step 4 — Construct the candidate evidence bundle

The standard chamber bundle is:

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

Only evidence genuinely supported by the source archive should be included.

If a sector cannot be supplied without inventing a new experiment-specific quantity, leave it absent.

Missing evidence must become:

```text
NOT_TESTED
```

not:

```text
NOT_SUPPORTED
```

---

# 9. C001 candidate construction

For C001 the primary temporal evidence consisted of eight IBM `Z_*.json` experimental trajectories.

They were stacked as:

```text
X_t = (Z_1(t), Z_2(t), ..., Z_8(t))
```

at common stroboscopic cycle `t`.

No target recurrence period was passed to the chamber.

The primary candidate bundle is:

```text
candidates\TC_P01_C001.zip
```

A separate no-recompilation ensemble was built as:

```text
candidates\TC_P01_NRCTRL.zip
```

The control was not mixed into the primary candidate.

---

# 10. Step 5 — Keep ground truth separate

The physical identity belongs outside the candidate ZIP.

For C001:

```text
ground_truth\TC_P01_C001_GT.json
```

The ground-truth record may include:

- candidate ID;
- physical class;
- reported experimental interpretation;
- expected verdict if one was genuinely preregistered.

For C001 no chamber-level expected verdict was imposed.

Therefore:

```json
"expected_verdict": null
```

This is methodologically correct.

It means the reveal can identify the physical class without retroactively pretending that a specific chamber level had been predicted.

---

# 11. Step 6 — Run Blind Mode

For C001:

```text
RUN_C001_WINDOWS.bat
```

The script:

1. rebuilds the neutral candidate from the untouched source archive;
2. rebuilds the no-recompilation control;
3. runs the candidate through `TIME-CRYSTAL-I v1.1.0 --blind`;
4. runs the control through the same frozen chamber;
5. writes locked outputs.

Canonical primary outputs:

```text
locked_runs\C001\
├── blind_verdict.json
├── analysis_lock.json
├── evidence_audit.json
├── EVIDENCE_AUDIT.md
├── external_result.json
└── RUN_LOG.txt
```

Control outputs:

```text
locked_runs\NRCTRL\
...
```

---

# 12. Step 7 — Read the blind result before reveal

Recommended order:

```text
1. RUN_LOG.txt
2. EVIDENCE_AUDIT.md
3. blind_verdict.json
4. analysis_lock.json
5. control blind_verdict.json
```

Do not open the ground-truth file yet.

The blind result should be judged on its own terms.

Questions to ask:

- What `q0` was selected?
- Is temporal closure supported?
- Is the shuffle-null result significant?
- Which higher sectors are supported?
- Which are `NOT_TESTED`?
- Did the control behave differently?
- Are there any adapter or data-quality warnings?

---

# 13. Step 8 — Preserve the analysis lock

The analysis lock is the methodological firewall.

For C001 the authoritative Windows analysis lock is:

```text
5deef733c2f71683868fa55ac71cd9f92e8118e2a8f30937119e50e65f035c16
```

Once this exists, the blind result is considered fixed.

Do not edit the candidate and rerun it as though the result were still blind.

Any later exploratory reanalysis must be explicitly marked as post-reveal research.

---

# 14. Platform-specific hash note

C001 showed that scientific quantities reproduced while serialized evidence hashes could differ between Linux-side and Windows-side generation.

The important distinction is:

```text
scientific reproducibility
≠
byte-for-byte cross-platform serialization identity
```

For the campaign, preserve the Windows lock produced by the actual local prospective run as the authoritative campaign lock.

Do not treat a cross-platform line-ending difference as a scientific discrepancy when:

- `q0`;
- closure;
- family contrast;
- shuffle p-value;
- sector status;
- final verdict

all reproduce.

A future maintenance version may canonicalize evidence serialization, but C001 must remain frozen as originally run.

---

# 15. Step 9 — Reveal only after inspection

Use the chamber's:

```text
REVEAL_WINDOWS.bat
```

Because the chamber folder and campaign folder are siblings, the correct relative paths from inside the chamber are:

```text
Blind output folder:
..\TC_PROSPECTIVE_01_research_folder\locked_runs\C001
```

and:

```text
Ground truth JSON path:
..\TC_PROSPECTIVE_01_research_folder\ground_truth\TC_P01_C001_GT.json
```

The reveal creates:

```text
locked_runs\C001\posthoc_comparison.json
```

---

# 16. Meaning of `MATCH: None`

If ground truth contains:

```json
"expected_verdict": null
```

then the reveal correctly reports:

```text
EXPECTED VERDICT: None
MATCH: None
```

This is not a failure.

It means no chamber-level expected verdict had been preregistered.

The reveal still formally records:

- candidate identity;
- locked blind verdict;
- physical class;
- analysis lock;
- ground-truth hash.

---

# 17. Step 10 — Close the candidate

After reveal, the candidate is closed at the evidence level actually tested.

Do not use newly inspected source material to retroactively promote the same candidate's blind chamber level.

For C001:

```text
Temporal     SUPPORTED
Rigidity     NOT_TESTED
Collective   NOT_TESTED
Spectral     NOT_TESTED
```

Therefore the proper blind chamber result remains:

```text
TEMPORAL_RECURRENCE
```

The fact that the physical system is reported as a large-period DTC does not authorize the chamber to fill missing sectors after the fact.

---

# 18. Closeout record

Every completed candidate should receive a closeout report containing:

- source archive;
- source SHA;
- candidate ID;
- adapter version;
- chamber version;
- frozen metric SHA;
- blind sector statuses;
- detected `q0`;
- key temporal metrics;
- final blind verdict;
- analysis-lock SHA;
- reveal status;
- revealed physical class;
- expected verdict if any;
- match if defined;
- control result;
- principal finding;
- limitations;
- status: `CLOSED`.

---

# 19. Registry update

After closeout, update:

```text
registry\TC_P01_REGISTRY.json
```

A candidate entry should contain at least:

```json
{
  "candidate": "TC_P01_C001",
  "status": "CLOSED",
  "blind_verdict": "TEMPORAL_RECURRENCE",
  "detected_q0": 4,
  "reveal_status": "POSTHOC_REVEAL_COMPLETE"
}
```

Do not rewrite old entries when new candidates are added.

The registry should become an append-only campaign history.

---

# 20. Scientific interpretation rules

## A. `q0 = 2` is not automatically a time crystal

Classical controls already demonstrated this.

## B. `q0 = 4` is not automatically a time crystal

The recurrence detector identifies temporal structure, not quantum many-body ontology.

## C. Higher chamber levels require higher-sector evidence

A candidate cannot reach Level 4 merely because its temporal recurrence matches a published DTC period.

## D. `NOT_TESTED` is not failure

It means the evidence required for the sector was not supplied.

## E. Controls matter

A candidate result is stronger when a closely related control fails under the same frozen protocol.

---

# 21. C001 blind result

Primary candidate:

```text
TC_P01_C001
```

Blind temporal result:

```text
SUPPORTED
```

Detected recurrence depth:

```text
q0 = 4
```

Closure:

```text
C(4) = 0.5482967314
```

Recurrence-family contrast:

```text
F = 0.3616570847
```

Shuffle p-value:

```text
p = 0.01492537
```

Blind chamber verdict:

```text
TEMPORAL_RECURRENCE
```

Level:

```text
1
```

---

# 22. C001 no-recompilation control

Control:

```text
TC_P01_NRCTRL
```

Automatic candidate recurrence depth:

```text
q0 = 6
```

Closure:

```text
C(q0) ≈ 0.410906
```

Family contrast:

```text
F ≈ -0.003452
```

Shuffle p-value:

```text
p ≈ 0.995025
```

Verdict:

```text
NO_TEMPORAL_ORDER
```

The control therefore did not produce a supported recurrence family.

---

# 23. C001 reveal

Posthoc reveal status:

```text
POSTHOC_REVEAL_COMPLETE
```

Physical class:

```text
Reported large-period discrete time-crystal candidate /
digital quantum-computer signature
```

Observed blind verdict:

```text
TEMPORAL_RECURRENCE
```

Expected verdict:

```text
None
```

Match:

```text
None
```

This correctly records a physical reveal without inventing a preregistered chamber-level prediction.

---

# 24. What C001 establishes

C001 establishes a prospective temporal generalization:

```text
TIME-CRYSTAL-I development lineage:
predominantly 2T systems
```

followed by an unseen candidate for which the frozen search independently returned:

```text
q0 = 4
```

The chamber was not told to search specifically for `4T`.

The matched no-recompilation control did not show supported temporal order.

Therefore the proper campaign statement is:

> **TIME-CRYSTAL-I prospectively generalized its frozen temporal recurrence machinery from period doubling to period quadrupling on C001.**

---

# 25. What C001 does not establish

C001 does not establish:

```text
MANY_BODY_TIME_CRYSTAL_ADMISSIBLE
```

because the blind candidate did not supply the chamber-standardized rigidity, collective, and spectral evidence needed for those gates.

It also does not establish that every reported `4T` candidate will be detected.

It is one prospective success and must remain one locked campaign observation.

---

# 26. What must not happen after closeout

Do not:

- reopen C001 and call a modified adapter "blind";
- modify `TIME-CRYSTAL-I v1.1.0` using C001 and rerun C001 as prospective;
- add source-specific thresholds;
- change `qmax` because a future candidate behaves differently;
- reinterpret `NOT_TESTED` as a failure;
- retrofit a non-null expected verdict into C001 ground truth;
- delete the no-recompilation control.

Post-reveal exploratory research is allowed, but it must be stored separately and labeled as posthoc.

---

# 27. Preparing C002

C002 must begin with the same frozen chamber and protocol.

Before looking at C002 outcomes:

1. assign a neutral ID;
2. preserve the raw source;
3. build the adapter without target-period information;
4. create a separate ground-truth file;
5. run Blind Mode;
6. inspect and lock;
7. reveal only afterward.

The point of the campaign is not to maximize chamber success.

The point is to discover where the chamber succeeds, where it stops because evidence is missing, and where it fails.

---

# 28. Quick operational checklist

## Before analysis

```text
[ ] raw source preserved
[ ] source SHA recorded
[ ] neutral candidate ID assigned
[ ] adapter versioned
[ ] no ground truth inside candidate
[ ] chamber unchanged
[ ] protocol unchanged
[ ] control separated
```

## Blind run

```text
[ ] candidate rebuilt from source
[ ] candidate run in --blind mode
[ ] control run through same chamber
[ ] blind_verdict.json written
[ ] analysis_lock.json written
[ ] evidence audit inspected
```

## Before reveal

```text
[ ] blind verdict recorded
[ ] q0 recorded
[ ] temporal metrics recorded
[ ] control result recorded
[ ] analysis-lock SHA recorded
[ ] no candidate modification performed
```

## Reveal

```text
[ ] correct blind output folder supplied
[ ] correct separate ground-truth JSON supplied
[ ] posthoc_comparison.json created
```

## Closeout

```text
[ ] closeout report written
[ ] registry updated
[ ] candidate status set to CLOSED
[ ] locked run preserved unchanged
```

---

# 29. Campaign workflow in one diagram

```text
RAW SOURCE
    │
    ▼
PRESERVE + HASH
    │
    ▼
RAW RECONNAISSANCE
    │
    ▼
NEUTRAL ADAPTER
    │
    ▼
CANDIDATE ZIP ──────────────── GROUND TRUTH JSON
    │                               │
    │                               │ kept separate
    ▼                               │
BLIND TIME-CRYSTAL-I RUN            │
    │                               │
    ▼                               │
EVIDENCE AUDIT                      │
    │                               │
    ▼                               │
BLIND VERDICT                       │
    │                               │
    ▼                               │
ANALYSIS LOCK                       │
    │                               │
    ├──────── STOP / INSPECT ───────┤
    │                               │
    ▼                               ▼
           POSTHOC REVEAL
                 │
                 ▼
        POSTHOC COMPARISON
                 │
                 ▼
              CLOSEOUT
                 │
                 ▼
          CAMPAIGN REGISTRY
```

---

# 30. Final operational rule

For every candidate in `TC_PROSPECTIVE_01`:

> **Analyze first, lock second, reveal third, interpret fourth.**

Never reverse that order.

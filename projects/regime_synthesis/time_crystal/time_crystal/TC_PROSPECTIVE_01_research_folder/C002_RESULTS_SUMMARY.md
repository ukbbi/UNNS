# TC_P01_C002 — Extended Results Summary and Closeout

## Candidate status

```text
CANDIDATE: TC_P01_C002
CAMPAIGN: TC_PROSPECTIVE_01
STATUS: CLOSED
```

C002 is the second formally completed prospective candidate of the `TIME-CRYSTAL-I v1.1.0` campaign.

It progressed through:

```text
source preservation
→ raw-format reconnaissance
→ signed-observable validation
→ neutral stroboscopic adapter
→ blind chamber run
→ matched control run
→ evidence audit
→ analysis lock
→ manual inspection
→ posthoc reveal
→ closeout
```

The blind candidate result and the matched-control result were both locked before their physical identities were revealed.

The blind results have not been altered after reveal.

---

# 1. Source

C002 was constructed from the signed numerical time-evolution file:

```text
time_evolution_L_14_N=300_Jt=0.07_eps=3.1416.csv
```

Recorded SHA-256:

```text
d5b4b4daa6ffa209741cfc3dc3dc9ddc30d8e23b48d5d5427be8346e2cf9f54b
```

The matched control was constructed from:

```text
time_evolution_L_14_N=300_Jt=0.07_eps=0.0000.csv
```

Recorded SHA-256:

```text
bb034defc01ea5a35c0748fb9eda477c98d0c67c8d3a9348afbc98a7047e827d
```

Both source files were preserved as the numerical source representation.

The candidate and control bundles were generated from those sources without modifying the original source files.

---

# 2. Candidate type

C002 is a:

```text
numerical quantum-many-body prospective candidate
```

It is not presented as an experimental candidate.

After posthoc reveal, its physical class was recorded as:

```text
Exact 14-spin numerical prethermal discrete-time-crystal simulation
in the N=300 slow-kick protocol near epsilon=pi
```

The matched control was revealed as:

```text
Matched exact 14-spin numerical N=300 control at epsilon=0
```

The distinction between numerical and experimental evidence is preserved throughout the campaign record.

---

# 3. Chamber

Chamber:

```text
TIME-CRYSTAL-I v1.1.0
```

Frozen temporal metric SHA-256:

```text
06344c8641aa14e6663cc3cba65d86fcdb9e37857909e85da6bc0d689e5b2553
```

Frozen prospective protocol SHA-256:

```text
2e85f96bb66f1d689e89eaa2916bb26639f608311735f450eb2822a64f92c449
```

No change was made to:

- temporal closure formula;
- `q` search range;
- recurrence-family definition;
- shuffle-null protocol;
- chamber temporal thresholds;
- chamber hierarchy;
- sector verdict logic.

C002 therefore used the same frozen scientific instrument as C001.

---

# 4. Why an additional reconnaissance stage was necessary

The first experimental files considered for C002 did not expose the signed or phase-resolved observable needed for a clean blind temporal analysis.

Their stored signals were positive processed magnitudes.

The project therefore did **not** manufacture the missing sign by imposing an alternating factor or a known period-doubling convention.

Instead, C002 reconnaissance continued until a source representation was found that stored signed:

```text
x, y, z
```

observables directly.

This prevented the known physical interpretation from being inserted into the chamber input.

---

# 5. Blind candidate construction

Neutral candidate ID:

```text
TC_P01_C002
```

The blind candidate did not contain its physical identity.

The source contains signed time evolution:

```text
index, x, y, z
```

The source protocol uses:

```text
N = 300
```

The adapter therefore performed only the documented stroboscopic reduction:

```text
(x_t, y_t, z_t)
→
(x_300n, y_300n, z_300n)
```

using exact stored source indices:

```text
0, 300, 600, ..., 300000
```

This produced:

```text
1001 stroboscopic observations
```

with signed `x`, `y`, and `z` preserved.

---

# 6. Adapter firewall

The C002 adapter did **not**:

- provide an expected recurrence period;
- tell the chamber to expect `2T`;
- multiply by an alternating sign;
- align the trajectory to a period-2 template;
- Fourier-filter toward a half-frequency peak;
- smooth the source;
- interpolate between source rows;
- select only a favorable early or late time window;
- change `qmax`;
- alter any TIME-CRYSTAL-I threshold;
- manufacture rigidity evidence;
- manufacture collective evidence;
- manufacture spectral evidence.

The adapter's role was limited to extracting the already-defined `N=300` stroboscopic sequence from the signed source trajectory.

---

# 7. Matched control construction

Neutral control ID:

```text
TC_P01_C002_CTRL
```

The matched control used the same:

- source representation;
- `x,y,z` coordinates;
- `N=300` stroboscopic reduction;
- candidate-bundle schema;
- frozen chamber;
- blind-analysis procedure.

The only physical difference came from the separate source trajectory eventually revealed as the `epsilon=0` numerical control.

This gives C002 a same-family comparison under identical chamber logic.

---

# 8. Candidate blind result

Blind mode:

```text
TRUE
```

Candidate:

```text
TC_P01_C002
```

Temporal sector:

```text
SUPPORTED
```

The frozen recurrence search independently selected:

```text
q0 = 2
```

Key quantities:

```text
C(2) = 0.5191138467
F    = 0.5063987992
p    = 0.0049751244
```

where:

- `C(2)` is frozen temporal closure at the detected recurrence depth;
- `F` is recurrence-family contrast;
- `p` is the frozen shuffle-null empirical p-value.

Final blind chamber verdict:

```text
TEMPORAL_RECURRENCE
```

Level:

```text
1
```

---

# 9. Candidate evidence hash and authoritative analysis lock

Candidate evidence SHA-256:

```text
de6eb7da4f237d231bdab68f9ebe36c811b35c60c6d11ed3ea8f93228c751293
```

The authoritative locally reproduced Windows C002 analysis lock is:

```text
1404bdcf53eab11671376908a75861ce9a822509d2ee841914bbb200cc245e61
```

This lock existed before the C002 physical identity was revealed.

It therefore fixes:

```text
candidate ID
evidence hash
frozen metric hash
protocol hash
blind verdict
blind level
```

before posthoc interpretation.

---

# 10. Why the candidate verdict stopped at Level 1

C002 supplied strong temporal evidence but did not supply the standardized higher-sector files required by the chamber.

Blind sector status:

```text
Temporal     SUPPORTED
Rigidity     NOT_TESTED
Collective   NOT_TESTED
Spectral     NOT_TESTED
```

Missing rigidity evidence:

```text
rigidity/initial_state_trajectories.csv
rigidity/perturbation_scan.csv
```

Missing collective evidence:

```text
collective/size_scaling.csv
collective/initial_state_order.csv
```

Missing spectral evidence:

```text
spectral/typicality.csv
```

The chamber therefore stopped at:

```text
TEMPORAL_RECURRENCE
```

rather than using the eventual physical label to promote the candidate.

This preserves the same evidence discipline demonstrated by C001.

---

# 11. Matched-control blind result

Control ID:

```text
TC_P01_C002_CTRL
```

The automatic recurrence-depth selector returned:

```text
q0 = 6
```

with:

```text
C(6) = 0.6250288825
F    = 0.0012356529
p    = 0.7960199005
```

Control temporal status:

```text
NOT_SUPPORTED
```

Control verdict:

```text
NO_TEMPORAL_ORDER
```

Level:

```text
0
```

The control therefore did not satisfy the frozen temporal-order gate.

---

# 12. Why the control result is important

The control demonstrates again that:

```text
automatic q0 candidate
```

is not equivalent to:

```text
supported temporal recurrence
```

The primary C002 candidate showed:

```text
q0 = 2
F ≈ 0.506399
p ≈ 0.004975
SUPPORTED
```

whereas the matched control showed:

```text
q0 = 6
F ≈ 0.001236
p ≈ 0.796020
NOT_SUPPORTED
```

Thus the chamber did not classify the control as temporally ordered merely because the recurrence-depth routine selected an integer.

The recurrence-family contrast and shuffle-null evidence remained decisive.

---

# 13. Control evidence hash and analysis lock

Control evidence SHA-256:

```text
9a98654fddb799cc979850a29391d2cf462e41a03267e3e84c3a0633a0a773d4
```

Authoritative locally reproduced control analysis lock:

```text
7a9b544919219cea0d46ec1c640049886ee0202754457aea01bb820737297f3b
```

The control was therefore independently locked before its physical identity was revealed.

---

# 14. Candidate posthoc reveal

Candidate reveal status:

```text
POSTHOC_REVEAL_COMPLETE
```

Revealed physical class:

```text
Exact 14-spin numerical prethermal discrete-time-crystal simulation
in the N=300 slow-kick protocol near epsilon=pi
```

Previously locked blind verdict:

```text
TEMPORAL_RECURRENCE
```

Ground-truth file did not contain a preregistered chamber-level expected verdict:

```text
expected_verdict = null
```

Therefore:

```text
verdict_match = null
```

This is correct.

The reveal records the physical identity without retroactively imposing a chamber-level prediction.

---

# 15. Candidate ground-truth hash

The posthoc reveal records candidate ground-truth SHA-256:

```text
0ec4780346cfcb0876b038390202a2363840572584ecfa99625635856fffc6c4
```

The reveal is explicitly tied to the previously locked analysis:

```text
1404bdcf53eab11671376908a75861ce9a822509d2ee841914bbb200cc245e61
```

---

# 16. Matched-control posthoc reveal

Control reveal status:

```text
POSTHOC_REVEAL_COMPLETE
```

Revealed physical class:

```text
Matched exact 14-spin numerical N=300 control at epsilon=0
```

Previously locked blind verdict:

```text
NO_TEMPORAL_ORDER
```

Again:

```text
expected_verdict = null
verdict_match = null
```

because no chamber-level expected verdict was preregistered.

---

# 17. Control ground-truth hash

The control reveal records ground-truth SHA-256:

```text
6084767d9532c03903ee3eb8d57c4ec7cbee5c510c214e51cc72d13391a21a88
```

The reveal is tied to the previously locked control analysis:

```text
7a9b544919219cea0d46ec1c640049886ee0202754457aea01bb820737297f3b
```

---

# 18. Principal prospective finding

The primary C002 result is:

> **A neutral numerical quantum-many-body candidate caused the unchanged TIME-CRYSTAL-I temporal machinery to recover `q0 = 2` with strong recurrence-family contrast and shuffle significance, while its matched numerical control failed the temporal-order gate.**

Formally:

```text
TC_P01_C002
q0 = 2
C(2) = 0.5191138467
F = 0.5063987992
p = 0.0049751244
→ TEMPORAL_RECURRENCE
```

versus:

```text
TC_P01_C002_CTRL
q0 = 6
C(6) = 0.6250288825
F = 0.0012356529
p = 0.7960199005
→ NO_TEMPORAL_ORDER
```

---

# 19. Relationship to C001

C001 and C002 now give two different prospective demonstrations of the frozen temporal layer.

C001:

```text
reported large-period experimental candidate
→ q0 = 4
→ TEMPORAL_RECURRENCE
```

C002:

```text
numerical prethermal-DTC candidate
→ q0 = 2
→ TEMPORAL_RECURRENCE
```

Both matched controls failed temporal order:

```text
C001 control
→ NO_TEMPORAL_ORDER

C002 control
→ NO_TEMPORAL_ORDER
```

The chamber was not modified between C001 and C002.

---

# 20. Structural significance

C002 strengthens the interpretation that the chamber temporal sector is not merely detecting a nominal oscillation period.

Its positive decision requires a recurrence family with sufficient contrast against nearby recurrence depths and sufficient separation from a shuffle-null ensemble.

This is visible in the candidate/control contrast:

```text
candidate:
F ≈ 0.506399
p ≈ 0.004975

control:
F ≈ 0.001236
p ≈ 0.796020
```

The control even has a larger raw closure value at its automatically selected `q0`:

```text
C_control ≈ 0.625029
```

than the candidate:

```text
C_candidate ≈ 0.519114
```

yet the chamber correctly rejects the control because closure magnitude alone is not the verdict rule.

That is an especially useful C002 result.

---

# 21. What C002 establishes

C002 establishes that, for this numerical candidate/control pair:

1. the neutral signed trajectory can be mapped into the frozen temporal protocol without target-period input;
2. the chamber independently recovers `q0 = 2` for the candidate;
3. the candidate recurrence family is strongly contrasted;
4. the candidate passes the shuffle-null temporal gate;
5. the matched control does not;
6. the final blind classifications are separated before physical identity is revealed.

The correct prospective statement is:

> **TIME-CRYSTAL-I prospectively recovered supported period-doubled temporal recurrence in C002 while rejecting the matched epsilon=0 numerical control.**

---

# 22. What C002 does not establish

C002 does **not** establish:

```text
MANY_BODY_TIME_CRYSTAL_ADMISSIBLE
```

because:

```text
Rigidity     NOT_TESTED
Collective   NOT_TESTED
Spectral     NOT_TESTED
```

It does not prospectively validate the full four-sector chamber hierarchy.

It also does not prove that:

- every prethermal DTC will pass;
- every non-DTC numerical control will fail;
- every period-doubled quantum system is a time crystal;
- the higher chamber sectors generalize from the Mi validation corpus to this simulation;
- the current thresholds are optimal.

Those remain campaign questions for later candidates.

---

# 23. Why no post-reveal promotion is allowed

After C002 was revealed as a numerical prethermal-DTC simulation, the campaign did not use that identity to elevate its chamber level.

The prospective result remains:

```text
TEMPORAL_RECURRENCE
```

Any future extraction of rigidity, collective, or spectral information from the same source family would be:

```text
POSTHOC / EXPLORATORY
```

unless a new prospective protocol is defined before examining those outcomes.

The original C002 blind result must remain untouched.

---

# 24. Methodological success

C002 validates the campaign procedure on a second, materially different candidate:

```text
preserve source
→ reject inadequate representation
→ identify signed source representation
→ freeze neutral adapter
→ blind candidate run
→ blind matched-control run
→ evidence audit
→ cryptographic locks
→ manual inspection
→ reveal candidate
→ reveal control
→ closeout
```

Importantly, the campaign did **not** weaken the blind protocol merely to force the original processed experimental files into the chamber.

Instead, the representation problem was identified and resolved explicitly before C002 was frozen.

---

# 25. Canonical C002 files to preserve

The primary prospective record is:

```text
locked_runs\C002\
├── analysis_lock.json
├── blind_verdict.json
├── evidence_audit.json
├── EVIDENCE_AUDIT.md
├── external_result.json
├── posthoc_comparison.json
└── RUN_LOG.txt
```

The matched-control record is:

```text
locked_runs\C002_CTRL\
├── analysis_lock.json
├── blind_verdict.json
├── evidence_audit.json
├── EVIDENCE_AUDIT.md
├── external_result.json
├── posthoc_comparison.json
└── RUN_LOG.txt
```

Together these fourteen files define the closed C002 candidate/control pair.

Do not overwrite them.

---

# 26. Recommended campaign registry entry

The campaign registry should now record:

```text
Candidate:
TC_P01_C002

Status:
CLOSED

Candidate type:
Numerical quantum-many-body

Physical class:
Exact 14-spin numerical prethermal discrete-time-crystal simulation
in the N=300 slow-kick protocol near epsilon=pi

Blind temporal sector:
SUPPORTED

Detected q0:
2

Closure:
0.5191138467

Family contrast:
0.5063987992

Shuffle p:
0.0049751244

Blind verdict:
TEMPORAL_RECURRENCE

Blind level:
1

Rigidity:
NOT_TESTED

Collective:
NOT_TESTED

Spectral:
NOT_TESTED

Candidate analysis lock:
1404bdcf53eab11671376908a75861ce9a822509d2ee841914bbb200cc245e61

Matched control:
TC_P01_C002_CTRL

Control physical class:
Matched exact 14-spin numerical N=300 control at epsilon=0

Control temporal sector:
NOT_SUPPORTED

Control q0:
6

Control family contrast:
0.0012356529

Control shuffle p:
0.7960199005

Control verdict:
NO_TEMPORAL_ORDER

Control analysis lock:
7a9b544919219cea0d46ec1c640049886ee0202754457aea01bb820737297f3b

Posthoc reveal:
COMPLETE for candidate and control

Expected chamber verdict:
NONE

Verdict match:
N/A

Principal finding:
Frozen temporal machinery recovered supported q0=2 recurrence in the
prethermal-DTC numerical candidate while rejecting the matched epsilon=0 control.
```

---

# 27. Campaign state after C002

The prospective campaign now contains two closed candidates:

```text
C001
→ q0 = 4
→ TEMPORAL_RECURRENCE
→ matched control: NO_TEMPORAL_ORDER
→ CLOSED

C002
→ q0 = 2
→ TEMPORAL_RECURRENCE
→ matched control: NO_TEMPORAL_ORDER
→ CLOSED
```

This gives the campaign:

```text
2 closed candidates
2 matched controls
4 locked records
0 unrevealed candidate records
```

after the C002 candidate and control reveals are complete.

---

# 28. Scientific significance

C002 adds a different kind of evidence to C001.

C001 primarily demonstrated:

```text
recurrence-depth generalization beyond 2T
```

through prospective recovery of:

```text
q0 = 4
```

C002 demonstrates:

```text
candidate/control specificity within a signed numerical prethermal setting
```

through the contrast:

```text
candidate:
SUPPORTED q0=2 recurrence

matched control:
NO_TEMPORAL_ORDER
```

The two results therefore probe different aspects of the frozen temporal machinery.

---

# 29. Limitations

C002 remains one numerical candidate/control pair.

The candidate has not tested prospective rigidity, collective, or spectral gates.

The campaign therefore still needs future candidates designed to ask whether:

- recurrence rigidity generalizes prospectively;
- collective order can be independently ingested;
- spectral/typicality evidence can be supplied without chamber-specific tuning;
- strong non-time-crystalline periodic quantum systems can reach or confuse higher levels;
- the full Level-4 verdict survives prospective testing.

C002 does not answer those questions.

---

# 30. C002 closeout verdict

The complete C002 result is:

```text
PROSPECTIVE CANDIDATE:
TC_P01_C002

CANDIDATE TYPE:
Numerical quantum-many-body

BLIND TEMPORAL ORDER:
SUPPORTED

DETECTED RECURRENCE:
q0 = 2

CLOSURE:
0.5191138467

FAMILY CONTRAST:
0.5063987992

SHUFFLE P:
0.0049751244

BLIND CHAMBER VERDICT:
TEMPORAL_RECURRENCE

MATCHED CONTROL:
TC_P01_C002_CTRL

CONTROL TEMPORAL ORDER:
NOT_SUPPORTED

CONTROL VERDICT:
NO_TEMPORAL_ORDER

POSTHOC PHYSICAL CLASS:
Exact 14-spin numerical prethermal discrete-time-crystal simulation
in the N=300 slow-kick protocol near epsilon=pi

CONTROL PHYSICAL CLASS:
Matched exact 14-spin numerical N=300 control at epsilon=0

HIGHER-SECTOR STATUS:
NOT TESTED

CANDIDATE STATUS:
CLOSED

CONTROL STATUS:
CLOSED
```

---

# 31. Final conclusion

The second prospective campaign candidate produced a clean candidate/control separation under the unchanged `TIME-CRYSTAL-I v1.1.0` temporal machinery.

The chamber independently recovered:

```text
q0 = 2
```

for the neutral C002 candidate, with substantial recurrence-family contrast and strong shuffle-null separation.

The matched control did not satisfy temporal order despite having a sizable raw closure value at its automatically selected recurrence depth.

After the results were locked, the candidate was revealed as an exact 14-spin numerical prethermal discrete-time-crystal simulation near `epsilon=pi`, while the matched control was revealed as the corresponding `epsilon=0` numerical control.

The correct bounded conclusion is:

> **C002 is a second prospective success of the TIME-CRYSTAL-I temporal sector: supported period-doubled recurrence was recovered blindly in the prethermal-DTC numerical candidate, while the matched numerical control was rejected.**

C002 should now remain closed and untouched while `TC_PROSPECTIVE_01` proceeds to the next genuinely unseen candidate.

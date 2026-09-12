# TC_P01_C001 — Extended Results Summary and Closeout

## Candidate status

```text
CANDIDATE: TC_P01_C001
CAMPAIGN: TC_PROSPECTIVE_01
STATUS: CLOSED
```

C001 is the first formally completed prospective candidate of the `TIME-CRYSTAL-I v1.1.0` campaign.

It progressed through:

```text
raw source preservation
→ neutral adapter
→ blind chamber run
→ independent control run
→ evidence audit
→ analysis lock
→ manual inspection
→ posthoc reveal
→ closeout
```

The blind result has not been altered after reveal.

---

# 1. Source

Source archive:

```text
4T-DTC_upload.tar
```

Recorded SHA-256:

```text
380f112980ac149a791b71f0553b776a82659da08dc60d69b242baf8c6712011
```

The archive was preserved as the original source.

The prospective candidate was generated from selected experimental IBM trajectories without modifying the source archive.

---

# 2. Chamber

Chamber:

```text
TIME-CRYSTAL-I v1.1.0
```

Frozen temporal metric SHA-256:

```text
06344c8641aa14e6663cc3cba65d86fcdb9e37857909e85da6bc0d689e5b2553
```

No change was made to:

- temporal closure formula;
- `q` search range;
- recurrence-family definition;
- shuffle-null protocol;
- chamber hierarchy;
- sector verdict logic.

---

# 3. Blind candidate construction

Neutral candidate ID:

```text
TC_P01_C001
```

The chamber was not given the reported physical identity.

The primary temporal state was constructed from eight experimental IBM `Z_*.json` trajectories as:

```text
X_t = (Z_1(t), Z_2(t), ..., Z_8(t))
```

at common stroboscopic cycle `t`.

The adapter did not:

- sign-align to a four-cycle template;
- Fourier-filter toward period 4;
- smooth toward a desired answer;
- provide `4T` as a target period;
- change `qmax`;
- mix mitigation variants into the primary state vector.

---

# 4. Independent control

A separate no-recompilation bundle was created:

```text
TC_P01_NRCTRL
```

It was passed through the same frozen chamber.

The control was not mixed into the primary candidate.

This provides an internal prospective comparison between:

```text
primary reported large-period experimental ensemble
```

and:

```text
no-recompilation hardware/control ensemble
```

under identical chamber logic.

---

# 5. Primary blind result

Blind mode:

```text
TRUE
```

Candidate:

```text
TC_P01_C001
```

Temporal sector:

```text
SUPPORTED
```

The frozen recurrence search independently selected:

```text
q0 = 4
```

Key quantities:

```text
C(4) = 0.5482967314
F     = 0.3616570847
p     = 0.01492537
```

where:

- `C(4)` is frozen temporal closure at the detected recurrence depth;
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

# 6. Why the verdict stopped at Level 1

The candidate supplied strong temporal evidence but not the full standardized higher-sector evidence required by `TIME-CRYSTAL-I`.

Blind sector status:

```text
Temporal     SUPPORTED
Rigidity     NOT_TESTED
Collective   NOT_TESTED
Spectral     NOT_TESTED
```

The chamber therefore correctly stopped at:

```text
TEMPORAL_RECURRENCE
```

It did not infer higher sectors from the candidate's eventual physical identity.

This is an important success of the chamber's evidence discipline.

---

# 7. No-recompilation control result

Control ID:

```text
TC_P01_NRCTRL
```

The automatic recurrence-depth selector returned:

```text
q0 = 6
```

but the recurrence family did not survive the chamber's temporal-order criteria.

Approximate control quantities:

```text
C(q0) ≈ 0.410906
F     ≈ -0.003452
p     ≈ 0.995025
```

Control temporal status:

```text
NOT_SUPPORTED
```

Control verdict:

```text
NO_TEMPORAL_ORDER
```

This is important because it demonstrates that the integer returned by the `q0` detector alone is not treated as evidence of temporal order.

The primary candidate showed:

```text
q0 = 4
F > 0
p << 1
SUPPORTED
```

whereas the no-recompilation control showed:

```text
q0 = 6
F ≈ 0
p ≈ 1
NOT_SUPPORTED
```

---

# 8. Authoritative Windows analysis lock

The locally reproduced Windows blind run generated the authoritative C001 campaign lock:

```text
5deef733c2f71683868fa55ac71cd9f92e8118e2a8f30937119e50e65f035c16
```

This lock existed before ground truth was revealed.

Therefore the later physical reveal could not alter the blind chamber result.

---

# 9. Evidence hash

Windows blind evidence SHA-256:

```text
19b1653412e99bbac0513e38ae35c6299b72c0f81872117431be1799dc57cf77
```

A prior Linux-side build produced the same scientific result but a different serialized evidence hash.

The scientific outputs agreed:

- `q0`;
- closure;
- family contrast;
- shuffle p-value;
- sector status;
- final verdict.

The hash difference is therefore treated as a cross-platform serialization/provenance issue rather than a scientific mismatch.

For C001, the Windows lock above is the authoritative campaign lock.

---

# 10. Posthoc reveal

Reveal status:

```text
POSTHOC_REVEAL_COMPLETE
```

Revealed physical class:

```text
Reported large-period discrete time-crystal candidate /
digital quantum-computer signature
```

Observed locked blind verdict:

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

It means the campaign did not retroactively claim that Level 1, Level 4, or any other chamber level had been predicted in advance.

---

# 11. Ground-truth hash

The reveal record preserved the ground-truth SHA-256:

```text
b4fed127327e6754968ba811f991bbab2057549991c67deeacb3863f0397d2da
```

The revealed identity is therefore part of the permanent closeout provenance.

---

# 12. Principal prospective finding

The most important result of C001 is:

> **An unseen large-period candidate caused the frozen TIME-CRYSTAL-I temporal machinery to recover `q0 = 4` without target-period input.**

The chamber had been developed primarily around `2T` systems.

Nevertheless, on C001 the unchanged search:

```text
q = 1,...,10
```

selected:

```text
q0 = 4
```

from the experimental ensemble.

This is the first genuine prospective demonstration that the temporal recurrence machinery is not limited to period doubling.

---

# 13. Stronger formulation

The prospective observation can be summarized as:

```text
development lineage:
mostly 2T
```

followed by:

```text
unseen candidate:
q0 = 4
```

with:

```text
C(4) = 0.5482967314
F = 0.3616570847
p = 0.01492537
```

and:

```text
matched no-recompilation control:
NO_TEMPORAL_ORDER
```

Therefore:

> **TIME-CRYSTAL-I prospectively generalized its frozen temporal-closure machinery from period doubling to period quadrupling on C001.**

---

# 14. What the result means structurally

C001 supports the interpretation:

```text
C(q)
```

is a recurrence-depth-sensitive temporal structural observable rather than a hard-coded detector of period 2.

Earlier classical controls had already shown that:

```text
q0 = 2
```

does not uniquely identify a time crystal.

C001 now adds the complementary result:

```text
q0 = 4
```

can emerge prospectively when the candidate carries a coherent period-4 recurrence structure.

This strengthens the interpretation of the temporal layer as a general recurrence-structure sector.

---

# 15. What the result does not mean

C001 does **not** establish:

```text
MANY_BODY_TIME_CRYSTAL_ADMISSIBLE
```

because:

```text
Rigidity   NOT_TESTED
Collective NOT_TESTED
Spectral   NOT_TESTED
```

The public archive contains additional material, but that material was not retrospectively converted into new chamber-standardized sectors after reveal.

That restraint is methodologically important.

---

# 16. Why no post-reveal promotion is allowed

After physical identity is revealed, additional source interpretation is no longer blind.

Therefore C001 must remain:

```text
TEMPORAL_RECURRENCE
```

for the prospective campaign.

Any future attempt to extract rigidity, collective, or spectral evidence from the same source archive must be labeled:

```text
POSTHOC / EXPLORATORY
```

and must not replace the original locked C001 result.

---

# 17. Why the control matters

Without the no-recompilation control, one possible concern would be:

> Does the chamber merely find some recurrence depth in every short IBM trajectory ensemble?

The control argues against that interpretation.

Although the automatic `q0` routine returned a candidate integer for the control, its recurrence-family contrast was essentially zero and its temporal ordering was fully compatible with shuffle:

```text
p ≈ 0.995
```

The chamber therefore rejected it.

This demonstrates that:

```text
q0 candidate
```

and:

```text
SUPPORTED temporal recurrence
```

are distinct chamber concepts.

---

# 18. Methodological success

C001 validates the complete prospective sequence:

```text
source preservation
→ neutral adapter
→ blind candidate
→ frozen chamber
→ independent control
→ evidence audit
→ cryptographic lock
→ posthoc reveal
```

The sequence worked operationally on Windows.

The only discovered infrastructure weakness was cross-platform evidence-hash canonicalization, which did not alter scientific outputs.

---

# 19. Current C001 archive that must be preserved

The canonical closeout record should preserve:

```text
locked_runs\C001\
├── analysis_lock.json
├── blind_verdict.json
├── evidence_audit.json
├── EVIDENCE_AUDIT.md
├── external_result.json
├── posthoc_comparison.json
└── RUN_LOG.txt
```

Together these seven files define the prospective record.

Do not overwrite them.

---

# 20. Recommended registry entry

The campaign registry should now state:

```text
Candidate:
TC_P01_C001

Status:
CLOSED

Physical class:
Reported large-period discrete time-crystal candidate /
digital quantum-computer signature

Blind temporal sector:
SUPPORTED

Detected q0:
4

Closure:
0.5482967314

Family contrast:
0.3616570847

Shuffle p:
0.01492537

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

Control:
TC_P01_NRCTRL

Control verdict:
NO_TEMPORAL_ORDER

Posthoc reveal:
COMPLETE

Expected chamber verdict:
NONE

Verdict match:
N/A

Principal finding:
Frozen temporal machinery prospectively recovered 4T recurrence.

Analysis lock:
5deef733c2f71683868fa55ac71cd9f92e8118e2a8f30937119e50e65f035c16
```

---

# 21. Scientific significance

C001 is important for three reasons.

## 21.1 Recurrence-depth generalization

The chamber moved beyond its predominantly `2T` development lineage and recovered:

```text
q0 = 4
```

without a target-period hint.

## 21.2 Control separation

The matched no-recompilation set did not pass temporal order.

## 21.3 Evidence discipline

The chamber did not allow the revealed physical identity to elevate the candidate beyond the actually supplied evidence.

That combination is stronger than simply reproducing a known `4T` oscillation.

---

# 22. Limitations

C001 remains one candidate.

It does not prove that:

- all `4T` DTCs will be recovered;
- all prethermal `4T` mimics will be rejected;
- the chamber can distinguish every large-period periodic attractor;
- the full four-sector hierarchy generalizes prospectively;
- the present prospective thresholds are optimal.

Those questions belong to later candidates.

---

# 23. Campaign implication

The proper next question is no longer:

> Can TIME-CRYSTAL-I detect period 4?

C001 has given a positive prospective answer at the temporal level.

The next question becomes:

> How does the same frozen chamber behave on a difficult DTC-like / prethermal candidate?

That motivates:

```text
TC_P01_C002
```

without changing `TIME-CRYSTAL-I v1.1.0`.

---

# 24. C001 closeout verdict

The complete C001 result is:

```text
PROSPECTIVE CANDIDATE:
TC_P01_C001

BLIND TEMPORAL ORDER:
SUPPORTED

DETECTED RECURRENCE:
q0 = 4

BLIND CHAMBER VERDICT:
TEMPORAL_RECURRENCE

MATCHED CONTROL:
NO_TEMPORAL_ORDER

POSTHOC PHYSICAL CLASS:
Reported large-period discrete time-crystal candidate /
digital quantum-computer signature

HIGHER-SECTOR STATUS:
NOT TESTED

CANDIDATE STATUS:
CLOSED
```

---

# 25. Final conclusion

The first prospective campaign candidate produced the result the project most needed to see:

> **TIME-CRYSTAL-I did not merely replay its period-doubling development history. On an unseen large-period experimental candidate, its frozen temporal layer independently recovered period quadrupling.**

The result is bounded correctly:

- it is a real prospective success of the temporal layer;
- it is not yet a full Level-4 time-crystal admissibility result;
- it is strengthened by the failure of the no-recompilation control;
- it remains locked exactly as obtained before reveal.

C001 should now remain closed and untouched while the campaign proceeds to C002.

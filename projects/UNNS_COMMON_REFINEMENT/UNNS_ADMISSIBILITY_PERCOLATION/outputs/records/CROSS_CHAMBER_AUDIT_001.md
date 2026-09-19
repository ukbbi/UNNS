# Cross-Chamber Audit 001

## Status

**STRUC-PERC-I BATCH COMPLETE — FINAL SYNTHESIS PAUSED FOR AUDIT**

The raw STRUC-PERC-I batch output is retained unchanged.

The batch produced:

```text
FULL_PERCOLATION      25
HARD_FRAGMENTATION     4
TAIL_FRAGMENTATION     1
```

The non-full cases are:

```text
AFF01  HARD_FRAGMENTATION
AFF04  HARD_FRAGMENTATION
AFN01  TAIL_FRAGMENTATION
AFN06  HARD_FRAGMENTATION
INT03  HARD_FRAGMENTATION
```

All 30 batch evaluations report `COMPLETE`.

Because STRUC-I had already classified all 30 frozen ladders as fully admissible
(`mean_Ak = min_Ak = 1.0`), the preregistered protocol requires these non-full
percolation verdicts to be audited before any cross-chamber scientific conclusion.

## 1. What was audited

The audit does **not** alter STRUC-PERC-I.

It reproduces the chamber's full-pairwise graph model on the frozen inputs:

```text
vertices = gap values Delta_i

edge(i,j) exists when:
abs(Delta_i - Delta_j) <= epsilon

epsilon = kappa * scale
```

where the chamber scale is:

```text
IQR(Delta) when IQR > 0
otherwise median(Delta)
```

For a one-dimensional threshold graph on gap values, exact full connectivity occurs when
`epsilon` reaches the largest adjacent separation in the **sorted gap-value list**.

Therefore the minimal graph-connectivity scale can be computed deterministically as:

```text
kappa_connect_exact
=
max adjacent separation in sorted gaps
/
epsilon scale
```

This is not a replacement chamber. It is an exact audit of the chamber's own operative graph model.

The audit script reproduces the batch verdicts for **30 / 30 cases**.

## 2. Adaptive-extension plateau issue

Four of the five non-full batch cases have ordinary finite connectivity thresholds that lie
beyond the point where the adaptive extension stops on a plateau.

### AFF01

Batch:

```text
HARD_FRAGMENTATION
giant ratio at base maximum = 0.669291
```

Audit:

```text
exact graph kappa_connect = 9.898979
adaptive plateau          = 2.000000
```

The chamber stops at the plateau before testing the later scale at which the graph would connect.

### AFN01

Batch:

```text
TAIL_FRAGMENTATION
giant ratio at base maximum = 0.968504
```

Audit:

```text
exact graph kappa_connect = 2.224745
adaptive plateau          = 2.000000
```

Again, the plateau occurs just before the actual connectivity scale.

### AFN06

Batch:

```text
HARD_FRAGMENTATION
giant ratio at base maximum = 0.976378
```

Audit:

```text
exact graph kappa_connect = 3.069694
adaptive plateau          = 2.000000
```

The graph is only one further scale increase away from full connectivity, but the plateau
criterion terminates the extension first.

### INT03

Batch:

```text
HARD_FRAGMENTATION
giant ratio at base maximum = 0.748031
```

Audit:

```text
exact graph kappa_connect = 10.412395
adaptive plateau          = 10.000000
```

The chamber stops at kappa 10 even though the exact connectivity threshold is only slightly above it.

## 3. AFF04 numerical IQR pathology

AFF04 exposes a separate issue.

The chamber computes:

```text
median gap = 0.317837
IQR        = 1.0658141036401503e-14
```

The IQR is positive only at floating-point noise scale.

Because STRUC-PERC-I uses:

```text
IQR > 0 ? IQR : median
```

it treats this tiny numerical residue as an active physical scale instead of invoking the
documented median fallback.

That produces:

```text
chamber-scale exact kappa_connect
= 1.326886e+14
```

which is numerically pathological.

With an audit-only relative-zero tolerance of `1e-12`, the documented fallback behavior gives:

```text
median fallback exact kappa_connect
= 4.449490
```

No frozen chamber file has been modified. This is recorded as an implementation audit issue.

## 4. Consequence for the five non-full verdicts

The five raw verdicts remain part of the permanent record.

However, they should **not yet be treated as robust evidence of an admissibility–percolation
contradiction**.

The audit shows that:

- AFF01, AFN01, AFN06 and INT03 are sensitive to premature adaptive-extension stopping;
- AFF04 is dominated by a near-zero-IQR numerical fallback failure.

Therefore the raw categorical tiers mix structural information with implementation-scale effects.

## 5. What remains scientifically usable

Several findings are robust and worth preserving.

### Rank-one contrast

All six `R1_FREE` ladders reach full percolation at the first tested scale:

```text
kappa_connect = 0.01
```

All six `R1_FAIL` ladders also reach full percolation, but at:

```text
kappa_connect = 1.0
```

This is a large and perfectly repeated connectivity-scale difference, even though STRUC-I
admissibility remained complete in both classes.

That is not a traceability classifier by itself, but it is a genuine structural-scale distinction.

### Full-percolation majority

Twenty-five of the thirty frozen ladders are reported as fully percolating by the chamber batch.

The remaining five require audit rather than immediate theorem-level interpretation.

## 6. Cross-chamber status

Current justified state:

```text
STRUC-I:
30 / 30 perturbatively admissible

STRUC-PERC-I raw batch:
25 FULL
1 TAIL
4 HARD

STRUC-PERC-I implementation audit:
non-full tiers are not yet robust as final scientific verdicts
```

Therefore:

> **No final admissibility–percolation synthesis should yet be published from the raw batch tiers.**

## 7. Next move

Do **not** rerun STRUC-I.

Do **not** overwrite the STRUC-PERC-I raw batch.

The next move is a narrowly versioned STRUC-PERC-I audit/repair step addressing:

1. effective-zero IQR fallback tolerance;
2. adaptive-extension plateau logic;
3. reporting the exact connectivity threshold for the one-dimensional full-pairwise gap graph.

Only after that repaired/audited percolation instrument is frozen should the same 30 inputs be
re-evaluated for the final cross-chamber synthesis.

# Current State and Decision Point — UNNS-H Mode Project

## 1. Purpose

This document freezes the current state of the UNNS-H Mode project after the TCV event-level work, the TokaMark public-source expansion, the first `m_edge(t)` construction, and the small five-shot TokaMark comparison panel.

It belongs here:

```text
unns_hmode_project/
  docs/
    23_CURRENT_STATE_AND_DECISION_POINT.md
```

It follows:

```text
docs/
  22_TOKAMARK_SMALL_PANEL_M_EDGE_COMPARISON.md
```

The purpose is not to add another layer of procedural output. The purpose is to decide what has actually been gained, what has not been gained, and what should happen next.

---

## 2. Blunt status

The project has produced a plausible structural signal.

It has not produced physical validation of H-mode.

The current v0.1 `m_edge(t)` margin is useful as an exploratory diagnostic. It is not yet reliable enough for broad claims, because incomplete diagnostic cases can produce inflated positive-margin fractions.

Therefore:

```text
Do not claim H-mode validation.
Do not discard the work.
Do not continue blind scans or larger panels with v0.1 unchanged.
Freeze the exploratory pipeline at this point.
Introduce diagnostic confidence before any broader scaling.
```

---

## 3. What the project genuinely gained

### 3.1 TCV event-level branch structure

The TCV work showed that L-H transition data is not featureless. Branching concentrated around:

```text
power balance
transport
timing
edge/divertor response
```

This was the first useful structural result. It supported the working interpretation that H-mode access is not merely a total-power threshold problem, but a boundary-route organization problem.

### 3.2 Event-level edge-admissibility model

The observed TCV branches were converted into an event-level margin:

```text
m_edge_event = C_edge_capacity - F_route_fragmentation
```

This gave the project a computable object instead of a verbal metaphor.

The event-level model separated reviewed TCV shots into:

```text
negative / leakage-like
boundary-ambiguous
positive / edge-response-like
```

This was still event-level, not time-resolved.

### 3.3 Full-corpus extension

The event-level scoring was extended across the full 92-event TCV canonical corpus.

That gave statistical breadth, but it did not solve the missing time-resolved positive-corridor problem.

### 3.4 Public TokaMark source acquisition

The project found that public TokaMark/MAST data can be accessed through HTTP metadata and direct chunk requests.

The metadata candidate scan found many full diagnostic candidates, including shot `12063`.

This solved a practical source problem:

```text
TCV lacked a time-resolved positive-corridor trace.
TokaMark supplied public candidate shots with profile, edge, power, density, and geometry diagnostics.
```

### 3.5 First public `m_edge(t)` trace

Shot `12063` was successfully read at array level and converted into a first normalized time-resolved margin:

```text
m_edge(t) = C_edge_capacity(t) - F_route_fragmentation(t)
```

The resulting trace was not uniformly positive. It was mostly boundary-ambiguous, with positive-boundary excursions and negative-leakage intervals.

This was a useful result because it showed the margin was not trivially labeling the whole shot as favorable.

### 3.6 Trace-level interpretability

The trace inspection found interpretable positive and negative windows.

For shot `12063`, the positive windows were internally coherent because they generally showed:

```text
C_edge_capacity > F_route_fragmentation
edge-response contribution present
reduced / low power-balance pressure in several windows
missingness not dominant
```

The negative windows were also coherent because they showed:

```text
F_route_fragmentation > C_edge_capacity
higher route-stress / power-balance pressure
lower margin than surrounding context
```

This supported the v0.1 margin as an internally interpretable exploratory diagnostic.

### 3.7 Cross-shot comparison

Shot `12063` was compared against weaker shot `11830`.

The comparator decided:

```text
reference_structurally_stronger
```

This suggested v0.1 was not simply labeling every usable TokaMark shot as equally positive.

### 3.8 Five-shot panel

The small five-shot panel ranked `12063` first:

```text
12063 rank 1
11876 rank 2
11776 rank 3
11768 rank 4
11830 rank 5
```

The panel decision was:

```text
reference_structurally_strong_but_not_unique
```

This was the most honest result so far. It strengthened the structural case for `12063`, but it also exposed a weakness in v0.1.

---

## 4. What the project has not gained

The project has not gained physical proof of H-mode origin.

It has not shown that the positive `m_edge(t)` windows are actual L-H transition windows.

It has not identified a physically anchored L-H transition time in shot `12063`.

It has not proven that `m_edge(t)` predicts confinement transitions.

It has not established cross-machine generality.

It has not produced a final formula.

It has not ruled out preprocessing artifacts in TokaMark-normalized signals.

It has not yet included a diagnostic confidence correction.

---

## 5. The main methodological problem now

The five-shot panel exposed the key problem:

```text
v0.1 discriminates, but incomplete shots can still look artificially positive.
```

Specifically, low-quality or incomplete candidates such as `11776` and `11768` can show high positive-boundary fractions or positive median margins despite missing critical diagnostics.

That means the current v0.1 margin confuses two different things:

```text
1. structural edge-capacity signal
2. diagnostic absence / reduced fragmentation evidence
```

This is not acceptable for broader scaling.

The formula must distinguish:

```text
m_edge_raw(t)
  the raw structural margin

Q_diag(t)
  diagnostic confidence / coverage quality

m_edge_conf(t)
  confidence-weighted margin
```

Without this distinction, larger scans will produce misleading positives.

---

## 6. What would be useless from here

The following would now be low-value or misleading:

```text
running more random TokaMark shots with v0.1 unchanged
creating more reports without changing the question
claiming that 12063 validates H-mode
scaling to all 11,188 TokaMark shots
building a public article that overstates the result
treating high positive fraction as success without diagnostic confidence
```

This is the “dancing around” risk.

More data will not fix a scoring ambiguity. The scoring ambiguity must be addressed first.

---

## 7. What would be meaningful from here

There are only two meaningful paths.

### Path A — Technical continuation

Introduce a diagnostic-confidence revision.

The next component would be:

```text
components/
  tokamark_m_edge_confidence_revision.py
```

It should preserve the existing margin and add confidence-aware columns:

```text
m_edge_raw(t)
Q_diag(t)
Q_capacity(t)
Q_fragmentation(t)
P_missing_critical(t)
m_edge_conf(t)
m_edge_conf_state
```

At minimum, it should penalize missing or unreliable:

```text
NBI power
D-alpha
Thomson Te/ne
soft-X
transport term
geometry support
high missingness_pressure
```

The goal would be to answer:

> Does diagnostic confidence preserve `12063` while suppressing incomplete inflated cases such as `11776` and `11768`?

This is the only technical continuation that directly addresses the weakness found by the panel.

### Path B — Stop and write this as a pilot study

The project can also stop here and be written as a pilot study.

The correct claim would be:

> A UNNS-H Mode exploratory pipeline was developed and tested on TCV and public TokaMark/MAST data. It produced a plausible boundary-admissibility signal and identified shot `12063` as structurally stronger in a small public panel, but the current v0.1 margin requires diagnostic-confidence correction before physical validation or broader scaling.

That would be honest, useful, and publishable as a methodological note if framed carefully.

---

## 8. Recommended decision

The recommended decision is:

```text
Freeze v0.1 as exploratory.
Do not scale v0.1 further.
Do not claim physical validation.
Proceed only with a diagnostic-confidence revision, or stop and write the pilot study.
```

The project should not continue producing more procedural files unless the next file directly addresses diagnostic confidence.

---

## 9. Minimum next technical requirement

Any next technical component must satisfy this requirement:

```text
It must reduce inflated positive margins in incomplete shots
without erasing the stronger structure of shot 12063.
```

The immediate test set should remain the same five-shot panel:

```text
12063
11830
11876
11768
11776
```

The revision succeeds only if:

```text
12063 remains structurally strong
11776 and 11768 are penalized for missing critical diagnostics
11876 remains active but clearly confidence-limited
11830 remains weaker because it lacks soft-X support
m_edge_raw is preserved for auditability
m_edge_conf is reported separately
```

If the revision cannot do this, then the framework is not yet ready for broader claims.

---

## 10. Correct next document if continuing

If continuing technically, the next document should be:

```text
docs/
  24_DIAGNOSTIC_CONFIDENCE_REVISION_PLAN.md
```

not another results report.

That plan should define:

```text
Q_diag(t)
P_missing_critical(t)
confidence-weighted margin logic
acceptance criteria
failure conditions
same-panel retest
```

Only after that should a new component be written.

---

## 11. Correct next article/report if stopping

If stopping and writing the pilot study, the manuscript/report title could be:

```text
Boundary-Admissibility Signatures in L-H Transition Data:
A UNNS Pilot Study on TCV and Public TokaMark/MAST Diagnostics
```

The claim should be framed as:

```text
exploratory structural modeling
not physical validation
not proof of H-mode origin
not a predictive operational model yet
```

The value would be that the pipeline found structured, nontrivial diagnostic behavior and revealed exactly what must be added next.

---

## 12. Final decision statement

The UNNS-H Mode project has reached a real decision point.

The work is not useless. It produced a coherent exploratory pipeline and a plausible structural signal. It also produced a useful negative result: v0.1 cannot be trusted at scale because incomplete diagnostics can inflate positive margins.

Therefore, the correct conclusion is:

> The current pipeline is strong enough to justify a diagnostic-confidence revision, but not strong enough to justify physical validation claims.

The next meaningful step is not more scanning. It is either:

```text
A) define and implement diagnostic confidence, then retest the same five-shot panel;
```

or:

```text
B) stop here and write the current work as a bounded pilot study.
```

Anything else risks becoming motion without discovery.

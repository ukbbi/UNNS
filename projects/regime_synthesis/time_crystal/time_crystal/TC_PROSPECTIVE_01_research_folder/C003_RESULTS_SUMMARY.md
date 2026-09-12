# TC_P01_C003 — Extended Results Summary and Domain-Boundary Closeout

## Candidate status

```text
CANDIDATE: TC_P01_C003
CAMPAIGN: TC_PROSPECTIVE_01
STATUS: CLOSED
RESULT TYPE: DOMAIN-BOUNDARY RESULT
```

C003 is the third formally completed prospective candidate of the
`TIME-CRYSTAL-I v1.1.0` campaign.

Unlike C001 and C002, C003 is **not** a prospective positive of the present
temporal grammar.

Instead, C003 is the first documented prospective case in which a physically
ordered time-structured system lies outside the class that the frozen
integer-depth `TIME-CRYSTAL-I` temporal layer recognizes as supported temporal
recurrence.

The complete sequence was:

```text
source preservation
→ workbook reconnaissance
→ candidate/control regime selection
→ rejection of invalid scalar ingestion
→ dual-clock adapter
→ blind chamber run
→ matched-control blind run
→ evidence audit
→ analysis lock
→ local Windows reproduction
→ manual inspection
→ posthoc candidate reveal
→ posthoc control reveal
→ domain-boundary closeout
```

The blind results were locked before physical identities were revealed.

---

# 1. Source

Source workbook:

```text
rawdata.xls
```

SHA-256:

```text
b016dd5326b3b010caa14edc80eda374863a5e59c98d574a5536dc5ddeaeb38a
```

The workbook contains the experimental datasets associated with the
discrete-time-quasi-crystal study.

The source was preserved as the original legacy XLS workbook.

The C003 adapter read the workbook directly and did not rewrite or overwrite
the source file.

---

# 2. Candidate type

C003 is an:

```text
experimental quantum-many-body quasi-periodic candidate
```

After posthoc reveal, the physical class was recorded as:

```text
Experimental Z2 discrete time quasi-crystal,
robust long-interaction regime
(Fig. 1d; tau1=2.00 us, tau2=3.236 us,
rotation factor 1-epsilon=0.933)
```

The matched control was revealed as:

```text
Matched quasi-periodically driven experimental short-interaction regime
with split subharmonic responses / breakdown of DTQC order
(Fig. 1b; tau1=0.25 us, tau2=0.404 us,
rotation factor 1-epsilon=0.933)
```

C003 therefore differs qualitatively from C001 and C002:

```text
C001 → integer-period large-period DTC candidate
C002 → integer-period prethermal-DTC numerical candidate
C003 → quasi-periodic DTQC candidate
```

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

- the temporal closure formula;
- the integer `q` search range;
- recurrence-family contrast;
- shuffle-null protocol;
- temporal thresholds;
- chamber hierarchy;
- higher-sector verdict logic.

This is essential to the interpretation of C003.

The chamber was **not** extended with a quasi-periodic metric before seeing the
C003 outcome.

---

# 4. Why C003 was selected

C001 and C002 had already shown that the frozen temporal layer could recognize
supported integer-depth recurrence in two materially different settings:

```text
C001 → q0 = 4 → TEMPORAL_RECURRENCE
C002 → q0 = 2 → TEMPORAL_RECURRENCE
```

C003 was deliberately selected to ask a different question:

> **What happens when the same frozen integer-depth temporal grammar is applied
> to a physically ordered system whose temporal organization is quasi-periodic
> rather than an ordinary integer-period recurrence?**

Thus C003 was designed as a **domain-boundary test**, not merely another
positive candidate.

---

# 5. Workbook reconnaissance

The source workbook contains four main sheets:

```text
Fig. 1
Fig. 2
Fig. 3
Fig. 4
```

For the prospective C003 run, the candidate/control mapping was frozen from the
representative signed polarization dynamics in `Fig. 1`.

Neutral candidate:

```text
TC_P01_C003
```

Neutral matched control:

```text
TC_P01_C003_CTRL
```

The physical figure identities were kept outside the blind candidate bundles
and stored only in separate ground-truth records.

---

# 6. First ingestion attempt and why it was rejected

A direct one-observable candidate representation was initially tested against
the frozen chamber input contract.

The chamber refused that representation because its temporal closure
implementation requires at least two accepted coordinates.

The direct scalar ingestion was therefore rejected **before any scientific
verdict was accepted**.

The campaign did not respond by:

- duplicating the same signal into two fake coordinates;
- treating experimental error bars as a dynamical coordinate;
- inventing a second observable;
- changing the chamber;
- weakening the input contract.

This failure was treated as an adapter-design problem, not as a physical result.

---

# 7. Dual-clock adapter

The physical source contains two incommensurate drive clocks.

The C003 adapter therefore uses the experimentally present two-clock structure
itself.

For each common event index `n`, the chamber state is constructed as:

```text
X_n = [ Sx(n tau1), Sx(n tau2) ]
```

using only measured polarization values already present in the workbook.

The source time axis encodes the union of the two event sequences.

The documented drive-time ratio used by the adapter is:

```text
tau2 / tau1 = 1.618
```

The same transform is applied to candidate and control.

The final neutral candidate and control each contain:

```text
115 paired dual-clock events
```

---

# 8. Adapter firewall

The C003 adapter does **not**:

- interpolate missing measurements;
- generate synthetic polarization values;
- resample onto an artificial uniform grid;
- impose a conventional Floquet stroboscopic clock;
- insert the known quasi-crystal response frequencies;
- Fourier-filter toward expected peaks;
- sign-align the data;
- select a favorable time sub-window;
- tune `qmax`;
- change closure thresholds;
- change family-contrast thresholds;
- modify the shuffle test;
- manufacture rigidity evidence;
- manufacture collective evidence;
- manufacture spectral evidence.

The chamber therefore receives a physically grounded two-coordinate projection
of the recorded quasi-periodic dynamics, but no target verdict.

---

# 9. Candidate blind result

Blind mode:

```text
TRUE
```

Candidate:

```text
TC_P01_C003
```

Automatic integer recurrence candidate:

```text
q0 = 6
```

Closure:

```text
C(6) = 0.1987652678
```

Recurrence-family contrast:

```text
F = 0.0934328447
```

Shuffle-null empirical p-value:

```text
p = 0.9601990050
```

Temporal sector:

```text
NOT_SUPPORTED
```

Final blind chamber verdict:

```text
NO_TEMPORAL_ORDER
```

Level:

```text
0
```

---

# 10. Authoritative candidate evidence hash and analysis lock

Authoritative Windows evidence SHA-256:

```text
edf1ea879e092e5f92a889fa4eb3edc056b07f70fbc2a95e7c864272b2877c15
```

Authoritative Windows analysis lock:

```text
2cce593284bf3416334871fae27c4bdaf54b702c3413af7233fa7182c1e0c066
```

This lock existed before the physical identity of C003 was revealed.

Therefore the later knowledge that the candidate is a robust experimental DTQC
could not influence the blind result.

---

# 11. Candidate evidence boundary

C003 was intentionally run as a temporal boundary test.

Blind sector state:

```text
Temporal     NOT_SUPPORTED
Rigidity     NOT_TESTED
Collective   NOT_TESTED
Spectral     NOT_TESTED
```

The workbook contains additional information relevant to stability and phase
structure, but that material was not retrospectively converted into higher
`TIME-CRYSTAL-I` sectors during the blind run.

The chamber therefore made its decision solely from the frozen temporal layer.

---

# 12. Matched-control blind result

Control:

```text
TC_P01_C003_CTRL
```

Automatic integer recurrence candidate:

```text
q0 = 6
```

Closure:

```text
C(6) = 0.0946396893
```

Family contrast:

```text
F = 0.0308741990
```

Shuffle-null empirical p-value:

```text
p = 0.9950248756
```

Temporal sector:

```text
NOT_SUPPORTED
```

Blind verdict:

```text
NO_TEMPORAL_ORDER
```

Level:

```text
0
```

---

# 13. Authoritative control evidence hash and analysis lock

Control evidence SHA-256:

```text
a9ac8f8f1f704bf779718c5ef63a4f96c2885827cbdba1729bca2f3654897fc8
```

Authoritative control analysis lock:

```text
561ed97513e009cff5865761a5bf098777957eafee77cc76020d099741e4d18e
```

The matched-control result was independently locked before its physical
identity was revealed.

---

# 14. Candidate posthoc reveal

Candidate reveal status:

```text
POSTHOC_REVEAL_COMPLETE
```

Revealed physical class:

```text
Experimental Z2 discrete time quasi-crystal,
robust long-interaction regime
(Fig. 1d; tau1=2.00 us, tau2=3.236 us,
rotation factor 1-epsilon=0.933)
```

Previously locked blind verdict:

```text
NO_TEMPORAL_ORDER
```

No chamber-level expected verdict had been preregistered:

```text
expected_verdict = null
```

Therefore:

```text
verdict_match = null
```

This is correct.

C003 was a boundary test, not a preregistered demand that the frozen chamber
must call the system temporally ordered.

---

# 15. Candidate ground-truth provenance

Ground-truth SHA-256:

```text
68ab853d9f90db028efe00ca6998c968ff905cda5cbf7352692b75ff0f94869d
```

The posthoc reveal explicitly links that ground-truth record to the already
locked analysis:

```text
2cce593284bf3416334871fae27c4bdaf54b702c3413af7233fa7182c1e0c066
```

---

# 16. Matched-control posthoc reveal

Control reveal status:

```text
POSTHOC_REVEAL_COMPLETE
```

Revealed physical class:

```text
Matched quasi-periodically driven experimental short-interaction regime
with split subharmonic responses / breakdown of DTQC order
(Fig. 1b; tau1=0.25 us, tau2=0.404 us,
rotation factor 1-epsilon=0.933)
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

because no chamber-level verdict was preregistered.

---

# 17. Control ground-truth provenance

Control ground-truth SHA-256:

```text
2894267e8e58cd6712f0a5fb7ef9abb79a12f8338a713e61f38c612a20f1f882
```

The reveal is tied to the already locked control analysis:

```text
561ed97513e009cff5865761a5bf098777957eafee77cc76020d099741e4d18e
```

---

# 18. The decisive C003 contrast

The posthoc physical identities establish that the blind pair consisted of:

```text
C003
→ robust experimental DTQC regime
```

versus:

```text
C003_CTRL
→ matched quasi-periodic breakdown regime
```

Yet the frozen temporal chamber returned:

```text
C003
→ NO_TEMPORAL_ORDER

C003_CTRL
→ NO_TEMPORAL_ORDER
```

This is the central C003 result.

---

# 19. Why this is not a simple negative result

It would be incorrect to summarize C003 as:

> "The chamber found no temporal order, therefore the physical system is not
> temporally ordered."

The posthoc identity explicitly establishes that C003 belongs to the reported
robust DTQC regime.

The correct interpretation is instead:

> **The present `TIME-CRYSTAL-I v1.1.0` integer-depth temporal grammar does not
> recognize the ordered quasi-periodic C003 regime as supported temporal
> recurrence.**

That is a statement about the **domain of the chamber metric**, not a negation
of the underlying physical regime.

---

# 20. Why the control matters

The candidate and control both fail the frozen temporal gate, but they are not
numerically identical.

Candidate:

```text
C = 0.1987652678
F = 0.0934328447
p = 0.9601990050
```

Control:

```text
C = 0.0946396893
F = 0.0308741990
p = 0.9950248756
```

The candidate therefore carries a larger integer-depth closure projection and a
larger family contrast than the breakdown control.

However, both shuffle-null probabilities are overwhelmingly non-significant.

The frozen chamber is therefore correct, according to its own preregistered
rules, to reject both.

This prevents us from retrospectively converting a small relative difference
into a positive verdict.

---

# 21. The key domain-boundary statement

C003 establishes the first prospective domain boundary of the temporal layer:

```text
physically robust quasi-periodic temporal order
≠
supported integer-depth temporal recurrence
```

within `TIME-CRYSTAL-I v1.1.0`.

Equivalently:

> **The frozen chamber is an integer-recurrence grammar, not a universal
> detector of every physically meaningful form of temporal order.**

This is the principal scientific gain from C003.

---

# 22. Relationship to C001 and C002

The three prospective candidates now form a structurally informative sequence.

## C001

```text
reported large-period DTC candidate
→ q0 = 4
→ TEMPORAL_RECURRENCE
```

Matched control:

```text
NO_TEMPORAL_ORDER
```

Principal gain:

```text
prospective recurrence-depth generalization from 2T to 4T
```

---

## C002

```text
numerical prethermal-DTC candidate
→ q0 = 2
→ TEMPORAL_RECURRENCE
```

Matched control:

```text
NO_TEMPORAL_ORDER
```

Principal gain:

```text
prospective candidate/control specificity in a signed numerical setting
```

---

## C003

```text
robust experimental DTQC candidate
→ q0 = 6 projection
→ NO_TEMPORAL_ORDER
```

Matched breakdown control:

```text
NO_TEMPORAL_ORDER
```

Principal gain:

```text
first prospective domain-boundary result
```

---

# 23. What the three-candidate sequence reveals

The campaign now supports a stronger picture than any single candidate could.

The frozen temporal layer can distinguish:

```text
ordinary/supportable integer recurrence
```

from:

```text
absence of supported integer recurrence
```

and it can generalize to at least:

```text
q0 = 2
q0 = 4
```

prospectively.

But C003 shows that a physically ordered quasi-periodic regime need not map
into that same integer-depth class.

Thus the temporal sector has acquired an empirically observed domain:

```text
SUPPORTED:
integer-depth recurrent order captured by C(q)

NOT AUTOMATICALLY SUPPORTED:
quasi-periodic temporal order with no single ordinary integer recurrence
```

This boundary was discovered prospectively rather than added theoretically
after the fact.

---

# 24. Why the frozen chamber must not be changed retroactively

C003 now tells us exactly where one might be tempted to extend the chamber:

- multi-frequency closure;
- vector recurrence indices;
- irrational/incommensurate recurrence coordinates;
- toroidal phase closure;
- two-clock closure families.

None of those should be added to `TIME-CRYSTAL-I v1.1.0`.

Doing so would erase the meaning of the C003 result.

Any quasi-periodic extension must become a **new chamber version or a distinct
branch**, and it must be validated on new unseen data.

C003 must remain permanently associated with the unchanged v1.1.0 result:

```text
NO_TEMPORAL_ORDER
```

---

# 25. What C003 establishes

C003 establishes that:

1. the frozen integer-depth chamber does not support temporal recurrence for the
   robust DTQC candidate under the preregistered dual-clock adapter;
2. the matched DTQC-breakdown control is also rejected;
3. the candidate has a stronger integer-depth projection than the control, but
   not enough to survive the shuffle-null gate;
4. the physical identity revealed afterward places the candidate in a robust
   quasi-periodic time-crystalline regime;
5. therefore the current temporal grammar has a demonstrated domain boundary.

The strongest correct statement is:

> **C003 prospectively demonstrates that robust quasi-periodic time-crystalline
> order can lie outside the admissible integer-recurrence class defined by
> `TIME-CRYSTAL-I v1.1.0`.**

---

# 26. What C003 does not establish

C003 does **not** establish that:

- DTQC order is absent;
- quasi-periodic temporal order is physically weaker than periodic DTC order;
- every DTQC will fail `TIME-CRYSTAL-I`;
- the dual-clock adapter is the unique possible representation;
- a future quasi-periodic closure metric would succeed;
- the present chamber should be immediately modified;
- C003 falsifies the entire UNNS temporal-closure program.

The result is more specific:

```text
the present frozen integer-depth grammar is insufficient for this robust DTQC regime
```

That is a domain statement, not a universal negative conclusion.

---

# 27. Higher-sector status

C003 did not progress beyond the temporal gate.

Therefore:

```text
Rigidity     NOT_TESTED
Collective   NOT_TESTED
Spectral     NOT_TESTED
```

This should not be interpreted as evidence against those physical properties.

The higher gates are simply unreachable under the present chamber hierarchy
once the temporal gate is not supported.

---

# 28. Methodological success

C003 is also a success of campaign methodology.

The campaign:

- identified that the first scalar representation violated the chamber input
  contract;
- refused to fake a second coordinate;
- constructed a physically grounded dual-clock projection;
- used the same adapter for candidate and control;
- froze the result;
- reproduced it locally on Windows;
- revealed the physical identities only afterward;
- accepted a domain-boundary result instead of tuning the instrument until it
  became positive.

That is exactly what prospective validation is supposed to do.

---

# 29. Canonical files to preserve

Primary candidate record:

```text
locked_runs\C003\
├── analysis_lock.json
├── blind_verdict.json
├── evidence_audit.json
├── EVIDENCE_AUDIT.md
├── external_result.json
├── posthoc_comparison.json
└── RUN_LOG.txt
```

Matched-control record:

```text
locked_runs\C003_CTRL\
├── analysis_lock.json
├── blind_verdict.json
├── evidence_audit.json
├── EVIDENCE_AUDIT.md
├── external_result.json
├── posthoc_comparison.json
└── RUN_LOG.txt
```

These fourteen files constitute the closed prospective C003 pair.

Do not overwrite them.

---

# 30. Recommended campaign registry entry

The campaign record should now state:

```text
Candidate:
TC_P01_C003

Status:
CLOSED

Result type:
DOMAIN-BOUNDARY RESULT

Candidate type:
Experimental quantum-many-body quasi-periodic

Physical class:
Experimental Z2 discrete time quasi-crystal,
robust long-interaction regime
(Fig. 1d; tau1=2.00 us, tau2=3.236 us,
rotation factor 1-epsilon=0.933)

Blind temporal sector:
NOT_SUPPORTED

Automatic q0:
6

Closure:
0.1987652678

Family contrast:
0.0934328447

Shuffle p:
0.9601990050

Blind verdict:
NO_TEMPORAL_ORDER

Blind level:
0

Candidate analysis lock:
2cce593284bf3416334871fae27c4bdaf54b702c3413af7233fa7182c1e0c066

Matched control:
TC_P01_C003_CTRL

Control physical class:
Matched quasi-periodically driven experimental short-interaction regime
with split subharmonic responses / breakdown of DTQC order

Control q0:
6

Control closure:
0.0946396893

Control family contrast:
0.0308741990

Control shuffle p:
0.9950248756

Control verdict:
NO_TEMPORAL_ORDER

Control analysis lock:
561ed97513e009cff5865761a5bf098777957eafee77cc76020d099741e4d18e

Posthoc reveal:
COMPLETE for candidate and control

Expected chamber verdict:
NONE

Verdict match:
N/A

Principal finding:
The robust quasi-periodic DTQC candidate lies outside the supported
integer-recurrence class of TIME-CRYSTAL-I v1.1.0 under the frozen C003 protocol.
```

---

# 31. Campaign state after C003

The prospective campaign now contains:

```text
3 closed candidates
3 matched controls
6 locked records
0 unrevealed candidate records
```

Candidate outcomes:

```text
C001
→ TEMPORAL_RECURRENCE
→ q0 = 4

C002
→ TEMPORAL_RECURRENCE
→ q0 = 2

C003
→ NO_TEMPORAL_ORDER
→ q0 = 6 projection, not supported
```

This is a much stronger campaign state than three positive candidates would
have provided, because the third candidate has begun to define the chamber's
actual domain.

---

# 32. Scientific significance

C003 changes the interpretation of `TIME-CRYSTAL-I`.

Before C003, the temporal layer could still be read too broadly as a candidate
measure of temporal order in general.

After C003, the evidence supports a narrower and more useful interpretation:

> **`TIME-CRYSTAL-I v1.1.0` detects a class of persistent integer-depth temporal
> recurrence, not arbitrary temporal order.**

That is a clarification of the chamber's scientific meaning.

It makes the instrument more interpretable rather than less useful.

---

# 33. Implication for future chamber development

C003 naturally motivates a future research question:

```text
Can UNNS temporal closure be generalized from integer-depth recurrence
to quasi-periodic multi-clock closure without destroying the distinctions
already validated by TIME-CRYSTAL-I v1.1.0?
```

That question must not be answered by modifying the closed C003 campaign.

A future quasi-periodic branch would need:

- its own metric specification;
- its own frozen adapter rules;
- its own null model;
- its own controls;
- new unseen DTQC candidates;
- tests showing that ordinary DTCs and ordinary quasi-periodic signals remain
  distinguishable.

C003 becomes the benchmark that such a future branch must explain.

---

# 34. Limitations

C003 is one robust-DTQC / breakdown-control pair.

The dual-clock adapter is physically grounded, but it is still a projection of
the full many-body experiment into the present chamber input format.

The campaign has not yet tested:

- multiple independent DTQC datasets;
- alternative quasi-periodic drive ratios;
- quasi-periodic numerical controls with known analytic structure;
- a frozen quasi-periodic closure metric;
- prospective higher-sector DTQC evidence.

Therefore the present conclusion should remain bounded to the demonstrated
domain boundary.

---

# 35. C003 closeout verdict

The complete C003 result is:

```text
PROSPECTIVE CANDIDATE:
TC_P01_C003

RESULT TYPE:
DOMAIN-BOUNDARY RESULT

CANDIDATE TYPE:
Experimental quantum-many-body quasi-periodic

BLIND TEMPORAL ORDER:
NOT_SUPPORTED

AUTOMATIC INTEGER RECURRENCE:
q0 = 6

CLOSURE:
0.1987652678

FAMILY CONTRAST:
0.0934328447

SHUFFLE P:
0.9601990050

BLIND CHAMBER VERDICT:
NO_TEMPORAL_ORDER

MATCHED CONTROL:
TC_P01_C003_CTRL

CONTROL TEMPORAL ORDER:
NOT_SUPPORTED

CONTROL VERDICT:
NO_TEMPORAL_ORDER

POSTHOC PHYSICAL CLASS:
Experimental Z2 discrete time quasi-crystal,
robust long-interaction regime

CONTROL PHYSICAL CLASS:
Matched quasi-periodically driven short-interaction regime
with split subharmonic responses / breakdown of DTQC order

HIGHER-SECTOR STATUS:
NOT TESTED

CANDIDATE STATUS:
CLOSED

CONTROL STATUS:
CLOSED
```

---

# 36. Final conclusion

C003 is not a failed prospective positive.

It is more informative than that.

The frozen `TIME-CRYSTAL-I v1.1.0` chamber had already demonstrated prospective
recognition of supported integer-depth recurrence at `q0=4` and `q0=2`.

C003 then confronted the same unchanged chamber with an experimentally robust
quasi-periodic time-crystalline regime.

The chamber did **not** call that regime temporally ordered under its frozen
integer-depth rules.

The matched breakdown control was also rejected.

After the blind results were locked, the candidate was revealed to be the robust
experimental Z2 DTQC regime.

The correct closeout conclusion is therefore:

> **C003 is the first documented prospective domain-boundary result of
> `TIME-CRYSTAL-I`: physically robust quasi-periodic time-crystalline order can
> fall outside the supported integer-recurrence class defined by the current
> chamber.**

This result should remain permanently attached to the unchanged
`TIME-CRYSTAL-I v1.1.0` campaign record.

C003 should now remain closed and untouched.

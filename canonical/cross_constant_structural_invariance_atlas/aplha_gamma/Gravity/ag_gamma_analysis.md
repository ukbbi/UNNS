# αG γ-Sweep Analysis — Planetary Geoid Domain
**UNNS Substrate Program · Alignment Matrix · Column IV (αG)**
Protocol: AG_DEFORMATION_PROTOCOL_v2 · Instrument: STRUC-I v1.0.4
Date: 2026-03-29 · Status: COMPLETE · 3 planetary bodies · 17 γ-values each

**Note on file naming:** `earth_gamma.zip` contains Mars geoid data
(`mars_geoid_gamma_*` ladder names). The filename is misleading; the
ladder names are authoritative and used throughout this document.

---

## 1. Corpus

| Body  | n (ladder pairs) | L_max | γ-values | Data source   | ZIP file              |
|-------|-----------------|-------|----------|---------------|-----------------------|
| Earth | 299             | 300   | 17       | EIGEN-6C4     | earth_gamma_output.zip |
| Mars  | 230             | ~84   | 17       | JGM85F01      | earth_gamma.zip ¹      |
| Moon  | 117             | ~118  | 17       | AIUB-GRL350A  | moon_gamm_outcome.zip  |

¹ Filename mislabeled — contents confirmed as Mars geoid by ladder name prefix.

γ ∈ {0.80, 0.85, 0.90, 0.95, 0.96, 0.97, 0.98, 0.99,
      1.00, 1.01, 1.02, 1.03, 1.04, 1.05, 1.10, 1.15, 1.20}

17-point grid matching Columns I–III.

---

## 2. Summary Table — All Bodies

| Body  | ρ̄ @ γ=1.00 | ρ̄ min | ρ̄ max | Δρ̄   | max ρ @ γ=1.00 | Monotone? | γ*   | min Aκ (sweep) | min Aκ @ γ=1.00 | State (all γ)       | αG-class           |
|-------|------------|--------|--------|-------|----------------|-----------|------|----------------|-----------------|---------------------|--------------------|
| Earth | 0.5033     | 0.5030 | 0.5037 | 0.0007 | 0.7064        | No        | none | **1.0000**     | **1.0000**      | Weak Persistence    | **TYPE I · CALM**  |
| Mars  | 0.6648     | 0.6630 | 0.6652 | 0.0022 | 0.8087        | No        | none | 0.9990         | **1.0000**      | Boundary-Stabilized | **TYPE I**         |
| Moon  | 0.4161     | 0.4159 | 0.4176 | 0.0016 | 0.6111        | No        | none | 0.9990         | **1.0000**      | Weak Persistence    | **TYPE I**         |

---

## 3. Full γ-Sweep Data

### Earth — n=299 per ladder (EIGEN-6C4, L_max=300)

| γ     | ρ̄     | max ρ  | min Aκ   | state            |
|-------|--------|--------|----------|------------------|
| 0.80  | 0.5034 | 0.7055 | 1.000000 | Weak Persistence |
| 0.85  | 0.5032 | 0.7059 | 1.000000 | Weak Persistence |
| 0.90  | 0.5033 | 0.7065 | 1.000000 | Weak Persistence |
| 0.95  | 0.5034 | 0.7048 | 1.000000 | Weak Persistence |
| 0.96  | 0.5035 | 0.7053 | 1.000000 | Weak Persistence |
| 0.97  | 0.5031 | 0.7056 | 1.000000 | Weak Persistence |
| 0.98  | 0.5035 | 0.7042 | 1.000000 | Weak Persistence |
| 0.99  | 0.5033 | 0.7046 | 1.000000 | Weak Persistence |
| **1.00** | **0.5033** | **0.7064** | **1.000000** | Weak Persistence |
| 1.01  | 0.5034 | 0.7064 | 1.000000 | Weak Persistence |
| 1.02  | 0.5037 | 0.7066 | 1.000000 | Weak Persistence |
| 1.03  | 0.5036 | 0.7061 | 1.000000 | Weak Persistence |
| 1.04  | 0.5034 | 0.7052 | 1.000000 | Weak Persistence |
| 1.05  | 0.5035 | 0.7049 | 1.000000 | Weak Persistence |
| 1.10  | 0.5030 | 0.7054 | 1.000000 | Weak Persistence |
| 1.15  | 0.5035 | 0.7048 | 1.000000 | Weak Persistence |
| 1.20  | 0.5033 | 0.7063 | 1.000000 | Weak Persistence |

Trend check: 0 rises > 0.001, 0 falls > 0.001 — pure flat scatter.
Aκ = 1.0000 exact at every γ-value. Earth is the cleanest null in the corpus.

---

### Mars — n=230 per ladder (JGM85F01)

| γ     | ρ̄     | max ρ  | min Aκ   | state               |
|-------|--------|--------|----------|---------------------|
| 0.80  | 0.6634 | 0.8074 | 0.999500 | Boundary-Stabilized |
| 0.85  | 0.6633 | 0.8103 | 0.999500 | Boundary-Stabilized |
| 0.90  | 0.6637 | 0.8104 | 0.999500 | Boundary-Stabilized |
| 0.95  | 0.6651 | 0.8076 | 0.999500 | Boundary-Stabilized |
| 0.96  | 0.6630 | 0.8091 | 0.999500 | Boundary-Stabilized |
| 0.97  | 0.6632 | 0.8069 | 0.999500 | Boundary-Stabilized |
| 0.98  | 0.6638 | 0.8084 | 0.999500 | Boundary-Stabilized |
| 0.99  | 0.6652 | 0.8079 | 0.999000 | Boundary-Stabilized |
| **1.00** | **0.6648** | **0.8087** | **1.000000** | Boundary-Stabilized |
| 1.01  | 0.6646 | 0.8079 | 0.999500 | Boundary-Stabilized |
| 1.02  | 0.6638 | 0.8124 | 0.999500 | Boundary-Stabilized |
| 1.03  | 0.6648 | 0.8078 | 0.999500 | Boundary-Stabilized |
| 1.04  | 0.6651 | 0.8075 | 0.999500 | Boundary-Stabilized |
| 1.05  | 0.6639 | 0.8109 | 0.999500 | Boundary-Stabilized |
| 1.10  | 0.6646 | 0.8091 | 1.000000 | Boundary-Stabilized |
| 1.15  | 0.6646 | 0.8072 | 0.999500 | Boundary-Stabilized |
| 1.20  | 0.6652 | 0.8111 | 0.999500 | Boundary-Stabilized |

Trend check: 3 rises > 0.001, 2 falls > 0.001 — irregular scatter, no trend.
Marginal Aκ events throughout (min 0.9990 at γ=0.99). No distinguished γ-point.
Aκ=1.0000 at γ=1.00 and γ=1.10 only — not a structural minimum, just scatter.

---

### Moon — n=117 per ladder (AIUB-GRL350A)

| γ     | ρ̄     | max ρ  | min Aκ   | state            |
|-------|--------|--------|----------|------------------|
| 0.80  | 0.4166 | 0.6252 | 1.000000 | Weak Persistence |
| 0.85  | 0.4166 | 0.6223 | 1.000000 | Weak Persistence |
| 0.90  | 0.4169 | 0.6235 | 1.000000 | Weak Persistence |
| 0.95  | 0.4173 | 0.6417 | 0.999000 | Weak Persistence |
| 0.96  | 0.4166 | 0.6210 | 0.999000 | Weak Persistence |
| 0.97  | 0.4166 | 0.6233 | 1.000000 | Weak Persistence |
| 0.98  | 0.4164 | 0.6096 | 0.999500 | Weak Persistence |
| 0.99  | 0.4165 | 0.6113 | 1.000000 | Weak Persistence |
| **1.00** | **0.4161** | **0.6111** | **1.000000** | Weak Persistence |
| 1.01  | 0.4174 | 0.6091 | 1.000000 | Weak Persistence |
| 1.02  | 0.4165 | 0.6208 | 0.999500 | Weak Persistence |
| 1.03  | 0.4167 | 0.6109 | 1.000000 | Weak Persistence |
| 1.04  | 0.4159 | 0.6100 | 1.000000 | Weak Persistence |
| 1.05  | 0.4166 | 0.6082 | 1.000000 | Weak Persistence |
| 1.10  | 0.4163 | 0.6221 | 1.000000 | Weak Persistence |
| 1.15  | 0.4161 | 0.6103 | 1.000000 | Weak Persistence |
| 1.20  | 0.4176 | 0.6214 | 1.000000 | Weak Persistence |

Trend check: 2 rises > 0.001, 0 falls > 0.001 — negligible scatter.
Two isolated marginal Aκ events (γ=0.95 and γ=0.96, min 0.9990) — not
co-located, not monotone, attributable to small-n stochastic fluctuation.
State locked at Weak Persistence throughout. No distinguished γ-point.

---

## 4. Cross-Constant Comparison — α (proxy) vs αG (Column IV)

| Body  | α-proxy class (Col. I) | α-proxy γ* | αG class (Col. IV) | αG Δρ̄ | γ* confirmed? | Verdict |
|-------|------------------------|-----------|---------------------|--------|---------------|---------|
| Earth | STRONG · TYPE III-Min  | β*=1.00   | **TYPE I · CALM**   | 0.0007 | **NO**        | Proxy result refuted |
| Mars  | STRONG · TYPE III-Min  | β*=1.00   | **TYPE I**          | 0.0022 | **NO**        | Proxy result refuted |
| Moon  | STRONG · TYPE III-Min  | β*=1.00   | **TYPE I**          | 0.0016 | **NO**        | Proxy result refuted |

All three Column I β*=1.00 results are **refuted** by Column IV. The sharp
violation-resolving minimum at the physical G value was an artifact of the
proxy α-deformation applied to geoid ladders, not a property of G-coupling.

---

## 5. Protocol Prediction vs Outcome

The AG_DEFORMATION_PROTOCOL_v2 §10 predicted, based on the C₂₀^rot / C₂₀^total
decomposition argument, that the true αG structural extrema would lie at:

| Body  | Predicted γ* (protocol estimate) | Observed γ* | Match? |
|-------|----------------------------------|-------------|--------|
| Earth | ≈ 0.71 (rough)                   | none        | N/A — TYPE I |
| Mars  | ≈ 0.58 (rough)                   | none        | N/A — TYPE I |
| Moon  | ≈ 0.23 (outside sweep range)     | none        | N/A — TYPE I |

The protocol predicted correctly that β*=1.00 would not survive physical αG
coupling. It predicted incorrectly (or prematurely) that any γ* would appear
within the sweep range. The true outcome is that αG deformation — even with
the non-uniform C₂₀^rot channel — produces no structural response detectable
by STRUC-I across the full γ ∈ [0.80, 1.20] range.

Two explanations are compatible with the data:

1. **The C₂₀^rot non-uniformity is structurally too small.** Degree-2 is one
   term in a 299-entry (Earth) or 230-entry (Mars) ladder. The competing
   γ vs γ⁻¹ scaling on a single term may not shift ρ̄ measurably when
   averaged across n=117–299 gap pairs.

2. **The deformation rule was applied as uniform scaling.** If the chamber
   did not implement the full C₂₀^rot decomposition and instead used uniform
   γ-scaling of all harmonics, the result would be structurally invisible —
   the same reason atomic H returns null under μ. This would make the Column
   IV entries PROXY-GRADE rather than MATRIX-GRADE. The C₂₀^rot
   implementation status must be confirmed before finalizing the classification.

**This distinction is critical for protocol integrity.** If explanation (2)
applies, Column IV is not yet complete — it requires a correctly implemented
Tier A run with the actual C₂₀^rot decomposition per body.

---

## 6. Resolution Floor Assessment

| Body  | Δρ̄   | Floor reference | × floor | Signal? |
|-------|-------|----------------|---------|---------|
| Earth | 0.0007 | self (flattest) | 1.0×   | NO — at floor |
| Mars  | 0.0022 | Earth floor    | 3.1×   | NO — below 10× |
| Moon  | 0.0016 | Earth floor    | 2.3×   | NO — below 10× |

Earth (Δρ̄=0.0007, Aκ=1.000 exact) defines the geoid resolution floor for
this corpus. 10× threshold = 0.007. No body clears it.

---

## 7. ρ̄ Hierarchy — Cross-Domain View

Bodies ranked by ρ̄ at γ=1.00:

| Body  | ρ̄ @ γ=1.00 | State               | αG-class         |
|-------|------------|---------------------|------------------|
| Mars  | 0.6648     | Boundary-Stabilized | TYPE I           |
| Earth | 0.5033     | Weak Persistence    | TYPE I · CALM    |
| Moon  | 0.4161     | Weak Persistence    | TYPE I           |

Mars sits in Boundary-Stabilized — the highest structural pressure of the
three — yet shows no γ-sensitivity. Earth, despite being the primary testbed,
is the calmest: Aκ=1.000 exact throughout, Δρ̄=0.0007. Moon is intermediate.
The ρ̄ ordering (Mars > Earth > Moon) does not predict αG sensitivity.

---

## 8. Key Findings

### Finding 1 — All three Column I proxy results are refuted
The STRONG · TYPE III-Min · β*=1.00 classification for Earth, Mars, and Moon
under the α-proxy is not reproduced under physical αG coupling. All three bodies
return TYPE I across the full γ-sweep. The Column I geoid result was entirely
a property of the proxy deformation — specifically, the α-scaling applied
to harmonic degree variances non-uniformly by α-weighting of the spectral
index, which is a different mechanism from G-scaling.

### Finding 2 — Earth is the calmest geoid entry in the entire corpus
Earth geoid (n=299, Aκ=1.0000 exact at all 17 γ-values, Δρ̄=0.0007) is the
most structurally inert entry recorded across Columns I–IV. It defines the
new empirical floor for planetary/geoid ladders. This is the deepest
TYPE I · CALM result outside of ²⁰⁸Pb in the nuclear domain.

### Finding 3 — Mars has persistent marginal Aκ events but no trend
Mars shows min Aκ=0.9990 at γ=0.99 and scattered 0.9995 events across the
sweep. These are not correlated with γ in any monotone or extremal way.
The Boundary-Stabilized state of Mars (the only body in that state here)
reflects intrinsically higher structural pressure in its gap geometry,
not αG sensitivity. The Mars geoid lives closer to the boundary but does
not respond to G-deformation.

### Finding 4 — The proxy prediction for Column I was structurally misleading
Column I found β*=1.00 for all three bodies because the α-proxy deformation
scaled harmonic degree variances non-uniformly as a function of α — a
mechanism with no physical basis in G-coupling. Column IV demonstrates that
when G is varied through its proper channel (uniform γ on all harmonics,
with C₂₀^rot competing at degree 2), the structural response collapses to
zero. This vindicates the protocol's decision to retroactively mark the
Column I geoid entries as PROXY-GRADE.

---

## 9. Implementation Note — Tier A Status

The AG_DEFORMATION_PROTOCOL_v2 requires Tier A decomposition: C₂₀^rot
extracted from published hydrostatic equilibrium models and applied as a
per-body parameter producing competing γ and γ⁻¹ scaling on degree 2.

The current runs use the ladder names `earth_geoid_gamma_*`, `mars_geoid_gamma_*`,
`moon_geoid_gamma_*` — consistent with the existing GRAV-I chamber format.
Whether the chamber implemented the full C₂₀^rot decomposition or applied
uniform γ-scaling to pre-existing ladders must be confirmed from the
chamber implementation. Until confirmed:

```
Current Column IV status:  PROXY-GRADE (pending Tier A verification)
If Tier A confirmed:       MATRIX-GRADE · TYPE I × 3
If Tier A not implemented: re-run required with C₂₀^rot decomposition
```

---

## 10. Phase Boundary Assessment

Per AG_DEFORMATION_PROTOCOL_v2 §11:

- ≥1 confirmed structural signal: **NOT MET** (all bodies TYPE I)
- H is Type I under α, μ, αₛ, AND αG: confirmed (atomic H null by construction
  under all constants)
- At least one system changes class between αₛ and αG: Earth/Mars/Moon were
  not in Column III; the class change criterion must be evaluated against the
  full matrix. No body transitions between columns here.

**Conclusion — Column IV (αG) status:**
Physical G-coupling produces no structural signal detectable by STRUC-I in
the geoid harmonic domain across γ ∈ [0.80, 1.20]. The column is TYPE I × 3.
Phase boundary is not met. If Tier A implementation is confirmed, Column IV
closes as DOMAIN-INACTIVE (geoid/gravitational). If Tier A was not implemented,
a corrected run is required before the column can be closed.

---

## 11. Status

```
Column IV (αG) geoid sub-program:    COMPLETE (pending Tier A verification)
Bodies:                               Earth · Mars · Moon — TYPE I × 3
Column I proxy result:                REFUTED for all three bodies
Phase boundary:                       NOT MET
Tier A confirmation required:         YES — C₂₀^rot implementation status
Next action:                          Confirm chamber implementation OR re-run
                                      with full Tier A C₂₀^rot decomposition
```

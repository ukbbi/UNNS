# FIELD-I v002 — Results (Intrinsic Relational Selection)

Run: `python field2.py` — exit 0, ALL PASS, 0 FAIL (output/field2_output.txt). Box X0=3000 (independent construction, 18,566 values, 561 fibres with R>=2, 1,658 pairs); corpus a<=8000, b<=30 (1,116 fibres with R>=2, R<=11). v001, manuscript v3, SELECT-I/II untouched.

## Verdict on the decisive question
**The fixed-nest rule does not determine how structures interact. Interaction must be an explicit component of the grammar.** Two separate reasons, both proved:
1. **Non-selection (T12).** A1–A4 (domain = equal-value pairs, symmetry, result in the common future, stationarity) admit result x + j·Δ with any j ≥ 1 (even pair-dependent j). Competing operations ⋆₁, ⋆₂, ⋆₃, j = 1+(min N mod 2) all satisfy A1–A4 and differ on every pair. Minimality (A7) selects ⋆₁ but is an added axiom, not a consequence.
2. **Incompatibility (T15).** Stationarity (A4) and label-blindness (A6) cannot hold together with A3: a prime-power argument shows the forced gap would be divisible by p² for infinitely many primes. So a grammar must give up one of them.

## Regimes (F7)
| Regime | What it recovers | Status |
|---|---|---|
| A value only | nothing: Π acts transitively on pairs of a fibre | proved (T11), checked |
| B (x, successor) | exactly (M,N); (Occ,v,route) is rigid — "relational" = label | proved (T10), checked |
| C H(x) / G(x) | label-blind; for interaction only γ = gcd H(x) matters (T13) | proved |
| D (x, Δ_rs) | pair identified within its fibre in 820/4130 = 19.9% of cases | data |
Rendezvous graph G(x): rigid (trivial automorphism group) in 100/1116 fibres overall (8.9%); R=2: 0/488, R=3: 0/465, R≥4: 100/163. In a rigid fibre, label-blind structure individuates every route, i.e. it is label information again; in R=2 (and in all observed R=3) fibres the two/three routes are structurally indistinguishable. H(x) vs G(x): no two fibres with R ≤ 6 share H but have non-isomorphic G (data).

## F6 spectrum (what H adds)
- Pair index h = x/Δ is always a positive integer (T7); every positive integer occurs (T9, x = 36h with d = 2,3).
- Collective index γ = gcd H (T8c); collective rendezvous = x(1+1/γ) ≤ 2x; equals 2x in 88/1116 corpus fibres. Coherence: Δ_coll = lattice-lcm of pairwise Δ (T8b). Observed γ in corpus misses 16, 25, 27, 32, 36 (open: which γ occur).
- Classification ladder: 9 R-classes < 553 (R,γ)-classes < 730 H-classes < 1,116 distinct x; 146 spectra shared by ≥2 values (largest class 32). H is arithmetic classification of x, not an independent measurement: it is computed from the whole fibre.

## F8 operation matrix (A2 symmetric, A3 common future, A4 stationary, A6 label-blind, A7 minimal)
| operation | A2 | A3 | A4 | A6 | A7 |
|---|---|---|---|---|---|
| ⋆₁ x+Δ | P | P | P | F | P |
| ⋆₂, ⋆₃, x+L², j=1+(min N mod 2) | P | P | P | F | F |
| j=1+((M+M′) mod 2) (adversarial) | P | P | **F** | F | F |
| Y₁ = x+Δ_coll = x(1+1/γ) | P | P | **F** | P | F per pair |
| Y₂ = x+2Δ_coll | P | P | **F** | P | F |
Occurrence-valued label-blind operations: none (T14, F8.3: R(y) ≥ 2 in all 4,974 cases). Obstruction instances for T15 verified for x = 81, 81/2, 36, 2025/2. Concrete stationarity failure of Y₁: x = 36, pair (2,3), shift 3Δ reaches 144, Δ_coll jumps 36 → 144.
Join on rational fibres (b>1): exists in 335/363 pairs, absent in 28 (first 400/3, {4,10}); no pair with several incomparable minimal upper bounds. Integer fibres: join-semilattice (all cases).

## Corrections to v001 (record only; v001 not edited)
- T4: gcd(d,d′) ∈ D iff gcd ≥ 2 and gcd ≡ 1 (mod b); example 784/3, D = {4,7,28}.
- F5.1 is now a theorem (T6), with integrality (T7) and a collective version (T8).

## What additional grammar is required (consequence of the nonselection theorem)
(G1) a selection rule for j (e.g. minimality, adopted as an axiom); (G2) a choice between route-aware stationary interaction ⋆₁ (uses labels) and label-blind collective Y₁ = x(1+1/γ) (non-stationary); (G3) if the result must be an occurrence (to iterate or compose operations), an explicit output-selection rule, since no equivariant one exists.

## Open
Which γ occur; a weaker stationarity compatible with A6; growth of the rigid fraction; why R=3 fibres are never rigid in the data.
Manuscript v3: no revision warranted. No physical or entanglement claim.

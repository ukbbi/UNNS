# HD-0 — Connecting maps and proof obligations

Spec: GEO_HD_1_SPEC_v003. Atlas: `results/E1/E1_ATLAS.json` (verifier: `src/atlas/verify_atlas.py`).
Scope of the SELECT-II part: integer states (b = 1). Status words: INHERITED (cited source), PROVED-ELEMENTARY (proved here, short), FINITE (checked on the atlas states only), OPEN.

## 1. Typed sets
V = positive integers (values). O = {(N,M,t): M(N+1)²/N = t} (occurrences). E = {m →_N t} (SELECT-II edges). Hist(t) = complete histories of t (source-rooted paths, Vol. I Def. 6.1). D(t) = {d ≥ 2 : d² | t}. F_t = fibre in exponent coordinates (b = 1: lattice points of the box [0,q]\{0}, q_p = ⌊v_p(t)/2⌋).

## 2. Maps already defined and sourced
| id | map | domain → codomain | property | status |
|---|---|---|---|---|
| pi | (N,M,t) ↦ t | O → V | fibres are O_t | INHERITED (Vol. I Thm 1.2) |
| idx | (N,M,t) ↦ d = N+1 | O_t → D(t) | bijection | INHERITED (F.T1) |
| coord | d ↦ (v_p(d))_p | D(t) → Z^k≥0 | bijection onto F_t for b = 1 | INHERITED (GEO-I v002 §1) |
| edge | (N,M,t) ↦ (M →_N t) | O_t → E_in(t) | bijection | INHERITED (S2.5, Vol. I Thm 5.3) |
| lab | (M →_N t) ↦ N | E → N>0 | N = M/gcd(M,t) | INHERITED (S2.3) |
| eps | path ↦ last state | Hist(t) → {t} | — | INHERITED (Def. 6.1) |
| last | history ↦ its last edge's occurrence | Hist(t) → O_t, t non-source | surjective; not injective (72: 4 → 3) | DEFINITION + FINITE (surjectivity is clear: any edge extends to a source-rooted path; non-injectivity witnessed at 72) |
| valexp | m ↦ (v_p(m))_p | V → ⊕_p Z≥0 | injective | INHERITED (unique factorisation) |

## 3. Connecting maps proposed by HD-0 (the obligations)
**M1 (edge transport, partial).** For an edge e = (m →_N t), T_e : F_m ⇀ F_t is the partial map on coordinates (identity on exponent vectors in the common ambient ⊕_p Z≥0), defined on F_m ∩ F_t = F_g, g = gcd(s(m), s(t)). Obligations:
- O1 well-defined: domain/codomain are subsets of ⊕_p Z≥0, hence comparable. PROVED-ELEMENTARY.
- O2 domain: F_g = divisors ≥2 of g; size τ(g) − 1. PROVED-ELEMENTARY (s(m) = g·c(m,N), s(t) = g(N+1), spec §11).
- O3 injective on its domain (it is the identity). PROVED-ELEMENTARY.
- O4 total iff c(m,N) = 1, in which case D(m) ⊆ D(t); a total T_e is an inclusion of boxes, so cells of F_m map to cells of F_t (unit faces of a smaller box avoiding 0 are unit faces of the larger box). PROVED-ELEMENTARY for b = 1 only.
- O5 never onto: every edge gains an index (s(t) ∈ D(t) \ D(m)). PROVED-ELEMENTARY.

**M2 (confluence compatibility).** For two edges e, e' into the same t the images dom/codomain subsets of F_t are F_{g(e)}, F_{g(e')}. Obligation: describe their intersection and union in F_t (both lower boxes: intersection = F_{gcd(g,g')}). PROVED-ELEMENTARY at the set level; any statement beyond it (e.g. an invariant of the pair of boxes versus the double-confluence pattern 96/27 → 432, 784) is OPEN.

**M3 (history transport).** For h = (m0 → … → t), T_h = composite of the T_e. Obligation: composition of partial inclusions is the partial inclusion on the intersection of the g's along the path. PROVED-ELEMENTARY. Whether different histories with equal endpoint have different T_h (a "holonomy" invariant) is OPEN and not asserted; it is the only place a new theorem could arise (HD-HIST-02).

**M4 (cross-scope, FIELD-I).** C : x ↦ x + L²/G gives D(x) ⊆ D(C(x)) (F.T31) i.e. a *total* inclusion F_x → F_{C(x)} on rationals (b may be > 1: coordinates then satisfy a character condition). Obligations: (a) the SELECT-II and C scopes are different operators (NI-6: C(72) = 108 is not an out-neighbour of 72); (b) a map relating the two must be declared explicitly, none is assumed; (c) b > 1 requires the lattice Λ_b, not Z^k. OPEN as geometry (spec HD-T2/T4).

## 4. Non-identifications (witnessed in the atlas, NI-1…NI-8)
value ≠ occurrence (72: 1 value, 3 occurrences) · occurrence ≠ history (O(2,16,72) has 2 histories) · history not determined by (source, endpoint, length) (1-4-16-72 vs 1-4-18-72 differ in the middle state) · history not determined by the label sequence alone (1-4, 2-8, 3-12, 5-20) · equal fibres ≠ equal values (72, 108 both have index set {2,3,6}) · C-step ≠ SELECT-II edge · finite-prime projection can be non-injective on states · SELECT-II edges and Graver moves have different vertex types.

## 5. Duplication check of candidate theorems
See `SOURCE_OVERLAP_MATRIX.tsv`. Summary: HD-TR-01…05 NEW_CANDIDATE but elementary valuation arithmetic (no priority claim); HD-TR-03 a variant of S2.3; HD-CNT-01 duplicates GEO-I v004 §1.5 (k = 2) and v002 Prop 2; HD-HIST-01, HD-ATLAS-02/03 duplicate S2.12/C4/S2.13; the 3750 merge is a finite bounded observation beyond frozen C7; HD-CELL-01 (k ≥ 3 coverage) and HD-HIST-02 are the open targets.

## 6. Honest limits
Everything in §3 marked PROVED-ELEMENTARY is a short argument from the valuation identity, re-checked on the 62 atlas edges by `verify_atlas.py`; none is a deep result. The proposed global atlas is a well-defined bookkeeping of inherited maps plus the partial transport maps above; it yields no new law by itself.

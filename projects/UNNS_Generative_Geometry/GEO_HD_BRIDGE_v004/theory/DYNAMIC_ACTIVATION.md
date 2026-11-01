# A4-T3 — dynamic activation criterion

Setting: `C(x)=x+L²/G` with `D(x)={d≥2: d²|a, d≡1 (b)}`, `L=lcm D`, `G=gcd{d−1}` (frozen FIELD-I map). No rational SELECT-II is used.

## Lemma M — monotonicity (PROVED)
`D(x)⊆D(C(x))` for every state with `D≠∅`. *Proof.* All `d∈D` satisfy `d≡1 (G)`, and `b | G`; write `G=bh`. Then `C(x)=(ah+L²)/G`. Each `d∈D` divides `L` and `d²|a`, so `d²|ah+L²`; `gcd(d,G)=1` so `d²` survives reduction; the reduced denominator `b'` divides `G` and `d≡1 (G)` gives `d≡1 (b')`. ∎ (Z2: 840 steps, 0 violations.)
**Corollary (persistence, A4-T4).** `E_g(x)⊆E_g(C(x))`: a realised relation never becomes dormant along an orbit; each relation has an activity interval `[n_g,∞)`.
**Corollary (what activation needs).** `E_g` can only gain pairs `(u,v)` with `u` or `v` in `D(C(x))∖D(x)`: every activation (or creation-realisation) event is a **D-event** (a growth of the occurrence set).

## Lemma P — progression (PROVED)
From `x=P²/ℓ` (so `D={P}`, `L=P`, `G=P−1=ℓm`), the orbit is `x_j=P²(m+j)/(ℓm)` as long as `D(x_j)={P}`; `P∈D(x_j)` always (`P≡1 (ℓm)`). The first state with `D≠{P}` lies on this progression, at `u=m+j`.

## Theorem T3-N — necessary conditions (PROVED)
If `y=(Pq)²/ℓ` is on the C-orbit of `x`, then
1. every state `z` of the orbit before `y` has `D(z)⊆D(y)={P}∪{p_iq}` (Lemma M);
2. hence at the first event `u` (on the progression, `u<q²m`) the new elements are of the form `p_iq`, which requires `q² | u/gcd(u,ℓm)` and `p_iq ≡ 1 (b)` with `b=ℓm/gcd(u,ℓm)`;
3. in particular the progression cannot run to `u=ℓm`: there the state is the integer `P²` and `D(P²)∋p_i∉D(y)`.
Conversely **any** event adding an element outside `D(y)` blocks `y` forever (**blocking criterion**).
Verified on every reached instance (Z4: 40 first events satisfy 2.). The initial guess "q²>ℓ ⇒ y unreachable" is **false**: ℓ=3, q=2 (`q²=4>3`) is reached (see below).

## Dynamical activation exists (FINITE-EXACT)
Reachability table `results/REACHABILITY.json` (993 instances; ℓ=3 with q∈{2,5,11,17,23,29}, ℓ=5,7 (k=2), ℓ=7 (k=3,q=2)): **REACHED 40, BLOCKED 929, UNRESOLVED 24 (step cap), OVERSHOT 0, D-empty 0.** Reached examples (actual C-orbits):
* `3025/3 → 12100/3` (p=(5,11), q=2) in 8 steps; first event at step 6 (state `12100/9`, adds 10); `e_5−e_{11}`: dormant at x (b=3), absent at b=9, active at y; `β₁ 0→1`.
* `p=(11,23), q=2`: 17 steps; `p=(41,107)` and `(53,71)` with **q=5**: 704 and 182 steps.
* `k=3, ℓ=7, p=(11,53,67), q=2`: 375 steps although the progression would need 16 740; after the first event (step 372, adds `2·53`) the larger `L²/G` lands exactly on `y`; `β₁` 0→3.
So members of the A4 family **are** connected by actual collective steps; the numerical multiplier `q²` is not the mechanism — the mechanism is *a D-event whose new elements lie in D(y)* followed by an exact landing.

## Step-level activation also occurs without excursion (FINITE-EXACT)
ℓ=5 tower `126²/5` (b=5 throughout): at 5→6, `D` gains 56 and 6 dormant relations become realised, `β₁ 1→4`; at 8→9 two more. ℓ=29 (`1890²/29`, G=29, `(P,ρ²)=(35,900)`): at 23→24 `D` gains 175; 2 of 4 new relations were primitive one step earlier; `β₁ 0→1`.

## Criterion (statement)
For `z=C(w)`: `g` is *dynamically activated* iff `g∈Gr(w)`, `g=e(v)−e(u)` with `u,v∈D(z)`, `{u,v}∩(D(z)∖D(w))≠∅` and no pair of `D(w)` realises it. The arithmetic content is the **D-event law** (v003 R3-T5b: in class `G=b`, first event of a stage at `t=u*²`; here the first-event conditions of T3-N.2 for the family). 

## OPEN (not proved)
(a) Are there infinitely many reached members (positive density among Dirichlet choices)? (b) Is "never blocked ⇒ reached" (no overshoot) true — 0 overshoots in 969 resolved rows, no proof. (c) Closed form for the first event position in the family.

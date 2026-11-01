# GEO_HD_BRIDGE v005 — theorem register
Decisive target (user-set): **A5-T3 and A5-T4** (arithmetic criterion for creation/loss of realised moves; predictive homology update), supported by **A5-T2** (exact first-event law); collective towers as infinite-family test ground.
Verification is by the independent verifier `src/verify_v005.py` (shards Z0–Z9). "FINITE-EXACT" statements are never extrapolated.

| ID | Statement | Status | Where | Audit |
|---|---|---|---|---|
| A5-T2.1 | Stage sieve: d∈D(Y_j/G) ⇔ Q(d)\|Y_j | PROVED | FIRST_EVENT | Z1 |
| A5-T2.2 | First event = least j solving one linear congruence per candidate; new set = {Q(d)\|Y_τ} | PROVED | FIRST_EVENT | Z2 |
| A5-T2.3 | τ_D finite for every D≠∅; \|D_n\|→∞ along every FIELD-I orbit | PROVED | FIRST_EVENT | — |
| A5-T2.4 | Activation family: candidate p_iq joins at u ≡ 0 mod lcm(r_i, q^{2+v_q(P−1)}) | PROVED + FINITE-EXACT | FIRST_EVENT | Z2 |
| A5-T3.1 | Divisor-interval edge rule; K_move(x) is a function of D(x) alone (b enters only through D) | PROVED (rule); K(D)=frozen K_move FINITE-EXACT (1,783 states) | MOVE_TRANSITIONS | Z3 |
| A5-T3.2 | Transition law: non-edges persist; old edge dies ⇔ a new occurrence lies in its divisor interval; new edges/cells contain a new vertex; K°=K∩K′ | PROVED | MOVE_TRANSITIONS | Z4 (2,576 events) |
| A5-T3.3 | Event localisation from old complex + stage congruence data | PROVED | MOVE_TRANSITIONS | Z4 |
| A5-T4.1 | Zig-zag identity Δβ_i=(h′_i−h_i)+(r′_i−r_i)+(r′_{i−1}−r_{i−1}); Δχ local | PROVED | HOMOLOGY_UPDATES | Z4 |
| A5-T4.2 | Δβ_i<0 ⇒ dead i-cell or new (i+1)-cell; Δβ_i>0 ⇒ new i-cell or dead (i+1)-cell | PROVED | HOMOLOGY_UPDATES | Z4 |
| A5-T4.3 | Nested events (Dead=∅): Δβ_i = h_i(K′,K) − k_i − k_{i−1} | PROVED | HOMOLOGY_UPDATES | — |
| A5-T4.4 | Exact graph-level predictor without rebuilding K(D′) (also reproduces β₁=k(k−1)/2 of the A4 family) | PROVED + FINITE-EXACT | HOMOLOGY_UPDATES | Z5 |
| A5-T5.1 | Towers are height filtrations; K_k induced subcomplex of K_{k′}; Dead=∅ on all tower steps | PROVED | TOWERS | Z7 |
| A5-T5.2 | Tower moves stabilise: Graver ℓ₁ ≤ \|⟨p_i⟩\| ≤ φ(m) | PROVED | TOWERS | Z7 |
| A5-T5.3 | Eventual quasi-polynomial Betti laws (degree ≤1, period \| ord_m ρ) | PROVED-SCOPED (qualitative; threshold k₁ uncontrolled) | TOWERS | — |
| A5-T6 | Tower laws G=11: β₁=8 (k≥2), β₂=17 (k≥6), β₃(k+5)=β₃(k)+9 (k≥8); G=5: (1,6,5,0) for 7≤k≤140 | FINITE-EXACT to k≤140 (not extrapolated) | TOWERS | Z7 |
| A5-T7 | Type I never occurs among D-events (a vertex is added); census 1,787 V / 603 II / 172 III / 14 IV | PROVED (structure) + FINITE-EXACT (census) | HOMOLOGY_UPDATES | Z4 |
| A5-T1.1 | Proper-divisor obstruction (sufficient for BLOCKED) | PROVED | REACHABILITY | Z6 |
| A5-T1.2 | Exact stage-jumping decider; 24 capped cases → 22 BLOCKED + 2 REACHED | FINITE-EXACT | REACHABILITY | Z6 |
| A5-T1.3 | Family scans k=2 (ℓ=3: 1,131 reached; ℓ=5: 1 reached) | FINITE-EXACT | REACHABILITY | Z6 |

Not attempted in this release: A5-T8, A5-T9.

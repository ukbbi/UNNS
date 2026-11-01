# G2-E/F — Event correspondence between collective and generative histories

**Levels** (never merged): L1 numerical (same endpoints); L2 net structural (same net `D`-change); L3 event (same sequence of `σ`-changes, no more, no fewer); L4 geometric (same sequence of box records); L5 dynamical (a conjugacy of the two systems).

## B2-T9 (σ-transport, SELECT-II saturation) — PROVED
Along an edge `m --N--> m'` the square-root content transports as `σ' = σ(N+1)/c`, `c=∏_{p|N}p^{l_p}`, `l_p=⌊n/2⌋` or `⌈n/2⌉ ≤ n=v_p(N)`, hence `c ≤ N < N+1`. So `σ'/σ=(N+1)/c>1` **on every SELECT-II edge**, and `D(m)⊊D(m')` (σ' is a proper multiple of σ in the rational sense). Checked on 24 496 edges (`m≤3000`): 0 edges with unchanged `D`. Every generative step is an event; the generative system has **no silent step**. ∎ (the divisibility `σ|σ'` is used only as `D` inclusion where σ' is an integer multiple; the strict inequality is what is proved in general).

## B2-T10 (rigid event correspondence, Level 3) — PROVED
From `x=σ²t`, `t∈{1,2,3}`, σ even: `C³(x)=4x=T₁(x)` and the reduced σ-sequence of the collective orbit is `(σ, 2σ)` exactly as for the single SELECT-II edge `N=1`. Both have one birth event (birth count `τ(odd σ)` new indices), and equal event records (`rigid_phase_record`, all σ checked). The tower `4^k→2·4^k→3·4^k→4^{k+1}` is the case `σ=2^k`.  **Level 3 holds; Level 4 holds for integers by B2-T1 (the box record is a function of σ); Level 5 is not available.**

## B2-T11 (birth-endpoint classification) — PROVED for birth endpoints, FINITE-EXACT in general
For regime-I iterates `x_n, x_m` (j births between): `x_n ⇝ x_m` by a SELECT-II history with matching reduced σ-sequence **iff** `x_m = 4^j x_n` (⇔ `t_n=1`) — when `x_m` is a birth endpoint. Over 16 028 pairs (56 starts) the equivalence "event-matched ⇔ `x_m=4^j x_n`" has **0 violations**; the table of counts by (j, reachable, event-equivalent) is in `results/EVENT_CORRESPONDENCE.json`. Reachability without event match is common (e.g. j=2: 636 pairs): same endpoints (Level 1) but different event resolution.

## B2-T12 (coincidence family) — PROVED family, FINITE-EXACT scan
For `N=2^a−1` squarefree and `s` even: `x=Ns²`, `C^k(x)=T_N(x)=(2^a s)²` with `k = k(a)` collective steps and `1+⌈a/2⌉`-type event growth (table in `results/SINGLE_EDGE_COINCIDENCES.json`, a=2…) against exactly **one** SELECT-II event. Scan `x<4000`: all single-edge coincidences have `N+1 ∈ {2^a, 3·2^a}` (12 values `2…512`) — **completeness is OPEN (O2-2)**.

## B2-T13 (scaling obstruction) — PROVED
If `C^P(x)=ρ²x` and `ρ²=R(N)=(N+1)²/N` for one edge, then `N | (N+1)²` ⇒ `N=1`. So a single SELECT-II edge is a non-trivial integer scaling only for `N=1`, `ρ²=4`; In particular the G=11 scaling `x_{n+8}=9x_n` (`ρ²=9`) is unreachable by any single edge (`R(N)=9` ⇔ `N²−7N+1=0`, no integer root) and by any history (two or more edges multiply to ≥16, one edge gives 9 or not at all). For other `ρ` (≤12) histories exist for ρ=2,4,5,8,9,10 and none were found for 3,6,7,11,12 (`square_multiplier_rho`).

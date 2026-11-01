# G2-B — Geometry of recombination (rewriting histories)

A *content* is a multiset of labels `N`; an *arrangement* is an order in which the edges `m --N--> m(N+1)^2/N` are all admissible (`N | current state`). Recombination = replacing a block of labels `u` by another block `v` with the same net endpoint.

## B2-T3 (rewrite law) — PROVED
Let `H_p(u)=` total of `v_p` over labels of `u` (the *denominator content*), `G_p(u)=sum v_p(N+1)`. The multiplier of a history is `∏ (N+1)^2/N`, so equal endpoints force `2G_p(u) − H_p(u) = 2G_p(v) − H_p(v)` for all `p`. With the balance `Delta q_p = G_p − Lambda_p`:

    Lambda_p(u) − Lambda_p(v) = ½ (H_p(u) − H_p(v))      (equal endpoints, both blocks admissible from the same state).

So **recombination moves loss budget in exactly the amount that the denominator content changes**; the geometry of the route (how many axes shrink and when) is governed by `H`, not by the order. Example `(2,2,3,3,3,3) → (1^6)` (up to the endpoint-neutral padding checked): `H` differs by `(2:2, 3:4)`, so `Lambda` differs by `(2:1, 3:2)` — matches `results/REWRITE_LAWS.json` (4 block rewrites, 20–39 admissible sources each, 0 failures).

## B2-T4 (parity conservation) — PROVED under restriction `v_p(N) <= 1`
If every label has `v_p(N)<=1`, a loss step for `p` happens iff `v_p(m)` is odd at an edge with `p|N`, and `v_p` changes by `2w−1` (odd), so parity of `v_p(m)` flips at every such edge. Along a history the number of loss steps for `p` therefore has the parity fixed by content and endpoints, and orderings can only permute *when* the losses occur. Checked on all arrangements of 122 (content `2,2,3,3,3,3`) and the other tested contents; 0 failures. Outside `v_p(N)<=1` the statement is not claimed.

## B2-T5 (mixed-index forcing) — PROVED for contents `2^α 3^β`
For a content using only labels with `(N, N+1) ∈ {(2,3),(3,4)}` the exponent pair `(v_2,v_3)` moves by `(−1,+2)` for `N=2`, and `(+2,−1)` for `N=3` (sign pattern from `v_p += 2v_p(N+1) − v_p(N)`). Writing the path as a lattice walk, an arrangement is admissible iff it never needs a negative exponent; a *square avoidance* DP (`avoids_square`, `feasible`) decides whether a route can keep `min(q_2,q_3)=0` i.e. avoid ambient dimension 2.
* Result: for contents with at least two labels of each kind and enough starting exponents (family `2^{2n}3^{4n}`, n=1..6) the 2-dimensional ambient geometry is **forced at every admissible arrangement**; the four smallest contents `(1,1,1,0),(1,1,2,0),(1,2,1,0),(1,2,2,0)` are *avoidable*. Brute force over 131 cases: 0 violations of the classification, 0 exceptions (`results/MIXED_INDEX_FORCING.json`).
* Scope: two active primes only. Arbitrary `k` — **OPEN (O2-4)**.

## Benchmark B3: `4 → 65536` two routes
Route A `1^7`: every state `4^j` has `q=(2: j)` — a segment, contractible, `Lambda=0`.  Route B `(2,2,3,3,3,3)` (any admissible order): contractible at every step (T1), but ambient dimension 2 at steps 3–4 and `Lambda=(2:1,3:2)`. Same endpoints, same route-complex component, different loss budget and different dimension profile.  Zero area-bivector potential around a loop (v001) does not make the geometric event sequence trivial: it is invisible to `H`-balanced potentials but visible in `Lambda` and in the `d_aff` profile.

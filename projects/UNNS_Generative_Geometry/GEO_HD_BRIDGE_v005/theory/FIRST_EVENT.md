# A5-T2 — The stage sieve and the exact first-event law

Status labels: PROVED / PROVED-SCOPED / FINITE-EXACT / COUNTEREXAMPLE / OPEN / NOT-TESTED. Only the frozen map `C(x)=x+L²/G`, `D(x)={d≥2 : d²|a, d≡1 (b)}` (x=a/b reduced), `L=lcm D`, `G=gcd{d−1}` is used.

## Setting
Let `x₀=a/b`, `D₀=D(x₀)≠∅`, `L`, `G` as above. Every `d∈D₀` is ≡1 mod b, so `b | G`; write `G=bh`. Every `d∈D₀` is ≡1 mod G and divides L, hence **gcd(L,G)=1**. Put

  `Y_j = a·h + j·L²`,   so   `x₀ + j·L²/G = Y_j / G`   (j ≥ 0).

While `D` stays equal to `D₀`, the frozen orbit is exactly `x_j = Y_j/G` (a *stage*). The formula `Y_j/G` is also used for *virtual* points (j beyond the first event).

## Theorem A5-T2.1 (stage sieve) — PROVED
For every integer `j ≥ 0` and `d ≥ 2`:

  **d ∈ D(Y_j/G)  ⇔  Q(d) | Y_j**,  where  `Q(d) = lcm( r(d) , ∏_{p|d} p^{2·v_p(d)+v_p(G)} )`,  `r(d)=G/gcd(d−1,G)`.

*Proof.* Let `g=gcd(Y_j,G)`; the reduced fraction is `a_j/b_j` with `a_j=Y_j/g`, `b_j=G/g`.
(i) `b_j | d−1` ⇔ `G/g | gcd(d−1,G)` ⇔ `r(d) | g` ⇔ `r(d) | Y_j` (as r(d)|G).
(ii) `d² | a_j` ⇔ `d²·g | Y_j`. For a prime `p|d`, `v=v_p(d)≥1`, `γ=v_p(G)`: `v_p(g)=min(v_p(Y_j),γ)`. If `v_p(Y_j)≤γ` the requirement `v_p(Y_j) ≥ 2v+v_p(Y_j)` is impossible; so `v_p(Y_j)>γ` and the requirement is `v_p(Y_j) ≥ 2v+γ`, which conversely already forces `v_p(Y_j)>γ`. Primes not dividing d impose nothing. Combining (i), (ii): `Q(d) | Y_j`. ∎
(Verified: Z1, brute-force D with an independently coded Q; 216 virtual points / 44 states fast, more in --full; 1140 points in the build-time run.)

## Corollary A5-T2.2 (event law = one linear congruence per candidate) — PROVED
`d∉D₀` joins at the least `j≥1` with **L²·j ≡ −a·h (mod Q(d))**; solvable iff `gcd(L²,Q(d)) | a h` (always when gcd(d,L)=1, since r(d)|G is prime to L). The first-event time and the new occurrence set are

  `τ_D(x₀) = min_{d∉D₀} j(d)`,   `D(x_τ)∖D₀ = {d∉D₀ : Q(d) | Y_τ}`.

No intermediate state and no intermediate complex is constructed. (Z2: first-event time + new indices equal brute-force simulation of the frozen map on all tested orbits; B5-9 control ℓ=29: τ=24, new={175}.) A candidate search is needed only up to `d ≤ isqrt(Y_J)` for a horizon J.

## Corollary A5-T2.3 (events never stop) — PROVED
For every state with `D≠∅`, `τ_D<∞`. *Proof.* Take a prime `p∤G·L` (so `p∉D₀`). `Q(p)=lcm(r(p),p²)`, `gcd(L²,Q(p))=1`, so the congruence is solvable. ∎
Hence along **every** FIELD-I orbit with `D≠∅` the occurrence set `D_n` (monotone by Lemma M) takes infinitely many distinct values and `|D_n|→∞`. (This is a statement about D only; it says nothing about topology.)

## Proposition A5-T2.4 (the activation family, closed form) — PROVED + FINITE-EXACT check
For `x=P²/ℓ` (A4 family: `D={P}`, `L=P`, `G=P−1=ℓm`, `h=m`, `Y_j=P²(m+j)`, `u=m+j`) and a candidate `d=p_i q`:

  `d` joins exactly when **u ≡ 0 (mod lcm( r_i , q^{2+v_q(P−1)} ))**,  `r_i=(P−1)/gcd(p_i q−1, P−1)`  (`r_i | m` since ℓ | p_iq−1).

Consequences: (a) the exponent `2+v_q(P−1)` is why a prime `q | P−1` (e.g. q=2 for odd P) is harder to activate — the valuation of G enters the *square* condition; this is the exact form of the necessary conditions of v004 T3-N.2 (q²|u/gcd(u,ℓm)); (b) the position of the first A4-type event is the least multiple of `M_i` above `m`. Verified against direct membership (Z2, 32 (instance,pᵢ) pairs fast, 292 in the build run, 0 mismatches). *Not claimed:* that no non-A4 candidate occurs earlier — that is exactly the blocking question (OPEN, REACHABILITY.md).

## Why towers have period = multiplier (link to A5-T5/T6)
For `x₀=S²/m` with `L=S`, `G=m`, `b=m`, `h=1`: `Y_j=S²(1+j)`. A new divisor `d=μ'·e` (extra factor of a prime ρ) needs `ρ^{2(v_ρ(S)+1)} | S²(1+j)`, i.e. `ρ² | 1+j`, so the first event of the tower stage is at `1+j=ρ²` — the tower multiplier `μ²`. The period of the tower is the sieve's first-event time (G=11: ρ=3, τ=8, multiplier 9; G=5: ρ=2, τ=3, multiplier 4).

## What this does and does not give
* Gives: an exact, arithmetic, simulation-free event time and new-index set for **every** FIELD-I state (not only the activation family).
* Does not give: a closed form for the *minimum over all candidates* in a family (the minimum over infinitely many congruence classes), nor a classification of which activation-family targets are reached (REACHABILITY.md).

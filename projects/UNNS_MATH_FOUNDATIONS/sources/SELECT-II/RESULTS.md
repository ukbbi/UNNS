# SELECT-II v001 — Mathematical findings and proofs

21 October 2026 — Status: **proved for the declared self-iteration graph** unless marked [checked].

## Definitions

Let vertices be positive integers. An edge `m --N--> t` exists for positive integers `m,N` when

`t = m(N+1)^2/N` is an integer.

Since `gcd(N,(N+1)^2)=1`, the edge condition is exactly `N | m`. Write `m=kN`, then `t=k(N+1)^2`.
Importantly, substituting a previous nest output for the next first argument is a **specific continuation interpretation**. Neither binary joint composition nor the use of these edges as all of UNNS generation follows from the arithmetic alone.

## Theorem A — outgoing edges and monotonicity

For each `m`, there is one different successor for each `N | m`:

`t/m = (N+1)^2/N = N+2+1/N`.

For integers `N>=1` this increases strictly with `N` and is >=4, with equality only at `N=1`.
Thus the graph is acyclic; every edge multiplies the value by at least 4; its outdegree is the ordinary positive-divisor function `tau(m)`.

Also `m | t` iff `N | (N+1)^2`, which by coprimality occurs only when `N=1`.

## Theorem B — incoming edges = nest multiplicity

Every incoming edge into `t` has form

`t=k d^2`, `d=N+1>=2`, `m=k(d-1)`.

Conversely, each `d>=2` with `d^2|t` determines exactly such an edge, and different `d` give different sources because `(d-1)/d^2` is strictly decreasing for integer `d>=2`.
Therefore

`indegree(t) = R(t) = number of d>=2 with d^2|t = product_p(floor(nu_p(t)/2)+1)-1`.

In particular, `indegree(t)=0` exactly when `t` is squarefree. Every predecessor is smaller than its target, so repeatedly choosing any predecessor ends at a squarefree root. A target may have many squarefree ancestors.

**Example:** incoming edges for `72`: `18 --1--> 72`, `16 --2--> 72`, `10 --5--> 72`. Its squarefree ancestors are `1, 3, 10`.

## Theorem C — the direct-edge label is identifiable

For `m=kN`, `t=k(N+1)^2`,

`gcd(m,t)=k`.

Hence from a known positive value pair `(m,t)` the edge can exist only with

`g=gcd(m,t)`, `N=m/g`, `t=g(N+1)^2`.

This is also sufficient, supplying an exact non-factorization-based edge membership test.

## Theorem D — no universal least common future

For value 1 and value 2, there are paths to both 81 and 100:

- `1 --1--> 4 --2--> 18 --2--> 81` and `2 --1--> 8 --8--> 81`.
- `1 --1--> 4 --1--> 16 --4--> 100` and `2 --2--> 9 --9--> 100`.

Exact finite traversal, complete for values <=100 since every edge increases, finds **precisely `{81,100}`** as common reachable values in this interval. There are no smaller common reachable values.

If a least common future `u` existed, it would reach both 81 and 100. Since every nonidentity edge increases by a factor >=4, `u<=81`. The only common reachable candidate <=81 is `u=81`. But `81` cannot reach `100` (any nonidentity successor is at least 324). Contradiction.

Thus the reflexive-transitive closure of these nest-value edges is a strict-growth partial order **without a binary least upper bound for all pairs**.

This is a counterexample to a *universal join in the specified self-iteration order*, not to RGG-2's valid theorem for the distinct, explicitly defined factor-amplification order.

## Computational record

`select2.py` uses only exact integer arithmetic (and `fractions.Fraction` for the integrality test), and passes 23 asserted tests and prints 3 reported data rows. The finite graph statistics and ancestry counts are checked finite-range observations, not asserted as universal formulas.

**Major conceptual result:** nest iteration can define a directed, rooted, merging generative graph without furnishing a uniquely selected binary continuation. To establish a genuine selection mechanism, one must first specify and justify the intended continuation semantics.

## Next investigation within SELECT-II

The next stage is **history-sensitive reachability**: distinguish paths leading to the same value, inspect edge-labelled histories versus endpoint-only reachability, and test whether an independently defined admissibility restriction yields a common continuation on a specified subregime. This remains open and is not claimed solved by v001.

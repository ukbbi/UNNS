# FUG-I v001 theorem and exact-witness register

All statements distinguish **PROVED** general results from **VERIFIED-EXACT** bounded enumeration. The original substrate primitive remains unchanged. Results already present in the archived foundations are identified as such.

## FUG-T1 — Incoming Fibonacci fibre formula [PROVED; inherited]

For `n>=1`, the integer-output occurrence fibre over `F_n` is naturally indexed by

`D_n={d>=2:d^2|F_n}`, with `(M,N)=(F_n(d-1)/d^2,d-1)`.

**Proof.** Set `d=N+1`. The equality `S_N(M)=F_n` gives `M*d^2=F_n(d-1)`. Since `gcd(d^2,d-1)=1`, we have `d^2|F_n` and the displayed unique `M`. The converse follows by direct substitution. This is FIELD-I F1 restricted to positive integer outputs.

## FUG-T2 — Fibonacci index meet and transport [PROVED; inherited]

`D_m ∩ D_n = D_gcd(m,n)` and `m|n => D_m subset D_n`.

**Proof.** Use `gcd(F_m,F_n)=F_gcd(m,n)` and the equivalence `d in D_k <=> d^2|F_k`. If `m|n`, `F_m|F_n`, so the map of occurrences `(M,N)->((F_n/F_m)M,N)` is well-defined, preserves the nest label, and such maps compose along `m|n|r`. This recovers the prior occurrence-geometry result.

## FUG-T3 — No adjacent or next-nearest Fibonacci continuation [PROVED]

For any `n>=1`, no **nonempty forward** SELECT-II path can connect `F_n` to `F_(n+1)` or to `F_(n+2)`.

**Proof.** Every legal move multiplies the state by `N+2+1/N>=4`, so any nonempty directed path has target at least `4 F_n`. But `F_(n+1)<4F_n` and `F_(n+2)<4F_n` for all `n>=1`: for `n>=2`, `F_(n+1) <=2F_n` so `F_(n+2) <=3F_n`; the `n=1` case is direct. Thus neither target is attainable. These obstructions concern the SELECT-II directed grammar, not the original two-input arithmetic or other continuation systems.

## FUG-T4 — Exact finite enumeration criterion [PROVED]

Let `Y>0` and define its full integer-anchor predecessor set

`P(Y)={ (Y(d-1)/d^2, d-1): d>=2, d^2|Y }`.

This is **exactly** the complete set of labelled incoming SELECT-II arrows to `Y`.

For fixed sources `x` and targets `y`, paths of 1, 2 or 3 edges can be exhaustively found by enumerating one or two forward edges from `x` and joining against `P(y)`.

**Proof.** For an incoming edge `T_N(z)=Y`, let `d=N+1`; then `Y=z*d^2/(d-1)`. Coprimality `gcd(d^2,d-1)=1` implies `d^2|Y`, and `z=Y(d-1)/d^2`, necessarily divisible by `N=d-1`. Conversely each listed predecessor gives a valid arrow to `Y`. Any 2- or 3-step path must have its final vertex just before `y` in `P(y)`. All intermediate states are positive and strictly smaller than the endpoint because each forward factor is at least 4. Therefore restricting intermediate states to the largest target in a finite window cannot omit any target-reaching path.

## FUG-C1 — Complete short paths among F_1,...,F_48 [VERIFIED-EXACT]

There are **8 labelled routes** of lengths 1 through 3 between positive ordered index pairs in `[1,48]`:

- Length 1: one route, from `(3,6)`.
- Length 2: four routes, two from `(5,12)` and two from `(6,12)`.
- Length 3: three routes, all from `(3,12)`.

The four indexed endpoint pairs at distance <=3 are `(3,6),(5,12),(6,12),(3,12)`, with minimal distances `1,2,2,3` respectively.

**Certification.** `scripts/fug_i.py` enumerates all possible source divisors, intermediate admissible divisors, and exact target predecessors. `scripts/verify.py` independently enumerates all labelled reverse paths from each target, using a deliberately simple square-divisor oracle. The two sets of paths agree exactly; there is no sampled or floating-point computation. Full route listing is in `results/fib_paths_le3_48.csv`.

## FUG-C2 — Branching and reconvergence witness [VERIFIED-EXACT]

The following routes are legal:

```
F_5=5  --1--> 20 --5--> 144=F_12
F_5=5  --5--> 36 --1--> 144=F_12
F_6=8  --1--> 32 --2--> 144=F_12
F_6=8  --2--> 36 --1--> 144=F_12
```

In particular, `5 --5--> 36 <--2-- 8`: two distinct Fibonacci inputs converge at the same *non-Fibonacci* ambient node, then continue to `F_12=144`. The two route labels and source values are distinct; their common endpoint equality is exact.

There are also three distinct 3-step histories from `F_3=2` to `F_12=144`:

```
2 --1--> 8 --1--> 32 --2--> 144
2 --1--> 8 --2--> 36 --1--> 144
2 --2--> 9 --1--> 36 --1--> 144
```

This is a concrete induced generative geometry under the selected grammar. It does not imply that Fibonacci's recurrence uses these edges.

## FUG-T5 — First appearance and unbounded incoming fibres [PROVED; inherited]

For `z(k)=min{r>=1 : k|F_r}`, the `d`-coordinate appears precisely at indices divisible by `z(d^2)`:

`d in D_n <=> z(d^2)|n`.

Every positive integer `q` has a positive Fibonacci multiple of `q^2`: modulo `q^2`, the Fibonacci recurrence on ordered pairs is invertible and periodic, so some `F_r=0 (mod q^2)`. Every divisor `d>1` of `q` then contributes an incoming occurrence of `F_r`, and `F_r|F_(kr)` for all `k>=1`. By choosing `q` with arbitrarily many divisors, `sup_n R(F_n)=infinity`, with arbitrarily large multiplicity at infinitely many indices.

This theorem is a consequence of classical Fibonacci arithmetic and the original substrate fibre theorem, already articulated in the prior study; it is not newly established by the v001 finite enumeration.

## FUG-O1 — General short-path classification [OPEN]

Classify every pair of Fibonacci indices `i<j` for which a positive SELECT-II path exists (with no length bound), and determine whether there are infinitely many connected pairs or a finite complete exception set. Neither direction is resolved in v001. Even an exact 48-index search to depth 3 cannot decide this question.

## FUG-O2 — Induction beyond selected integer self-substitution [OPEN]

Determine which structures persist when the overlay uses other declared continuation grammars, rational non-anchor occurrences, or a physically justified dynamical correspondence. `T_N` is not the only conceivable way to deploy the founding arithmetic.

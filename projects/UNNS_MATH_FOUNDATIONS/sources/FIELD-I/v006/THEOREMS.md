# FIELD-I v006 — Exact modular collapse and eventual scaling

**Version:** v006. **Model:** positive rational values realised by the original fixed-nest formula, with the *proposed* collective map `C`; all claims about `C` are conditional on G1-C/G2-min/G3-V. Prior versions remain frozen.

Definitions: for reduced `x=a/b>0`, `D(x)={d>=2 : d^2|a, d≡1 (mod b)}`. If `D(x)` is nonempty, put `G=gcd{d-1:d∈D(x)}`, `L=lcm D(x)`, `Δ=L²/G`, `C(x)=x+Δ`. The denominator `b` divides `G`, and `gcd(L,G)=1`; consequently `y=Gx` is an integer and `Δ` is already reduced. By v005 T31, `D(C(x))⊇D(x)` and `G(C(x))|G(x)`. Further, `G=1` iff `x` is an integer divisible by 4 (v005 T30).

## L1 — Modular escape from any fixed fibre (PROVED)

Suppose `G(x)=g>1` and the fibre `D(x)` were kept unchanged under repeated `C` steps, with `L=lcm D(x)`. Then `y_k=g x_k=y_0+kL²`. There is a **positive** integer `k` for which `y_0+kL²≡0 (mod 4g)`, forcing `x_k` to be an integer divisible by 4 and hence `G(x_k)=1`. More precisely:

* **L odd:** `gcd(L²,4g)=1`; the least positive such `k` is the solution of `k≡-y_0(L²)^{-1} (mod 4g)`, with `1≤k≤4g`.
* **L even:** `g` is odd; since an even `d∈D(x)` exists, `4|a` and `4|y_0`. Furthermore `gcd((L/2)²,g)=1`. The least positive `k` solves `k≡-(y_0/4)((L/2)²)^{-1} (mod g)`, with `1≤k≤g`.

**Conclusion:** the actual orbit must acquire at least one additional modulus **no later than** that calculated `k`, because otherwise the hypothetical constant-fibre orbit would reach `G=1`, a contradiction. This is a bound on *fibre growth or collapse*, not a bound on collapse alone. The first-growth time may be much earlier because other square divisors can appear.

## L2 — Universal collapse for G=2,3,6 (PROVED)

These bounds remain valid **even if D grows before collapse**, since all congruence statements hold at every state with the specified G.

**G=2:** all admissible `d` are odd, so `L` is odd and `L²≡1 (mod 8)`. While `G=2`, `y=2x` advances by `+1 (mod 8)`. Initially `y≠0 (mod 8)`, because equality would give `x∈4ℤ` and `G=1`. Since `G` can only drop from 2 to 1, it must reach 1 within **7** steps.

**G=3:** `G` odd requires at least one even `d` (otherwise every `d-1` is even); thus `L` is even and the reduced numerator `a` is divisible by 4. Because `b|3`, `y=3x` is divisible by 4. While `G=3`,

`(y_next/4)-(y/4)=(L/2)²≡1 (mod 3)`,

since `gcd(L,3)=1`. The residue `y/4` starts nonzero modulo 3 (or `x` would already be in `4ℤ`), hence the orbit reaches `G=1` in **at most 2** steps; 3 has no other proper positive divisor.

**G=6:** `d≡1 (mod 6)` forces every admissible `d` to be odd and coprime to 3; hence `L²≡1 (mod 24)`. While G remains 6, `y=6x` advances by `+1 (mod 24)`. Starting residue is nonzero, so without a G reduction the orbit reaches `G=1` within 23 steps. If instead G first drops at step `j≤22`, it becomes 2 or 3, reaching 1 in at most 7 further steps. Thus **G=6 collapses within 29 steps**.

**Exclusions:** a permanently stabilized `G∞` cannot equal 2, 3, or 6. This does **not** establish that all orbits reach 1; other possible values of `G∞>1` remain unresolved.

## L3 — Exact eventual three-step scaling in regime I (PROVED)

For `G=1`, let `x=s²t` with `t` squarefree, `s` even. The v005 recursion is `s' = s*sqrt_part(t+1)`, `t'=sqfree(t+1)`. Every `t` enters the cycle `1→2→3→1` (v005 T32). At and after its entry time `N`:

`x_(n+3)=4*x_n`, `gamma(x_n)=t_n∈{1,2,3}`, `s_(n+3)=2*s_n`.

Put `o=odd_part(s_N)`, constant forever thereafter. Since `R(x)=tau(s)-1`,

`R(x_(n+3))-R(x_n)=tau(o)`.

There is no claim of three-step scaling before the `t`-cycle is entered.

## L4 — Exact reach counting for the G=1 branch (PROVED)

After cycle entry the cumulative reachable-modulus set is

`U={q*2^k : q|o, k>=0, q*2^k>=2}`,

where `o=odd_part(s_N)`. It includes all earlier moduli because `D(x_n)` is monotone. For integer `X>=1`, its counting function is exactly

`U(X)=sum_{q|o, q<=X}(1+floor(log_2(X/q))) - 1`.

The integer floor is exact; subtract one to exclude `d=1`. Hence `U(X)=tau(o)*log_2 X+O(1)` as `X→∞` (with `o` fixed), so the **natural density is zero** for the `G=1` regime.

## L5 — Correction to v005 T33 (SCOPE ERRATUM; v005 preserved)

The first sentence of v005 T33 claims `U(X)=O(log X)` and density 0 for **every** collective orbit. Its proof supplies those conclusions only if the orbit reaches `G=1`. If hypothetical `G∞=g>1` persists, current evidence proves only that `U⊆{d>=2:d≡1 (mod g)}`; this excludes infinitely many moduli and gives **upper asymptotic density ≤1/g**, not zero density or logarithmic reach counting. **The non-universality theorem for all collective orbits remains valid.**

## L6 — Unresolved full collapse theorem (OPEN)

Whether every realised initial value reaches `G=1` remains open. L1 prevents unbounded **unchanged-fibre** plateaus; it does not exclude infinitely many growth events preserving `G`. L2 removes three possible stable G values. Nothing here selects the collective grammar as the unique UNNS interaction or implies physical behavior.

## Verification methodology

`field6.py` uses exact `Fraction` and integer arithmetic with independent fibre reconstruction from factorisation, modular inverses, and actual forward iteration. All PASS rows are computed finite checks of identities whose **general proofs are stated above**. DATA rows are observations; OPEN rows are not encoded as always-passing assertions. Tests do not depend on any older script.

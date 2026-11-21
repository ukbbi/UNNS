# FUG-I v002 — formal scope and induced objects

**Research status:** local Phase 2, separate from frozen FUG-I v001. All paths in this release are exact arithmetic, without a fixed path-length cutoff. The index window remains finite: `1 <= i < j <= 84`.

## S0. Fixed substrate / selected continuation

The original UNNS occurrence law is

`M ⟂ N = M(N+1)^2/N`, for all positive integers `M,N`, with rational output allowed.

Phase 2 studies the separately selected integer-anchor self-substitution grammar

`T_N(x) = (x/N)(N+1)^2`, with `N | x`.

An edge is `x --N--> T_N(x)`. **This does not exhaust the original rational-valued substrate or other possible continuation grammars.** Every forward edge has a growth factor `>=4`.

The independent observation sequence is Fibonacci: `F_0=0, F_1=F_2=1, F_(n+2)=F_(n+1)+F_n`. Indexed observations are retained separately (in particular `F_1` and `F_2` remain distinct).

## S1. Backward ancestral geometry

For `y>=1` define the complete immediate predecessor set

`Pred(y) = {(y(d-1)/d^2, d-1): d >= 2, d^2 | y}`.

A **backward ancestral path** is any finite directed sequence `x_0 --N_1--> ... --N_l--> y` of legal `T_N` moves, of length `l>=0`. Intermediate nodes can be non-Fibonacci. Paths are distinguished by complete label word and state history, not only endpoints.

Define:
- `A(y)` = set of all states lying on a forward path ending at y, including y;
- `H_k(y)` = number of length-k labelled paths ending at y, from any positive integer starting state; `H_0(y)=1`;
- `h(y) = max{k: H_k(y)>0}`;
- `Roots(y) = {r in A(y): Pred(r) is empty}`;
- `FibPaths(i,j)` = all nonempty directed paths from `F_i` to `F_j`.

`Roots(y)` is a set of **squarefree terminal ancestors**, not a claim about physical causality or a new primitive in the substrate.

## S2. Exact finite scope

Only `1 <= i < j <= 84` enter the Fibonacci-to-Fibonacci endpoint census. Crucially, there is **no depth cutoff**: backwards expansion runs all the way to squarefree roots.

`F_84=160500643816367088 < 2^64`; every reverse state is strictly smaller. Factorization uses a fixed-witness deterministic Miller–Rabin test for the 64-bit range, plus Pollard-rho factor splitting and product checks.

A second script counts paths independently without enumerating label words; it also checks the complete reverse closure for Fibonacci targets `n<=60` by naïvely checking every possible `d` through `floor(sqrt(y))`. This is explicitly narrower than the 84-index certificate, but independent of prime-factor routines.

## S3. Controls and limits

Two independent input controls are evaluated under identical methods and index range: Lucas numbers `L_1=1,L_2=3` and shifted Fibonacci `F_n+1`. They are mathematical controls, not statistical null distributions.

The release does not establish a global classification of all Fibonacci index pairs, nor any physical or universal generative hypothesis. The operator `T_N` is one selected grammar for using the original substrate.

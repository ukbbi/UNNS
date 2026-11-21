# FUG-I v002 — Phase 2 theorem and result register

## FUG2-T1. Immediate predecessor criterion [PROVED; inherited substrate arithmetic]

For any `y>0`, its complete set of labelled incoming `T_N` edges is

`Pred(y) = {(y(d-1)/d^2, d-1): d>=2, d^2|y}`.

**Proof.** Put `d=N+1`. From `y=x d^2/(d-1)` and `gcd(d^2,d-1)=1`, infer `d^2|y` and recover `x=y(d-1)/d^2`, necessarily divisible by `N=d-1`. The converse is substitution. This is the square-divisor fibre theorem of FIELD-I/FUG-I v001, now used as a reverse-graph oracle.

## FUG2-T2. Complete reachability by finite backward descent [PROVED; known SELECT-II decidability, specialized here]

Every forward edge multiplies its source by `R(N)=(N+1)^2/N>=4`. Therefore every backward edge decreases a positive integer by at least a factor of four, and every path `x => y` has length at most `floor(log_4(y/x))`. In particular every nonempty ancestral path ending at y has length at most `floor(log_4 y)`.

**Proof.** Multiply the >=4 inequalities along the path. Strict descent ensures that iterating the exact predecessor rule of T1 eventually terminates and enumerates every admissible path, of any length. No depth bound is required for a fixed integer target.

## FUG2-T3. Primitive ancestral roots are exactly squarefree integers [PROVED]

A positive integer `r` has no incoming `T_N` edge iff it is squarefree. Every `y>=1` has at least one finite backward path ending at some squarefree r, and `Roots(y)` is a nonempty finite set.

**Proof.** By T1, an incoming edge exists iff a square `d^2` with `d>=2` divides r, exactly the negation of squarefreeness. By T2 each backward move decreases the positive integer strictly and cannot continue forever. The branching at each node is finite because y has finitely many square divisors.

**Status note.** The squarefree criterion is inherited from the original fibre theorem; the root-set viewpoint is a Phase 2 organization of that existing arithmetic, not a priority claim.

## FUG2-T4. Exact recursion for ancestry multiplicities [PROVED]

Let `H_0(y)=1`. For all `k>=1`,

`H_k(y) = sum_{d>=2, d^2|y} H_(k-1)( y(d-1)/d^2 )`.

Then `H_k(y)=0` for every `k>floor(log_4 y)`. Thus `h(y)` and the entire multiplicity profile are exactly computable.

**Proof.** Every nonempty path ending at y has a unique last edge (including its label); delete that edge. The last step is counted by T1. Conversely each shorter path to a predecessor extends uniquely by that label. The length bound follows from T2.

## FUG2-T5. Scale lifting and ancestral-history monotonicity [PROVED; consequence of SELECT-II scale covariance]

For positive integers B,x and an admissible word w,

`T_w(Bx) = B T_w(x)`, with the *same label word w* admissible from Bx.

Consequently, for every y and k,

`H_k(By) >= H_k(y)`, and `h(By) >= h(y)`.

**Proof.** For one step, `N|x => N|Bx` and `T_N(Bx)=B T_N(x)`. Induction proves this for any legal word. Each length-k path to y lifts injectively (multiply every intermediate state by B) to a path to By. Hence the cardinalities and the height inequality.

**Fibonacci corollary.** Because `m|n => F_m|F_n`, the inequalities hold for `y=F_m`, `By=F_n` whenever m|n:

`H_k(F_m) <= H_k(F_n)` for all k; `h(F_m) <= h(F_n)`.

**Important caveat.** Squarefree terminal **root sets need not be included** under scaling: lifting a root can turn it into a non-squarefree integer. Therefore monotonicity of paths does not imply `Roots(F_m) subset Roots(F_n)`.

## FUG2-T6. Direct-edge gcd criterion [PROVED; re-expression of known edge uniqueness]

For integers `0<x<y`, let `g=gcd(x,y)`. There is a directed integer-anchor edge `x --N--> y` exactly when

`y/g = (x/g+1)^2`, in which case `N=x/g` is the **unique** label.

**Proof.** Write `x=cN`, `y=c(N+1)^2`, and use `gcd(N,(N+1)^2)=1` to obtain `g=c`; substitution proves the converse. Applying Fibonacci strong divisibility `gcd(F_i,F_j)=F_gcd(i,j)` gives the exact Fibonacci-specific condition:

`F_j/F_g = (F_i/F_g + 1)^2` with `g=gcd(i,j)`.

This criterion requires no search over labels for direct Fibonacci edges; it does not by itself classify arbitrary multi-step reachability.

## FUG2-C1. Complete first-84 Fibonacci endpoint census [VERIFIED-EXACT finite result]

For all indexed pairs `1<=i<j<=84`, and **all forward lengths**, precisely four endpoint pairs are connected under selected `T_N`:

| i | j | shortest length | number of exact histories |
|--:|--:|--:|--:|
| 3 | 6 | 1 | 1 |
| 3 | 12 | 3 | 3 |
| 5 | 12 | 2 | 2 |
| 6 | 12 | 2 | 2 |

Hence there are exactly eight full labelled routes: one length one, four length two, three length three; there are no longer Fibonacci-to-Fibonacci routes in the finite window. This strengthens the 48-index, depth<=3 v001 census *without changing it*.

**Certification.** `run_p2.py` follows every reverse branch from each Fibonacci target to squarefree roots, with complete 64-bit factorizations. `verify_p2.py` independently aggregates all path counts in a DP and brute-checks all reverse states reached by Fibonacci targets up to index 60; it also verifies the 84-index records by exact edge/gcd signatures and factor recombination.

## FUG2-C2. Rich ambient ancestry, sparse Fibonacci endpoint links [VERIFIED-EXACT finite result]

For `F_12=144`, its ancestry has maximal length 3, 11 total distinct ancestral nodes **including the target**, and terminal squarefree roots `{2,5,6,11}`. For `F_72=498454011879264`, maximal length is 5, there are 23 distinct ancestral nodes **including the target**, and seven squarefree roots. An exact maximal-length history is

`82416337943 --1--> 329665351772 --2--> 1483494082974 --6--> 12115201677621 --7--> 110767558195392 --2--> 498454011879264`.

(Compare `results/fib_ancestry_84.csv` for all 84 layers; the `distinct_ancestor_nodes` column excludes the target.)

For `F_12|F_24`, index-divisibility lifts all paths and gives `h(F_12)=3 <= h(F_24)=4`; nonetheless their terminal squarefree-root sets are disjoint. This demonstrates the difference between route transport and root identity.

## FUG2-O1. Global Fibonacci reachability [OPEN]

Determine whether the four endpoint pairs found in the first 84 indices exhaust all pairs for arbitrary Fibonacci indices. The finite census does NOT settle this.

## FUG2-O2. Growth and classification of root spectra [OPEN]

Characterize the sets `Roots(F_n)`, their growth and overlap, and their relation to Fibonacci index divisibility beyond the proved history-count monotonicity. Determine whether infinite families of non-isomorphic ancestral branching geometries occur.

## FUG2-O3. Other nesting grammars [OPEN]

Repeat the induction using rational non-anchor occurrences and alternative explicitly specified continuation grammars, without replacing the founding `M ⟂ N` operation or assuming SELECT-II is the only mechanism.

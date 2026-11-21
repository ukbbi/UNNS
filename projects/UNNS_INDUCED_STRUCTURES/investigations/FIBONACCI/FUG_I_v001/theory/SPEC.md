# FUG-I v001 formal specification

## 0. Objects remain independent

**Fixed original UNNS arithmetic:** `S_N(M)=M(N+1)^2/N`, `M,N in Z_(>0)`, with positive rational outputs. Integer anchors occur iff `N|M`. The full original occurrence primitive is not restricted to anchors.

**Selected transition grammar:** `T_N(x)=x(N+1)^2/N` for `N|x`; the output is fed back as the next positive integer input. This is the SELECT-II choice, not an automatically determined binary composition.

**External recurrence:** `F_0=0,F_1=1,F_2=1,F_(n+2)=F_(n+1)+F_n`. The state `n` is a Fibonacci index, distinct even when `F_1=F_2`.

## 1. Incidence and fibre geometry (preexisting approach)

For n>=1, `D_n={d>=2: d^2|F_n}`. For each d in D_n, there is one occurrence:

`(M,N)=( F_n (d-1)/d^2, d-1 )`.

The indexed incidence set is `I_F={(n,M,N): S_N(M)=F_n}`. Its points retain their index and occurrence route. Within each layer, integer divisibility `d|e` can define a Hasse diagram; between layers, `m|n` can define occurrence transport `M -> (F_n/F_m) M` at fixed N. These relations originate respectively in arithmetic and Fibonacci index divisibility; they are **not** selected transition edges.

## 2. Ambient generative graph (SELECT-II only)

The directed graph `G_T=(Z_(>0), E_T)` has one labelled arrow

`x --N--> T_N(x)` for every divisor `N|x`.

Every arrow increases the integer: `T_N(x)/x = N+2+1/N >=4`.

An **ambient path** of length ell is a word of labels `w=(N_1,...,N_ell)` with each sequential divisibility condition satisfied. Its states are `(x_0,...,x_ell)`.

## 3. Fibonacci-induced path incidence

For index range `1<=i<j<=48`, write `i =>[w] j` when a legal directed ambient path starts at `F_i` and ends at `F_j`. Intermediate nodes may be any positive integers, not only Fibonacci values.

- `E_F^(ell)` is the multiset of indexed pairs decorated by all legal label words of length exactly ell; different words or intermediate states are distinct paths.
- `P_ell(i,j)` counts distinct admissible label words with the given endpoints.
- `d_T(F_i,F_j)` is minimum directed ambient path length, if it exists; the v001 search resolves it only for pairs with a path of length <=3.
- The retained external relation `n -> n+1` is the Fibonacci index-order relation, **not** a `T_N` arrow.

The distinction between points, labels and paths is mandatory. Numerical equality alone does not identify generative histories.

## 4. Finite exact computation and limits

Freeze `W={F_1,...,F_48}` (indices retained), maximum tested path length `ell_max=3`, only forward positive-index SELECT-II edges, with **no upper bound on nest labels other than divisibility**.

The program may prune any intermediate state above `F_48`, because a forward path strictly increases. This is an exact pruning rule, not a computational approximation.

The finite count is complete for `(i,j)` in the frozen index window and `1<=ell<=3`. It says nothing about paths first appearing at depth >=4, about arbitrary larger Fibonacci indices, or about undirected SELECT-II routes.

## 5. Two kinds of nesting must not be conflated

1. Incoming occurrence multiplicity at `F_n`, equal to `#D_n`.
2. Multiple directed generative histories between selected Fibonacci source and target observations, counted by `P_ell(i,j)`.

These are different invariants. At `F_12=144`, incoming multiplicity is `5`, but the v001 computation finds `4` two-step paths into 144 from indexed Fibonacci sources and `3` three-step paths from the source `F_3=2`. These counts address different questions.

## 6. Controls

The finite experiment is repeated unchanged for Lucas `L_1=1,L_2=3` and `L_(n+2)=L_(n+1)+L_n`, and for the deterministic perturbation `F_n+1`. The control is mathematical discrimination, not a significance test or physical null. The control's indices remain distinct even when values coincide.

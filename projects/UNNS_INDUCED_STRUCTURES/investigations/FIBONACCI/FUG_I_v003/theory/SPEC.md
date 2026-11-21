# FUG-I v003 — Generative ancestry geometry and history invariants

**Scope:** Fibonacci indices `1 <= n <= 84`, exact arithmetic; all directed path lengths, no finite depth cutoff. Every theorem formulated for all positive integers has a proof in `THEOREMS.md`; finite census rows are explicitly `VERIFIED-EXACT`.

## S0 — Substrate and continuation distinguished

The original UNNS nesting arithmetic remains

`M ⟂ N = M(N+1)^2/N`, for positive integers `M,N`, including rational non-anchor values.

FUG-I studies **one explicitly selected continuation**, the SELECT-II integer-anchor self-substitution

`T_N(x)=(x/N)(N+1)^2`, for positive integers `x,N` with `N|x`.

This directed grammar is not the entirety of the original UNNS Substrate. Each step grows by a factor `(N+1)^2/N >= 4`. Every inverse ancestry tree of a fixed positive integer is finite.

## S1 — Label words and complete histories

A word is a finite tuple `w=(N_1,...,N_k)` of positive integer labels, including the empty word `()`.

`T_w(x)` is obtained by performing the indicated steps in order, **only if each step is admissible**. An ending history `x --w--> y` includes its source, its ordered labels and all intermediate integer states.

`W(y) = {w: exists x >= 1 with legal T_w(x)=y}` is the complete history-word set of target `y`. Each `w in W(y)` identifies a unique source and state path once `y` is fixed. The empty word is in every `W(y)`.

`H_k(y)=#{w in W(y): |w|=k}` and `P_y(t)=sum_{k>=0} H_k(y)*t^k`. `H_0(y)=1`.

`R(y)=H_1(y)` is the usual immediate integer occurrence multiplicity. Neither `R` nor `P` captures a physical quantum observable by itself.

## S2 — Minimal source and endpoint thresholds

Define `r_N=(N+1)^2/N`. For a word `w=(N_1,...,N_k)` let `Q_{j-1}=prod_{i<j} r_{N_i}=a_{j-1}/b_{j-1}` in lowest terms, with `Q_0=1`.

The **minimal admissible source** is

`K(w)=lcm_{1<=j<=k} [ b_{j-1}*N_j / gcd(a_{j-1},b_{j-1}*N_j) ]`, with `K(())=1`.

The **minimal admissible endpoint** is the integer

`E(w)=K(w)*prod_{i=1}^k r_{N_i}`, with `E(())=1`.

Precisely the source multiples of `K(w)` support word `w`, and their endpoints are precisely the positive multiples of `E(w)`.

## S3 — Meet, transport and activation

`W(gcd(a,b)) = W(a) ∩ W(b)` for arbitrary positive integers. In particular, since `gcd(F_m,F_n)=F_{gcd(m,n)}`, the corresponding Fibonacci identity holds.

When `m|n`, scale `B=F_n/F_m` transports each complete word history of `F_m` injectively into `F_n`. The **new-history polynomial** is `D_{m,n}(t)=P_{F_n}(t)-P_{F_m}(t)` with nonnegative coefficients. `activation_depth(m,n)` is its lowest nonzero positive exponent or `0` if `D=0`.

An activation depth of 2 means there are no new *immediate* labels, but there are newly available two-step histories. This is an exact statement about the selected directed grammar, not a claim about unseen physical stages.

## S4 — Source-locked merger classification

A merger at endpoint `y` is an unordered pair of distinct nonempty words `w != v` with **the same source x** and `T_w(x)=T_v(x)=y`.

* `permutation`: label multisets agree (`Counter(w)==Counter(v)`); order may differ.
* `different_content`: label multisets differ; the rational multiplier equality is a genuine kernel relation rather than only commutativity of multiplication.

Each merger is counted as a pair of words **at a particular indexed Fibonacci layer**. Sources and endpoints may coincide at different indices; counting retains index identities. This is intentionally different from counting one identity globally.

## S5 — Explicit research limitations

Only Fibonacci indices through 84 enter the finite census. A theorem derived from an exact `F72` witness and Fibonacci divisibility extends **that specific configuration** to every `F_{72k}`, but does not classify all other index pairs or claim novelty of general content-kernel identities known in GEO-HD.

Lucas and `F_n+1` are arithmetic input controls, not a complete statistical null model. Their indices are kept distinct even if two terms have equal numerical values.

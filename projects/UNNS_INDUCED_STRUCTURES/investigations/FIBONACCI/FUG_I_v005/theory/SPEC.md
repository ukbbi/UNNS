# FUG-I v005 — Scope and objects

**Frozen primitive:** The founding UNNS arithmetic remains `M ⟂ N = M(N+1)^2/N` for positive integer M,N, including its rational non-anchor sector. It is not redefined in this study.

**Selected continuation grammar:** This phase investigates the positive-integer self-substitution route of SELECT-II:

`T_N(x) = x(N+1)^2/N`, allowed if and only if `N|x`, for positive integers x,N.

**Full (unrestricted) label grammar:** Every positive integer N is permitted when admissible. No finite alphabet truncation is used in the phase's defining classification.

**A finite word** `w=(N1,...,Nk)` is an ordered finite list of labels. It is legal from source x when each prefix of the corresponding T_N iteration produces a positive integer. A word has rational multiplier `Q(w)=prod_j (Nj+1)^2/Nj`; its minimum legal positive source is `K(w)` and minimum legal positive endpoint `E(w)=K(w)Q(w)`. Legal sources are exactly the positive multiples of K(w), and legal endpoints exactly the positive multiples of E(w).

**Ancestry language** `W(y)` consists of all finite words (including the empty word) that legally end at y from *some* positive source. It is finite at each fixed y because every step multiplies the state by at least four.

**Index overlay:** F_0=0,F_1=1,F_2=1 and F_(n+2)=F_(n+1)+F_n. The Lucas sequence has L_0=2,L_1=1 and the same recurrence; `F_(2n)=F_n L_n`. Denote the smallest index with q|F_n by `z(q)`.

**Full first-new-history depth:** For a|b, define

`delta(a,b) = min{ length(w): w in W(b) \ W(a) }`, or `0` if `W(a)=W(b)`.

Because a|b implies `W(a) ⊆ W(b)`, this is unambiguous. The empty word cannot contribute.

**Immediate incoming labels:** `D(y)={N>=1:(N+1)^2|y}`. Define `q(y)=prod_p p^floor(v_p(y)/2)`. Then `D(y)={d-1 : d|q(y),d>=2}`. This is not the forward-admissible label set `{N:N|y}`. The distinction matters.

**Source-locked merger:** Several distinct words w_i produce the same target from the *same* positive source. Equal endpoint alone is weaker unless the sources have also been checked.

## Evidence status

- **PROVED:** Theorem statements in `THEOREMS.md`, using explicitly declared inherited number-theoretic and FUG-I machinery.
- **VERIFIED-EXACT:** first-84 complete unrestricted pair census (307 proper index transports), fully certified Lucas quotient cases r=1,3,5,7, and independent arithmetic tests.
- **OPEN:** infinitude of odd r with squarefree L_(12r)/2, universal first-new-depth classification outside the stated families, complete different-content kernel classification beyond the constructed examples.

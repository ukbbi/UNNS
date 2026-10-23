# FIELD-I — proof record (v001)

All results use the **positive integer occurrence domain** `M>=1`, `N>=1`. This is arithmetic derived from the original fixed-nest formula. No novelty/priority or physical interpretation is implied by the word *theorem*.

## F1. Rational-fibre characterization [PROVED]

Let `x=a/b>0` be reduced (`gcd(a,b)=1`). Write `d=N+1>=2`. The equality

`M*d^2/(d-1) = a/b`

holds for positive integer `(M,N)` if and only if

`d^2 | a` and `b | (d-1)`.

**Proof.** Cross multiplication yields `b*M*d^2 = a*(d-1)`. Since `gcd(d^2,d-1)=1`, `d^2 | a`. Put `a=k*d^2` to obtain `b*M = k*(d-1)`. Because `gcd(k,b)=1` (as `k | a`), `b | (d-1)`. Conversely, if both divisibilities hold, set `N=d-1`, `M=(a/d^2)*((d-1)/b)`. Both are positive integers and substitution gives `S_N(M)=a/b`. The parameter `d=N+1` is unique for each occurrence. QED.

Thus

`R(a/b) = #{ d>=2 : d^2 | a and d==1 (mod b) }`.

When `b=1` this is the square-divisor count minus one: the RGG integer-anchor fibre count. For `b>1`, the denominator congruence is restrictive. The exact example `225/2` has `d=3,5,15`, hence occurrences `(M,N)=(25,2),(18,4),(7,14)`.

**Corollary [PROVED].** Every positive occurrence has integer output iff `N | M` (because `gcd((N+1)^2,N)=1`); non-anchor iff its output has reduced denominator greater than one. The non-anchor domain is not empty and may contain collisions.

## F2. Rational cross-nest intersection [PROVED]

Fix `N1,N2>=1`, set `L=lcm(N1+1,N2+1)` and `g=gcd(N1,N2)`. Then

`S_N1(Z_positive) ∩ S_N2(Z_positive) = { j*L^2/g : j=1,2,3,... }`.

**Proof.** If reduced `x=a/b` belongs to both nests, the F1 theorem applied with `d_i=N_i+1` gives `(N1+1)^2 | a`, `(N2+1)^2 | a` and `b | N1, b | N2`. Therefore `L^2|a` and `b|g`. Since `gcd(L,g)=1` (each prime dividing `g` divides both `N_i`, hence neither `N_i+1`), `x=(a/L^2)*(g/b)*(L^2/g)` is a positive integer multiple of `L^2/g`. Conversely any `x=j*L^2/g`, reduced by `c=gcd(j,g)`, has numerator `(j/c)*L^2` and denominator `g/c`. Its numerator is divisible by both `(N_i+1)^2` and its denominator divides each `N_i`; F1 supplies positive integer moduli in each nest. QED.

**Corollary [PROVED].** Their positive integer outputs meet at multiples of `L^2`. The first full rational intersection is noninteger exactly when `g>1`; in that case it is `L^2/g`. The formulas generalize, but do not independently select, the old anchor divisibility structure.

## F3. Finite rational-fibre enumeration [VERIFIED]

The exact enumeration and brute-force oracle agree over `1<=M<=90,1<=N<=20`; see `test_fibres.py`. Additional finite noninteger collisions are listed with explicit bounds in `output/witnesses/rational_collisions.json`. These are arithmetic collisions, not automatically nontrivial relational interactions.

## F4. Two consecutive observations [PROVED, but LABEL LEAKAGE]

For fixed `N`, `S_N(M+1)-S_N(M)=(N+1)^2/N = N+2+1/N`, strictly increasing for positive integer `N`. Thus `G(M,N)=(S_N(M),S_N(M+1))` is injective: its difference identifies `N`; its first coordinate then identifies `M`. This is an **invertible coordinate chart** on occurrences, not an independently selected binary interaction.

If the current value `x` has two distinct occurrences, their `N` labels differ (for fixed `N`, `M->S_N(M)` is injective). Thus their next output differs. Consequently, there is **no single-valued scalar map `F(x)`** whose value equals the fixed-nest successor for *every* occurrence of x, whenever the fibre has more than one route. The correct current state is at least `(M,N)` or a history/label-equivalent description.

## F5. Unary covariance does not select a binary relation [PROVED counterexample; operations PROPOSED]

Define `U(M,N)=(M+1,N)` and the following two binary operations on positive occurrences:

`J_low((M,N),(M',N')) = (max(M,M'), min(N,N'))`,

`J_high((M,N),(M',N')) = (max(M,M'), max(N,N'))`.

Both operations are **closed, commutative, associative, idempotent**, and agree when the two nest labels are equal (then each yields `(max(M,M'),N)`). Both satisfy simultaneous unary covariance:

`J(Ur,Us) = U(J(r,s))`,

because `max(M+1,M'+1)=max(M,M')+1`, while min/max of unchanged nest labels remains unchanged.

Yet `J_low` and `J_high` differ whenever `N!=N'`. In particular, the colliding rational inputs `(25,2)` and `(18,4)` both have value `225/2`, whereas `J_low` yields `(25,2)` of value `225/2` and `J_high` yields `(25,4)` of value `625/4`. Hence the original unary successor plus the listed natural algebraic constraints **does not select a unique binary operation**. Their formulas are deliberate adversarial constructions, not claimed intrinsic. QED.

**OPEN:** A justified binary interaction or relational law would require an *additional independently warranted principle*, not merely output collision or an injective label chart. The integer self-iteration graph of SELECT-II is a different proposed model and must not be conflated with this unary fixed-nest dynamics.

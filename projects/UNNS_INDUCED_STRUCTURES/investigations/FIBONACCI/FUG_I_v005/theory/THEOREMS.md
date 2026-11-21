# FUG-I Phase 5 — Theorems and proofs

**Framework:** Original `M ⟂ N` unchanged. All theorems concern the explicitly selected integer self-substitution grammar `T_N(x)=x(N+1)^2/N` with `N|x`, unless stated otherwise. Ordinary Fibonacci and Lucas number-theory identities are acknowledged as inherited results. Phase 5 claims new exact *specializations and certified constructions* inside this research record, not priority over the mathematical literature.

## FUG5-T1. Unrestricted recursive first-activation decision [PROVED]

Let a,b be positive integers with a|b. For each y, let

`D(y)={N>=1:(N+1)^2|y}` and `P_N(y)=y*N/(N+1)^2` for N in D(y).

Define δ(a,b) as in SPEC.md. Then δ is determined by the following finite recursion:

1. If `D(a) != D(b)`, then `delta(a,b)=1`.
2. Otherwise, for every `N in D(a)=D(b)`, compute `delta(P_N(a),P_N(b))`. If all are zero, `delta(a,b)=0`; otherwise `delta(a,b)=1+min{delta(P_N(a),P_N(b))>0}`.

**Proof.** Since a|b, any legal history ending at a scales by b/a to one ending at b; thus W(a)⊆W(b). Every nonempty word ending at y has a unique last label N∈D(y). Removing it gives a word ending at P_N(y), and conversely appending N to such a word gives a word ending at y. If a new last label appears, a new word of length one appears. When last-label sets are identical, all new words arise exactly from new predecessor words in some common last-label branch; their lengths increase by one. Every inverse move reduces the endpoint by a factor at least four, so the recursion terminates. □

**Scope:** This provides a complete *all-label decision algorithm for each fixed pair*; it is not a closed-form classification of all Fibonacci index pairs. The independent verifier reconstructs every finite pair difference by explicitly enumerating words rather than relying on this recursion.

## FUG5-T2. Exact immediate-activation criterion [PROVED]

For every a|b, set `q(y)=∏_p p^floor(v_p(y)/2)`. The incoming one-step label sets are identical iff `q(a)=q(b)`. Consequently,

`delta(a,b)=1` exactly when `q(a) != q(b)`.

**Proof.** A one-step incoming label is N=d−1 with d²|y, so the available d are the divisors d≥2 of q(y). Every positive integer q is uniquely determined by its divisor set. Thus one-step equality is equivalent to equality of q. Combine with T1. □

**Useful general quotient criterion.** Write b=a c. Then `q(b)=q(a)` iff for every prime p with v_p(a) odd, p does not divide c, and for every p with v_p(a) even (including v_p(a)=0), `v_p(c)≤1`. Equivalently, `c` is squarefree and is coprime to the product of primes appearing to odd exponent in a. This characterization holds for every positive a|b.

## FUG5-T3. Full-label Fibonacci doubling gate [PROVED]

For **every odd positive integer r**, define `a=F_(12r)` and `b=F_(24r)`. Then the *unrestricted* first-new-history depth is

`delta(a,b)=2` if `L_(12r)/2` is squarefree, and `delta(a,b)=1` otherwise.

In particular, new depth-two structure exists for every odd r; whether it is the *first* activation is decided exactly by Lucas squarefreeness.

**Proof.** Write n=12r. Classical doubling gives b=a L_n. The Fibonacci recurrence modulo 64 has period dividing 96 and direct residues at indices 12,36,60,84 modulo 96 are respectively 16,48,16,48. Since r is odd, `v_2(a)=4`. Also `v_2(L_n)=1`: n is even, and the Lucas identity `L_n²−5F_n²=4` together with `16|F_n` gives `L_n² ≡ 4 (mod 16)`, hence exactly one factor of 2 in L_n. Any odd prime common to F_n and L_n would divide 4 by that identity, which is impossible, so `gcd(F_n,L_n)=2`.

Therefore b adds exactly one factor 2 to a's even 2-adic exponent, and all odd prime factors of L_n/2 are new. By T2, the one-step label sets agree exactly when L_n/2 is squarefree.

Independently, the word `w=(7,2)` has minimum endpoint 288: `7 --7-->64 --2-->288`. Since F_24 is divisible by 288 and 24|24r, the word belongs to W(F_(24r)). It does not belong to W(F_(12r)), since its endpoint threshold contains 2^5 while `v_2(F_(12r))=4`. Thus δ≤2 and δ>0. If the one-step sets agree, δ=2; otherwise δ=1. □

**Explicit fully factored examples:**

- r=1: L_12/2=161=7·23, squarefree; δ=2.
- r=3: L_36/2=16692641=7·23·103681, squarefree; δ=2.
- r=5: L_60/2=1730726404001=7·23·241·2161·20641, squarefree; δ=2.
- r=7: L_84/2=179445175002939041=7²·23·167·14503·65740583; δ=1.

The listed factorizations are independently certified by trial-division primality testing for every displayed prime and exact product recombination. No claim is made about the frequency of squarefree Lucas quotients at untested indices.

## FUG5-T4. Infinite obstruction to unrestricted delayed-first activation [PROVED]

For every odd positive integer s, the pair

`(F_(84s), F_(168s))`

has `delta=1`, and the newly activated immediate label includes `N=6` (because `7²|F_(168s)` but `7²∤F_(84s)`). This is an infinite subfamily of the odd-r pairs in T3 with r=7s.

**Proof.** `z(7)=8`, seen directly from the first eight Fibonacci terms and strong divisibility. Since `84s≡4 (mod 8)` for odd s, 7 does not divide `F_(84s)`. Direct exact evaluation gives `49|L_84`. For odd s the Lucas identity `L_(ms)` as a polynomial in L_m (with m even) has odd parity and no constant term; equivalently, L_m divides L_(ms) whenever s is odd. Hence `49|L_(84s)`. Therefore `49|F_(168s)=F_(84s)L_(84s)` but 49 does not divide F_(84s), proving activation of N=6 at depth one. □

**Significance:** Phase 4's restricted-alphabet infinite depth-two law was correct, but a universally unrestricted depth-two claim for all odd r is false. The obstruction is explicit and infinite, not a large-index computational artifact.

## FUG5-T5. Infinite, unrestricted, matched non-Fibonacci delayed activation [PROVED]

For every prime p≥5, let a=144 and b=288p. Then a|b and

`delta(a,b)=2`

under the full positive-label grammar.

**Proof.** `a=2^4·3²`, while `b=2^5·3²·p` for p≥5. Thus `q(a)=q(b)=2²·3=12`; by T2 no new one-step label appears. But the word (7,2) has minimum endpoint 288 dividing b and not a. Hence the first new depth is exactly two. Since there are infinitely many primes p≥5, this gives an infinite family of fully unrestricted delayed activations in the *integer Substrate* independent of Fibonacci. □

**Interpretation:** An exact delayed-activation pattern by itself is not a distinctive Fibonacci phenomenon. The Fibonacci-specific challenge is to classify which of its index pairs realize the pattern.

## FUG5-T6. Arbitrarily many distinct-content source-locked mergers at Fibonacci targets [PROVED]

For every integer t≥1, define the common source and endpoint

`X_t=2^(2t) 3^(4t)`, `Y_t=2^(16t) 3^(4t)`.

For each j=0,...,t form the word

`w_(t,j) = 1^(7j) 2^(2(t−j)) 3^(4(t−j))`

(where exponents on labels denote repetition). These t+1 words all start legally from X_t, have distinct label-content vectors, and terminate at Y_t. Consequently, there exist Fibonacci targets with arbitrarily many **distinct-content histories from the same source**, namely F_(z(Y_t)), and every Fibonacci target with index divisible by z(Y_t) inherits the t+1 merger histories by integer scaling.

**Proof.** The multiplier identity

`[(1+1)²/1]^7 = [(2+1)²/2]^2 [(3+1)²/3]^4 = 4^7`

is exact; it was already reflected in the integer valuation-kernel results of GEO-HD. Each word w_(t,j) has multiplier `4^(7t)`. For legal generation, the initial source has at least 2t factors of 2 and 4t factors of 3. Each label-2 step consumes one factor 2, while each label-3 step consumes at most one factor 3; labels 1 add factors of 2 and labels 2 additionally add factors of 3. Therefore the displayed order of steps is legal from X_t. Their common endpoint is X_t 4^(7t)=Y_t. Since the number of label-1 steps is 7j, the t+1 content vectors are distinct.

For every positive modulus q, the pair recurrence `(F_n,F_(n+1))` modulo q is an invertible map on a finite set and hence returns to `(0,1)` after a positive number of steps. Thus `z(q)` exists, in particular z(Y_t). As `Y_t|F_(z(Y_t))`, multiply the common starting source by `F_(z(Y_t))/Y_t`; all histories remain legal and end at the indicated Fibonacci target. Strong divisibility then gives persistence at all index multiples. □

**Scope and provenance:** This is a constructive unbounded merger theorem for Fibonacci overlay using an inherited arithmetic kernel; it does not mean the Fibonacci recurrence internally generates the T_N steps. The construction is not unique to Fibonacci among divisible-sequence families.

## FUG5-C1. First-84 unrestricted census [VERIFIED-EXACT]

Over all 307 proper index-divisibility transports among Fibonacci indices 1–84, the full positive-label grammar yields:

| First new history depth | Number of index pairs |
|---:|---:|
| 0 (no new histories) | 193 |
| 1 | 108 |
| 2 | 6 |

The six unrestricted delayed pairs are `(12,24)`, `(12,36)`, `(12,60)`, `(12,72)`, `(24,72)`, `(36,72)`.

Two independent methods agree: paired-predecessor recursion (T1), and complete inverse-history enumeration followed by exact word-set difference. The former requires no finite alphabet and does not enumerate complete word sets. The 84-layer bound comes from the supplied v004 64-bit reference baseline, not from an assumed global bound on Fibonacci geometry.

## FUG5-C2. Finite certificate checks [VERIFIED-EXACT]

- Full prime factor certificates for r=1,3,5,7 of T3, with all primes checked by independent trial division.
- First 12 odd s members of the infinite obstruction family (T4), checked using fast-doubling Fibonacci modular arithmetic, alongside the all-s proof.
- Ten matched integer controls `(144,288p)`, for p=5,...,37 among the recorded prime list, checked by independent inverse-history enumeration.
- The first eight members of the unbounded merger construction (T6), with every displayed word replayed from a common source.
- Independent brute-square-divisor predecessor oracle over integers 1..1000.

## Open problems

1. Is `L_(12r)/2` squarefree for infinitely many odd r? The present work supplies the **iff criterion** for each r but does not settle this infinitude.
2. What additional arithmetic mechanisms yield first activation at depth 3 or above among larger Fibonacci layer pairs, if any?
3. Is there an effective, broadly applicable classification of first-activation depth by index arithmetic alone, avoiding large-integer factorization?
4. Which merger structures discriminate Fibonacci from valuation-matched and recurrence-matched controls?
5. What, if any, properties of the full rational non-anchor UNNS occurrence domain can be derived from these integer-route constructions?

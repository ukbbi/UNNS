# FUG-I Phase 4 — Structural activation and ancestry growth laws

**Scope.** Proved results for the **selected integer self-substitution grammar** `T_N(x)=x(N+1)^2/N` with `N|x`, laid against independently generated Fibonacci values. The original UNNS rational nesting operation is unchanged. Minimal-threshold, history-transport, and GEO-HD merger facts were established in earlier UNNS releases; new contributions here are the exact Fibonacci activation formulation, selected first-appearance gates, and the explicit infinite families.

## FUG4-T1. Fibonacci word-activation law [PROVED]

For every finite positive label word `w`, let `K(w)` be its minimal legal source and `E(w)=K(w)Q(w)` its minimal endpoint, with `Q(w)=prod (N+1)^2/N`. Then `w in W(F_n)` if and only if

`z(E(w)) | n`.

**Proof.** By the previously established minimal-endpoint theorem (FUG3-T1), `w in W(y)` iff `E(w)|y`. We justify rank of apparition and the divisibility-index law: the pair `(F_n,F_(n+1))` evolves invertibly modulo any positive integer `q` because `(a,b) -> (b,a+b)` has inverse `(a,b) -> (b-a,a)`; hence starting at `(0,1)` it returns to `(0,1)` after a positive number of steps. Therefore `z(q)` exists. The classical strong-divisibility identity `gcd(F_m,F_n)=F_gcd(m,n)` implies that the set of indices divisible by `q` is exactly the multiples of `z(q)`: if `q|F_n` and `q|F_z`, then `q|F_gcd(n,z)`, and minimality forces `gcd(n,z)=z`. Conversely `z|n` gives `F_z|F_n`. Apply to `q=E(w)`. QED.

**Corollary (complete history spectrum).** With `P_n(t)=sum_{w in W(F_n)}t^|w|`,

`P_n(t)=sum_{finite words w} [z(E(w))|n] t^|w|`.

Every coefficient is finite because all legal forward steps increase the integer by a factor at least 4. The formula applies at every positive Fibonacci index, not just n<=84.

## FUG4-T2. Simultaneous rank and transport laws [PROVED]

For positive integers `a,b`,

`z(lcm(a,b)) = lcm(z(a),z(b))`.

Thus specified words `w_1,...,w_s` all occur at a Fibonacci layer (possibly from distinct sources) exactly when its index is divisible by `lcm_i z(E(w_i))`. For `m|n`, the new words in layer `F_n` relative to `F_m` are exactly

`{w: z(E(w))|n and z(E(w)) does not divide m}`.

The first activation depth is the smallest `|w|` in this set, or 0 if the set is empty.

**Proof.** `lcm(a,b)|F_n` iff both `a|F_n` and `b|F_n`. By T1's rank law this happens exactly at common multiples of `z(a)` and `z(b)`, i.e., multiples of their lcm, proving the identity. For histories, use T1 and set difference. Since `m|n` every rank dividing m also divides n; no old history disappears. QED.

**Important distinction.** This joint-admissibility theorem does NOT imply a common starting source. Source-locked mergers need T3.

## FUG4-T3. Exact first-appearance gate for the different-content merger [PROVED]

Take two words

`a=(3,8,3)` and `b=(1,1,1,2)`.

Both have multiplier `Q=288`, but different label content. Their minimal individual sources are `K(a)=3` and `K(b)=1`. Hence the minimum **common** source is `3`, and the minimum common endpoint is

`E_pair = 3*288 = 864`.

The two words form a source-locked merger at Fibonacci target `F_n` **if and only if** `72|n`. Thus `F_72` is the first such Fibonacci target; every `F_(72k)`, k>=1, supports it.

**Proof.** A word is admissible from exactly the positive multiples of its minimal source. Therefore the common-source set is multiples of `lcm(3,1)=3`, and identical multipliers `288` give precisely the endpoints `864*k`.

The integer `864` divides `F_72`; it divides neither `F_24` nor `F_36`, as exact residues show:

`F_24 mod 864=576`, `F_36 mod 864=432`, `F_72 mod 864=0`.

Since `864|F_72`, its rank divides 72. Any proper divisor of 72 divides either 24 or 36, so the residues eliminate all proper divisors. Hence `z(864)=72`. Apply T1 to the paired minimum endpoint. QED.

**Witness at minimum source 3:**

`3 --3--> 16 --8--> 162 --3--> 864`

`3 --1--> 12 --1--> 48 --1--> 192 --2--> 864`.

The previously observed F72 source is `s=1,730,743,096,803 = 3*(F72/864)`.

**Caution.** This theorem classifies this named pair of words. It does not assert that other different-content mergers cannot occur at nonmultiples of 72.

## FUG4-T4. Infinite delayed two-step activation in a controlled grammar [PROVED]

Fix the explicitly restricted alphabet

`A={1,2,3,5,7,11}`.

For **every odd positive integer r**, the pair of Fibonacci layers `(F_(12r),F_(24r))` satisfies:

(a) identical one-step incoming label sets in alphabet A:

`D_A(F_(12r))=D_A(F_(24r))={1,2,3,5,11}`;

(b) `W_A(F_(12r))` is a proper subset of `W_A(F_(24r))`, and the **first new history depth is exactly 2**. A witness is the label word `(7,2)`, which has `K=7`, minimum endpoint `E=288`, and first Fibonacci appearance index `z(288)=24`.

**Proof.** Fibonacci modulo 64 has period dividing 96: from the recurrence, the pair `(F_96,F_97)` equals `(0,1)` modulo 64, and the recurrence is deterministic. For r odd, `12r mod 96` is in `{12,36,60,84}`; direct exact residues are `16,48,16,48` for `F_n mod64` respectively. Also, `24r mod96` is in `{24,72}`, both yielding `F_n mod64=32`.

Hence `v_2(F_(12r))=4` and `v_2(F_(24r))=5`. Since `12|12r` and `12|24r`, the integer `F_12=144` divides both values. Thus each label `N=1,2,3,5,11`, whose `(N+1)^2` divides 144, belongs to each one-step set. The only remaining alphabet label is `N=7`, whose required square `64` divides neither (their 2-adic valuations are 4 and 5). This proves (a).

The word `(7,2)` has minimum legal source `7`, as `7 --7-->64 --2-->288`; hence its minimal endpoint is 288. This endpoint divides `F_24` and therefore every `F_(24r)`. It does not divide `F_(12r)` because that integer has 2-adic valuation 4 while `288=2^5*3^2`. Therefore the word is new in the larger layer. Because `12r|24r`, existing histories persist by strong divisibility and T1. Since the one-step sets agree and the new word has length 2, the first new history depth is exactly 2. QED.

**Crucial scope limit.** For the *unrestricted* label grammar, new one-step labels may appear at higher labels as r varies. The theorem proves delayed first activation for the fixed alphabet A; it also proves appearance of a new two-step word in the unrestricted grammar but not that this is its first new depth for every odd r.

## FUG4-T5. Explicit unbounded ancestry-depth spine [PROVED]

For every integer `t>=0` let `n_t=6*4^t`. Then

`v_2(F_(n_t)) = 3+2t`, and

`max {k: (1,1,...,1) of length k belongs to W(F_(n_t))} = t+1`.

In particular, complete UNNS ancestry depths of Fibonacci targets are **unbounded** across the infinite Fibonacci family.

**Proof.** The Lucas numbers `L_n=F_(n-1)+F_(n+1)` satisfy `F_(2n)=F_n L_n`. Modulo 4, `L_n` has period 6: the initial pair `(L_0,L_1)=(2,1)` returns modulo 4 after six steps. Thus `L_n congruent 2 mod 4` whenever `6|n`. Since `F_6=8`, repeated doubling gives `v_2(F_(6*2^s))=3+s` for all integers `s>=0`. Substitute `s=2t`.

The word `1^k` multiplies a source by `4^k`; its minimum source is 1 and minimum endpoint `E=4^k`. It ends at a positive integer y iff `4^k|y`. Hence its maximal length at `y=F_(n_t)` is `floor(v_2(y)/2)=t+1`. Since t is unbounded, so are allowable depths. QED.

**Scope.** This is an exact lower bound on total ancestry depth. It identifies the maximal depth of all-`N=1` histories only, not the maximal possible mixed-label depth.

## FUG4-T6. Inherited history meet [PROVED — restated baseline]

`W(F_m) intersect W(F_n) = W(F_gcd(m,n))`.

This is inherited from the FUG3 complete-history gcd-meet theorem plus the classical strong-divisibility identity. Phase 4 re-verifies it independently but **does not claim it as a new theorem**.

## FUG4-C1. Exact finite first-84 activation census [VERIFIED-EXACT]

All 292 Phase 3 history records were rechecked, representing 84 empty words and 208 nonempty indexed occurrences. There are 84 **distinct** observed words (83 nonempty plus the empty word). Each word's individual Fibonacci appearance rank is computed and independently verified by minimal endpoint divisibility. Every occurrence among the first 84 layers is recovered from the rank alone.

First-appearance counts for the 83 distinct nonempty words:

| First Fibonacci index | Newly appearing words |
|---:|---:|
| 6 | 1 |
| 12 | 14 |
| 24 | 9 |
| 25 | 2 |
| 36 | 6 |
| 48 | 25 |
| 56 | 3 |
| 60 | 13 |
| 72 | 10 |

All 307 inherited index-divisibility transport classifications are reconstructed exactly: 193 unchanged, 108 first activated at depth 1, and 6 first activated at depth 2. There are 7,056 gcd-meet checks and 4,164 two-word rank-lcm cross-checks where the joint first index is <=84.

## FUG4-C2. Descriptive controls [VERIFIED-EXACT, NOT MATCHED NULLS]

Among 307 proper index-divisibility pairs:

| Indexed sequence | Failures of `W(value_m) subset W(value_n)` | Distinct words violating first-appearance index-periodicity |
|---|---:|---:|
| Fibonacci | 0 | 0 |
| Lucas | 37 | 4 |
| Fibonacci+1 | 55 | 35 |

These comparisons are a **check on index divisibility structure**, not evidence of a newly discovered Fibonacci-specific physical effect. The Fibonacci result follows from classical strong divisibility; Lucas and shifted-Fibonacci do not obey the identical index-divisibility structure. Counts are finite and the controls are not valuation-matched.

## Provenance and remaining questions

- `FUG3-T1`, `FUG3-T3`, `FUG3-T4`, earlier SELECT-II and GEO-HD provide minimal-source, scale-transport, and kernel machinery. `FUG4-T1/T2` specialize and sharpen it into Fibonacci index activation schedules.
- Infinite family T4 is **alphabet-restricted**. An unrestricted full first-depth-two family is **not** established.
- T5 proves unbounded *selected* ancestry depth across Fibonacci targets, not that any individual Fibonacci value has infinite ancestry.
- A complete classification of all Fibonacci merger types and their first-appearance ranks remains open.

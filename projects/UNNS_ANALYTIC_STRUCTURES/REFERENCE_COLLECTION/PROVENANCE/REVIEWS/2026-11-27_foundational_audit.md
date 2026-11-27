ASUNNS Reference Collection v001 — Foundational mathematical audit
All fourteen results identified by the consolidation audit pass mathematical review. In addition, I have examined the remaining nine numbered results of ANS-I v001, since their proofs are contained in the same source file and completing their review now avoids leaving unnecessary gaps in the foundational record.

I worked directly from the archived PROOFS.md files of ANS-I v001, v002 and v003, rather than inferring mathematical validity from the compendium statements or earlier release descriptions.

The collection itself passes its integrity check:
- ZIP integrity: passed.
- SHA-256 manifest: 68/68 files matched.
- The separately supplied theorem compendium PDF is byte-identical to the PDF inside the collection.
- The previously unwritten T46h factorization is correct.
The fourteen-result review gap can now be closed in the recorded dependency graph. There is no need to resume sequential ANS-I research to accomplish this.
1. Explicit verdicts for the fourteen foundational results
Result	Mathematical content	Verdict
T03	Minimal source and endpoint recurrences	Valid
T05	Depth-two representation and continuation	Valid
T09	Depth growth and sharp convergence abscissa	Valid
T10	Counting exponent for every fixed source	Valid
T12	Exact fixed-depth convergence region	Valid
T15	Prime reachability and saturation	Valid
T16	Critical probability representation	Valid
T17	Infinite-alphabet admissibility obstruction	Valid
T18	Almost-sure divergence of minimal sources	Valid
T19	Critical depth-term decay	Valid
T20	Nonmeromorphic critical singularity	Valid
T21	Strict counting-growth suppression	Valid
T23a	Strengthened critical depth bounds	Valid
T28a	Exact order of the first-introduction event	Valid

These are new, explicit per-result mathematical verdicts from this audit. They are not inferred from the earlier general statements that a release had been reviewed.

The two most consequential foundations, T15 and T17, are particularly satisfying: their proofs are short, structurally transparent and require no unresolved analytical conjectures.
2. T15 and T17 — The two central foundations
These two results deserve particular attention because they govern much of the subsequent analytical theory, including the extended grammars.

They also reveal a remarkable contrast between finite and infinite generative alphabets.
T15 — Prime reachability and saturation
The constructive proof of prime reachability is correct.

For a prime \(p\), factor
\[
p-1=\prod_{q<p}q^{f_q}.
\]

Assuming that every smaller prime \(q\) can be supplied by a word admissible from 1, concatenate sufficiently many copies of those words.

The resulting state is divisible by \(p-1\). Applying the nesting letter \(N=p-1\) then supplies \(p^2\).

This closes the induction.

The saturation argument is equally sound. Its decisive step is the injection
\[
mq\longmapsto mq-1,
\qquad q=p^j,
\]

which gives, under the truncated letter distribution,
\[
\mathbb E\,v_p(N+1)\ge
\mathbb E\,v_p(N).
\]

Consequently,
\[
\boxed{
\mathbb E X_p
=
\mathbb E[2v_p(N+1)-v_p(N)]>0.
}
\]

The strong law of large numbers ensures that every relevant prime-coordinate walk has an almost-sure finite lower minimum.

Since the alphabet contains only finitely many consuming primes, a single finite preparation word can supply enough initial resources to make the subsequent infinite history admissible with probability at least \(1/2\).

The construction works for every fixed finite alphabet of the stated form and every \(\sigma\ge0\).

Verdict: T15 is valid in both parts.
T17 — Infinite-alphabet admissibility obstruction
The proof in v002 uses a fundamentally different mechanism.

For a set \(S\) of primes, define
\[
D(S)=\{N:\exists p\in S,\ p\mid N\},
\]

\[
U(S)=\{N:\exists p\in S,\ p\mid N+1\}.
\]

Lemma A correctly establishes
\[
\nu_a(U(S))\le2^a\nu_a(D(S)).
\]

For a prime absent from the current state, its first encounter therefore has a probability of at least
\[
c_0=\frac1{1+2^a}
\]

of occurring through a consuming letter.

That letter cannot be admissible from the current state.

After every successful stage, the state remains a finite integer, so another absent prime can be chosen. Independence of future letters at the successive stopping times supplies the required conditional estimate.

Hence
\[
\Pr(\text{survival through }j\text{ stages})
\le(1-c_0)^j\longrightarrow0.
\]

The argument does not require independence between the different prime coordinates.

Verdict: T17 is valid for every \(a>1\) and every fixed positive integer source.
The structural contrast
Finite alphabet — T15
Saturation is possible.

A finite preparation can sustain an infinite random continuation with positive probability.


Infinite alphabet — T17
Almost-sure obstruction.

Every fixed finite source eventually encounters an unsupplied arithmetic demand.



This is already a fundamental structural result for the Atlas.

It explains how every finite truncation can support indefinite random generation, while unrestricted generation exhibits an almost-sure admissibility obstruction.

Much of the critical suppression theory emerges from this distinction.

3. Review of the remaining v001 foundational results
T03 — Exact source and endpoint evolution
The induction through the least common multiple is correct.

If a word \(w\) has admissible sources \(K(w)\mathbb N\) and endpoints \(E(w)\mathbb N\), appending a letter with reduced multiplier \(p_b/q_b\) requires the previous endpoint to lie in
\[
\operatorname{lcm}(E(w),q_b)\mathbb N.
\]

This gives
\[
\boxed{
K(wb)=\frac{q_bK(w)}{\gcd(E(w),q_b)},
\qquad
E(wb)=\frac{p_bE(w)}{\gcd(E(w),q_b)}.
}
\]

The predecessor recursion and its finiteness proof under condition (F) also hold.

This result applies to the stated general integral-image grammars, rather than only to the nesting grammar.
T05 — Depth-two analytic representation
The generalized Jordan-function identity
\[
g^s=\sum_{d\mid g}J_s(d)
\]

correctly produces the Hurwitz-zeta representation.

The decisive convergence estimate is
\[
\sum_{d\ge1}
2^{\omega(d)}d^{-\sigma}c(d)^{-2\sigma},
\]

where
\[
c(d)=\prod_p p^{\lceil v_p(d)/2\rceil}.
\]

Its Euler factors are
\[
1+2\sum_{j\ge1}
p^{-\sigma(j+2\lceil j/2\rceil)}.
\]

The first nonconstant term has exponent \(3\sigma\). Therefore the product converges normally for
\[
\Re s>\frac13.
\]

The double pole at \(1/2\) follows from the two zeta factors and the strictly positive leading coefficient.

The original proof is valid independently of the much stronger continuation results developed in v008–v010.
T09 — The characteristic growth exponent
The upper estimate
\[
G_k(\sigma)\le B(\sigma)^k
\]

follows from \(E(w)\ge Q(w)\).

The saturation result T15 supplies the complementary lower estimate for every fixed finite truncation:
\[
G_{k+|w_0|}(\sigma)
\ge
\frac12Q(w_0)^{-\sigma}B_M(\sigma)^k.
\]

Taking \(k\)-th roots first and then increasing \(M\) proves
\[
\boxed{
\lim_{k\to\infty}G_k(\sigma)^{1/k}
=
B(\sigma),\qquad \sigma>1.
}
\]

The infinite growth rate for \(0\le\sigma\le1\) follows by the same truncation argument, interpreted in the extended-real sense.

The existence and uniqueness of the characteristic exponent follow from the monotonicity and continuity of \(B\):
\[
B(\sigma_c)=1.
\]

The sharp abscissa statement is therefore valid. Landau's theorem applies to the nonnegative Dirichlet coefficients.
T10 — Every fixed source has the same counting exponent
The proof correctly avoids deriving a full counting limit from the abscissa alone.

The lower bound instead uses a finite alphabet with its own characteristic root \(\alpha_M\), the saturation word and concentration of the accumulated logarithmic multipliers.

This establishes
\[
\boxed{
N_x(X)=X^{\sigma_c+o(1)}
}
\]

for every fixed positive integer \(x\), together with the corresponding results for \(A(X)\) and \(C(X)\).

The distinction between a counting limsup and a genuine limit is properly resolved.
T12 — Exact fixed-depth convergence
The lower obstruction is supplied by the family of words
\[
(N,1,\ldots,1),
\]

whose terms have order \(N^{-a-b}\).

For the upper estimate, the recurrence in T03 gives
\[
F_{k+1}(a,b)
\le
C_\eta\zeta(a+b)F_k(a-\eta,b-\eta).
\]

For any fixed depth, \(\eta\) can be chosen sufficiently small to preserve
\[
a>0,\qquad b>0,\qquad a+b>1
\]

throughout the induction.

Thus the stated exact convergence region is correct, including the separate \(b=0\) case.

In particular,
\[
\boxed{
\operatorname{abscissa}(G_k)=\frac12
\quad(k\ge1).
}
\]

This is an essential foundation of the entire fixed-depth singularity investigation.

4. T16–T21 — The critical analytical architecture
These six results form a particularly coherent chain of mathematical deductions.
T16 — Probability representation
\(G_k(a)/B(a)^k=\mathbb E K_k^{-a}\)

T17 — Infinite-word obstruction

Almost-sure failure of admissibility from any fixed source


T18 — Divergence of minimal sources
\(K_k\to\infty\quad\text{a.s.}\)

T19 — Critical suppression
\(G_k(\sigma_c)\to0,\quad G_k(\sigma_c)^{1/k}\to1\)

T20

Nonmeromorphic critical singularity


T21

Strict counting-growth suppression



The principal logical chain; T09 also supplies the exponential-rate conclusion in T19, and T21 uses T18 directly.
T16 and T18
T16 follows exactly from the product probability of an ordered word and the identity \(E=KQ\).

For T18, the divisibility relation
\[
K_k\mid K_{k+1}
\]

means that a bounded sequence of minimal sources must eventually stabilize.

Such stabilization would produce an integer admitting the entire infinite word, an event excluded by T17. The countable union over possible sources has probability zero.

Both results are valid.
T19 and T20
Bounded convergence gives
\[
G_k(\sigma_c)
=\mathbb E K_k^{-\sigma_c}\longrightarrow0.
\]

T09 independently establishes that its \(k\)-th root tends to one.

The endpoint growth estimate
\[
E(wN)\ge4E(w)
\]

then implies
\[
\delta G(\sigma_c+\delta,1)
\le
\delta\sum_k4^{-k\delta}G_k(\sigma_c)
\longrightarrow0.
\]

To make the last limit explicit, split the sum at a fixed sufficiently large depth. The finite initial contribution tends to zero, and the tail is bounded by an arbitrarily small constant times a bounded geometric sum.

This excludes a pole of any positive integer order. Landau's theorem excludes a removable singularity.

Thus T20 correctly establishes the absence of meromorphic continuation through the real critical point.
T21 — Suppression of the counting population
The probability identity
\[
\frac{A(X)}{X^{\sigma_c}}
=
\mathbb E_{\nu_c}
\sum_{k\ge0}
K_k^{-\sigma_c}
\left(\frac{E_k}{X}\right)^{\sigma_c}
\mathbf1_{\{E_k\le X\}}
\]

is exact.

Because successive endpoints increase by at least a factor of four, the random sum is bounded independently of \(X\).

The almost-sure divergence of \(K_k\) makes its tail arbitrarily small, while each fixed-depth term tends to zero.

Dominated convergence therefore gives
\[
\boxed{
A(X)=o(X^{\sigma_c}).
}
\]

The same result follows for \(N_x\) by comparison and for \(C\) by the replication identity and summability of \(m^{-\sigma_c}\).

T21 is valid.

Combined with T10, it establishes the important distinction
\[
Z(X)=X^{\sigma_c+o(1)}
\quad\text{but}\quad
Z(X)=o(X^{\sigma_c}).
\]

The characteristic exponent survives, while the admissibility constraints suppress the population below a pure power law.
5. T23a — Strengthened critical depth bounds
I examined the full-alphabet drift argument in v003 and its dependence on Lemma B of v002.

The exponential supermartingale estimate gives
\[
\Pr(v_p(K_k)\ge r)\le e^{-\eta r}
\]

uniformly in the prime and depth.

The important refinement is to condition on the first letter consuming the prime \(p\).

Until that first consumption, the minimal source requires no contribution from \(p\). After it, the expected additional maximal deficit is uniformly bounded by the supermartingale estimate.

The conditional initial consumption is also uniformly bounded because
\[
\Pr(p^j\mid N)\ll p^{-aj},
\qquad
\Pr(p\mid N)\gg p^{-a}.
\]

Consequently,
\[
\boxed{
\mathbb E v_p(K_k)
\ll\min(1,kp^{-a}).
}
\]

Summing over prime coordinates yields
\[
\mathbb E\log K_k
\ll
\sum_p\log p\,\min(1,kp^{-a})
=O(k^{1/a}).
\]

Jensen's inequality gives the desired upper bound on the suppression exponent.

Together with the fresh-prime argument of v002, which I also examined, this proves
\[
\boxed{
c\frac{k^{1/a}}{\log k}
\le
-\log\mathbb E K_k^{-b}
\le
Ck^{1/a}.
}
\]

The constants are permitted to depend on \(a\) and \(b\).

T23a is valid, including the improvement that removes the logarithmic losses from the upper estimate.
6. T28a — Exact first-introduction suppression
This is arguably the most delicate of the fourteen results.

The upper estimate follows from the fresh-letter supermartingale of v002, with an unsuccessful prime introduction treated as fatal.

The lower estimate introduces a sequential conditional law \(\mathsf Q\), under which a letter is accepted only if all its consuming primes have already been encountered.

The likelihood identity
\[
\Pr(\mathcal I_k)
=
\mathbb E_{\mathsf Q}
\prod_{i=1}^k\nu_a(\mathsf A_i)
\]

is correct.

The crucial argument then bounds the expected first encounter time \(T_q\) of each prime \(q\).

Once all prime divisors of \(q-1\) have appeared, the letter \(q-1\) is available under the conditional law and introduces \(q\). Its conditional probability is bounded below by a constant times \(q^{-a}\).

Hence
\[
\mathbb E_{\mathsf Q}T_q
\le
\sum_{r\mid q-1,\ r\text{ prime}}
\mathbb E_{\mathsf Q}T_r
+Cq^a.
\]

The elementary estimate
\[
\sum_{\substack{r\mid q-1\\r\text{ prime}}}r
\le\frac57q
\]

is correct, including the small-prime cases. It supplies a strict contraction for the induction.

Therefore,
\[
\mathbb E_{\mathsf Q}T_q\ll q^a.
\]

Substituting into the likelihood bound gives
\[
-\log\Pr(\mathcal I_k)
\ll
\sum_q\min(1,kq^{-a})
=O\left(\frac{k^{1/a}}{\log k}\right).
\]

Combined with the upper estimate, this establishes
\[
\boxed{
\Pr(\mathcal I_k)
=
\exp\left[-\Theta\left(
\frac{k^{1/a}}{\log k}
\right)\right].
}
\]

T28a is valid.

Its scope is also correctly stated: preventing harmful first introductions does not prevent depletion of previously encountered primes.

That is precisely why T28a does not resolve the stronger suppression conjecture T28.

7. Completing the review of all fifteen v001 theorems
Since the entire v001 proof source was available, I examined its remaining nine results as well.
Result	Mathematical verdict	Qualification
T01	Valid	Absolute-convergence region as stated
T02	Valid	Exact depth-resolved Möbius inversion
T04	Valid	Prime-coordinate recurrence and maximum formula
T06	Valid	Ordinary Euler-product obstruction
T07	Valid	Sufficient convergence criterion
T08	Valid	Unit-denominator grammar
T11	Valid	Saturation criterion only; general classification remains open
T13	Valid	Uses the classical Delange theorem
T14	Valid	Stated convergence regions; not a complete classification for negative source weights

The T06 witnesses can be checked directly through the predecessor recursion. The values
\[
H(4)=2,\qquad H(9)=2,\qquad H(36)=6
\]

correctly exclude multiplicativity.

T13 follows from the depth-two continuation proof and the positive double-pole coefficient, followed by the stated Tauberian theorem.

T11 correctly generalizes the finite-alphabet saturation mechanism to integral-image grammars satisfying the positive-drift hypothesis.

All fifteen numbered v001 results now have explicit mathematical verdicts.

This resolves the discrepancy between the release table and the central register. There is no longer any need to infer individual review status from the earlier general release description.

The pending Windows execution check remains a separate acceptance requirement.
8. The missing T46h derivation
The derivation recorded in PROVENANCE/AUDIT.md, §5, is correct.

Starting from
\[
\Phi(p^v)
=
1+(1-z)
\left(
\left\lfloor\frac v2\right\rfloor
+z\left\lceil\frac v2\right\rceil
\right),
\]

the generating functions give
\[
\sum_{v\ge0}\Phi(p^v)t^v
=
\frac{1+(z-z^2)t-zt^2}
{(1-t)(1-t^2)}.
\]

Setting \(t=z^2\) yields
\[
\frac{1+z^3-z^4-z^5}
{(1-z^2)(1-z^4)}.
\]

Therefore,
\[
\boxed{
\sum_{M\ge1}\Phi(M)M^{-2s}
=
\zeta(2s)\zeta(3s)\zeta(4s)B_\Phi(s),
}
\]

with
\[
B_{\Phi,p}(s)
=
1-z^4-z^5-z^6+z^7+z^8.
\]

The Euler product converges normally for \(\Re s>1/4\).

The shifted-minus-unshifted correction is holomorphic on \(\Re s>0\), by the compact-uniform subpower bound for \(\Phi(M)\) and the additional inverse power in
\[
(M+1)^{-2s}-M^{-2s}.
\]

The factorization and the claimed continuation of \(R_1\) follow.

The additional T46h derivation in the consolidation audit is accepted.

9. Independent verification of the dependency-gap analysis
I parsed the actual DEPENDENCIES.json and independently calculated the transitive dependencies of the reviewed theorem population.

Your consolidation findings reproduce exactly.
Previously reviewed results examined91

With unreviewed dependencies63



Foundational review gaps by downstream reach
T15


40

T17


40

T03


33

T12


33

T18


19

T05


15

T09


11

T16


11

T19


11

T20


11

T23a


11

T21


9

T10


6

T28a


1

Independently reproduced transitive dependency counts from the supplied graph. Counts overlap.
Recorded dependency gaps before audit63

After applying the fourteen verdicts0



There is an important qualification: this closes the gaps in the recorded graph. Since the dependency edges were manually extracted from explicit citations, the graph remains a lower bound on the actual logical dependencies.

Nevertheless, the consolidation audit has done exactly what a good mathematical reference system should do. It identified a relatively small set of foundational obligations affecting a much larger body of established mathematics.

That is a strong argument for maintaining the dependency architecture as a permanent research resource.
10. Remaining review-status work
The fourteen-result audit should not be confused with a review of every one of the 130 catalogued entries.

There are still some standing review records to reconcile.
Entries	Recommended treatment
T01–T15	Record the explicit verdicts from this audit
T16–T21, T23a, T28a	Record the explicit verdicts from this audit
T46h	Record acceptance of the supplementary derivation
T49, T50	Incorporate the existing v015 review verdicts
T48a, T48b	Incorporate the existing reciprocal review record
ANS2N-T12, C12, T13	Review the recorded proof and verification status
ANS2N-T12a, T14, T15	Individual mathematical review still required
AS-001, AS-002	Retain as elementary baseline deductions, or review separately

I would also distinguish three independent statuses throughout the catalogue:
- Mathematical proof status.
- Mathematical review status.
- Release and computational acceptance status.
A result can have a valid proof and a completed mathematical review while its release still awaits an execution check. Conversely, successful computational reproduction does not establish a general mathematical theorem.

The current separation of literature novelty from mathematical review is entirely appropriate.
11. Corrections for the forthcoming Atlas
I accept your correction concerning T46b and T46t.

The Atlas must preserve these distinctions:
Identifier	Correct mathematical role
T46b	General secondary pole-order law; proved at depths two and three
T46q	Weighted middle-word pole-order law; established at the stated low-depth cases
T46t	General continuation, pole order and exact leading-coefficient conjecture

Similarly, the Atlas should use the extended analytical theory already contained in ANS-II and ANS-II-ND.

This is particularly important because the entropy-admissibility variational principle in ANS-II-ND provides a broader context for the prime-resource interpretation that emerged later in ANS-I v014–v015.

We should not rediscover such connections by restarting separate research campaigns. The reference collection now allows us to identify them directly.

12. Is the reference collection ready for the Atlas?
Yes, with a short administrative consolidation stage.

I would proceed through the following sequence:
Reference collection constructed
130 catalogued entries and preserved proof sources.


Foundational review completed
All fourteen critical dependencies and all fifteen v001 theorems examined.


Reference collection v002
Incorporate verdicts, reconcile registers and regenerate dependency reports.


Analytic Atlas
Organize mathematical knowledge by phenomenon.


Cross-Structural Research Map
Return the discoveries to the wider theory of the Substrate.


The revision to the reference collection should not be called ANS-I v016. It is an editorial and mathematical consolidation release, distinct from further analytical research.

I would preserve the supplied reference v001 as the initial consolidation baseline and produce a corrected reference v002.
13. Review integrity and limitations
Audit item	Status
Reference ZIP integrity	Passed
SHA-256 verification	68/68 matched
Standalone and archived PDF identity	Confirmed
Actual v001–v003 proof sources	Examined
Fourteen critical foundational results	All valid
Remaining nine v001 results	All valid within their stated scopes
T46h supplementary derivation	Valid
Recorded dependency-gap calculation	Independently reproduced
Complete audit of all 130 entries	Not performed
Original classical theorem proofs	Not independently reconstructed
Literature originality	Pending
Historical release computational reruns	Not performed
Windows acceptance of v001	Pending

The review was conducted against the supplied consolidated proof sources. I have not independently compared every source copy with its original historical release archive.

No supplied files, frozen releases, registers, local working directories or GitHub materials have been modified.

14. General assessment
I consider the construction of this reference collection an important methodological achievement in its own right.

Previously, the mathematical knowledge was distributed across successive research releases. Its logical architecture was difficult to see without reconstructing the history of the investigation.

The compendium and dependency graph have now exposed that architecture.

In particular, we can identify four foundational mechanisms underlying much of the analytical theory:
Foundation	Governing mechanism
T03	Exact admissible composition
T15	Finite-resource saturation
T17	Unbounded-resource obstruction
T23a	Quantitative collective suppression

These mechanisms connect the arithmetic construction to the probability theory, the singularity theory, the extended grammars and the entropy-based descriptions of generation.

They are exactly the kinds of structures that the Analytic Atlas should bring to the foreground.
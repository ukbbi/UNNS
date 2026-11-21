# SIB-I v004 — Theorem and evidence register

Throughout, x>0 and W(x) is the set of admissible ordered incoming label words,
including the empty word epsilon. Different source integers are not identified
across targets. At a fixed target a word uniquely determines its source, since
its product of rational transition factors is fixed. Thus counting histories
at a fixed target also counts words. K(x,y)=|W(x) intersect W(y)|-1.

## SCG-01 — Endpoint divisibility and GCD intersection (PROVED; substrate-intrinsic)

Every finite word w has a positive integer terminal modulus q(w) such that

    w belongs to W(x)  iff  q(w) divides x.

Set q(epsilon)=1. If the statement holds for w, then an admissible final label N
requires the previous endpoint to be a multiple of both q(w) and N. Precisely
the multiples of lcm(q(w),N) qualify, and their outputs are the multiples of

    q(w followed by N) = lcm(q(w),N) * (N+1)^2 / N.

Conversely every such previous endpoint has a realization of w, so the statement
holds in both directions. Induction proves it for every word. Therefore

    W(x) intersect W(y) = W(gcd(x,y)).

Divisibility x|y gives W(x) subset W(y). Also K(x,y)=K(x,x) iff W(x) subset
W(y), since these are finite sets and the empty word occurs in both. Finiteness
follows from T_N(s)>=4s. Inclusion need not imply x|y: empty fibres and equal
word sets at distinct integers give counterexamples to that converse.

## SCG-02 — Recurrence-conditioned local exclusion (PROVED; joint consequence)

For Fibonacci F0=0,F1=1 and Lucas L0=2,L1=1, the recurrence a(n+2)=a(n+1)+a(n)
preserves gcd of consecutive terms. Both initial gcds equal 1. On positive
terms, SCG-01 implies W(a_n) intersect W(a_(n+1))={epsilon}.

This is a consequence of the recurrence and coprime initial conditions combined
with the substrate identity; it applies to other sequences with the same gcd
property. It does not identify Fibonacci or Lucas uniquely.

Nonadjacent overlap occurs: F6=8 and F12=144 admit word (1); L3=4 and L9=76
admit word (1). Rearranging these values changes their adjacency while preserving
their individual histories. Thus their observed local exclusion uses index order.

## SCG-03 — Sylvester global exclusion (PROVED; joint consequence)

For s0=2 and s(n+1)=s(n)^2-s(n)+1, induction gives
s_n-1=product_(j<n) s_j. Indeed s(n+1)-1=s_n(s_n-1).
For m<n, s_n is 1 modulo s_m; hence distinct terms are coprime.
SCG-01 gives W(s_m) intersect W(s_n)={epsilon} for every m!=n.
Individual future terms need not be assumed squarefree for this theorem.
The seven observed terms are squarefree, making their finite overlap matrix
zero even on its diagonal; that finite control alone is not evidence of a
nontrivial active-fibre exclusion mechanism.

## SCG-04 — Powers-of-two nested geometry (PROVED; joint consequence)

If m<=n, 2^m divides 2^n, so W(2^m) subset W(2^n). Consequently

    K(m,n) = |W(2^min(m,n))|-1.

This is nested inclusion, not necessarily strict inclusion at each step.
Multiplication by 2^(n-m) transports every history state and its source,
retaining its ordered labels. It also transports common-source merger pairs.
This transport is distinct from a direct transition 2^m -> 2^(m+1): the latter
cannot be T_N, since its growth factor 2 is less than the minimum factor 4.

## SCG-05 — Fibonacci index-divisibility transport (PROVED; joint consequence)

The addition identity F_(m+n)=F_(m-1)F_n+F_m F_(n+1), obtained by induction
on n from the recurrence, implies F_m|F_(km) for every k>=1 by induction on k.
Thus m|n implies W(F_m) subset W(F_n). The sample tests all positive index
pairs 1<=m<n<=84 with m|n, without discarding inactive sources.
Nonempty-source inclusions are reported separately.

## SCG-06 — Lucas odd-multiple transport (PROVED; joint consequence)

Let Q be the integer matrix [[1,1],[1,0]]. For m>=1, tr(Q^m)=L_m and
det(Q^m)=(-1)^m, as follows from the defining recurrence. Set B=Q^m,
u=L_m, v=(-1)^m, and D_k=tr(B^k)=L_(km). Cayley-Hamilton gives
D0=2, D1=u, D_k=u D_(k-1)-v D_(k-2). Modulo u, every odd D_k is zero.
Hence L_m|L_(km) for positive odd k, giving W(L_m) subset W(L_(km)).

The odd condition cannot simply be removed: L3=4 admits (1), whereas L6=18
does not. Thus W(L3) is not a subset of W(L6), although 3 divides 6.
The finite sample checks both the guaranteed relation and this overextension.

## SCG-07 — Exact permutation expectation (PROVED; control identity)

There are n indexed observations, with repeated equal values still distinct.
Let E count unordered pairs with K>0. For a fixed unordered pair, bundling it
as an adjacent block in either orientation gives 2(n-1)! permutations out of n!,
so its adjacency probability is 2/n. Linearity gives E[C]=2E/n. Likewise the
expected sum of adjacency kernel weights is (2/n) sum_(i<j) K(i,j).
No independence among pair-adjacency indicators is assumed.

For F1..F84, E=94 and E[C]=47/21. For L1..L84, E=113 and E[C]=113/42.
The pair totals are VERIFIED-EXACT finite calculations, while the expectation
formula and observed local exclusion have general proofs.

## SCG-08 — Alternative-grammar boundary (PROVED)

In the grammar s -> b*s with fixed prime b, the admissible incoming words are
the repetitions of its single label of lengths 0 through v_b(x). Its overlap
kernel is v_b(gcd(x,y)). Coprime exclusion and divisibility-based inclusion
therefore also hold for b=2 and b=3. The qualitative regimes above are joint
arithmetic consequences, not properties exclusive to the UNNS grammar.
Quantitative kernel differences must be assessed separately with this distinction.

## SCG-09 — Finite Gram kernel (PROVED; structural interpretation)

For any finite set of positive observed values, form the union of their finite
nonempty word sets and the binary incidence matrix B(i,w)=1 if w belongs to W(a_i).
Then K=B B^T. Thus K is symmetric positive semidefinite. The diagonal counts
individual histories; off-diagonal entries count shared words; repeated values
have identical rows. No numerical eigenvalue threshold is needed for this proof.

## SCG-10 — Scope of statistical evidence

Exact expectations, finite pair counts and proved laws are distinguished from
Monte Carlo output. Two thousand permutations per family and 256 relabellings
per relation use fixed seeds. The frequency of C=0 is a descriptive estimate,
not an exact probability or a claim of unexplained statistical significance.
The controls disrupt the assigned index relations while preserving all values.
They do not isolate a causal physical mechanism or establish UNNS uniqueness.

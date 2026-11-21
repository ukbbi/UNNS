# SIB-I v003 theorem and evidence register

Let P(x) contain the incoming edges (s,N) with T_N(s)=x. Equivalently, for each
d>=2 with d^2|x, include (x(d-1)/d^2,d-1). Let H_h(x) count length-h histories
from any positive source to x; H_0(x)=1 denotes the empty history at x only.

## RPA-01 — Exact depth profile (PROVED)

For h>=1, H_h(x)=sum_(s,N in P(x)) H_(h-1)(s). Every history has a unique
last edge, so the sum is disjoint even when earlier branches share a source.
The nonempty-history polynomial satisfies

    F_x(z) = z * sum_(s,N in P(x)) (1 + F_s(z)).

Its coefficient of z^h is H_h(x), its value at 1 is total route count, and
its degree is maximum depth (defined as 0 for the zero polynomial).
All predecessors are <=x/4, so recursion terminates. The full unlabelled
unfolded predecessor tree therefore determines the entire depth profile.

## RPA-02 — Truncated exponent-decorated signatures (PROVED)

Let E0(x) be the sorted prime-exponent list. Define

    E_(h+1)(x) = (E0(x), multiset{ E_h(s) : (s,N) in P(x) }).

Equality of E_h signatures implies equal route counts at lengths 1 through h+1.
For h=0 this follows from R_1(x)=product(floor(e/2)+1)-1. Inductively, the
child multiset determines the sum of each length profile available at the
previous signature depth, while E0 determines the one-step count.
This theorem does not assert equality of longer histories or merger counts.

## RPA-03 — Unfolded shape loses convergence and content (VERIFIED-EXACT counterexamples)

Ufull(x) is recursively the multiset of Ufull(s) for its incoming predecessors,
with an empty multiset at a leaf. It retains neither labels nor node identities.

100 and 896 have identical Ufull and 9 routes each. Their numbers of distinct
sources are 7 and 8, and merger-source counts are 2 and 1 respectively.
300 and 14884 have identical Ufull and 10 routes each, but different-content
pair counts are 0 and 1 respectively. These are finite exact counterexamples
to sufficiency of unfolded shape for those quantities. Complete case edges and
ordered routes are exported, and independent inverse enumeration validates them.

These examples establish insufficiency of this representation. They do not
individually isolate label erasure from source-identity erasure; both occur in Ufull.

## RPA-04 — Exact source/content recurrence (PROVED)

Let C_x(s,m) count nonempty ordered histories from source s to x with label
multiset m. For each incoming edge (p,N), add 1 to C_x(p,{N}); for every
nonzero C_p(s,m), add C_p(s,m) to C_x(s,m union {N}), retaining multiplicity
of labels in the union. Contributions from different last edges add.
Induction on target value proves that this recurrence counts every ordered
history once in exactly its source/content cell.

Write A_s=sum_m C_x(s,m). Then:

    total routes = sum_s A_s
    merger sources = count{s : A_s>=2}
    all common-source unordered pairs = sum_s binomial(A_s,2)
    permutation pairs = sum_(s,m) binomial(C_x(s,m),2)
    different-content pairs = all common-source pairs - permutation pairs.

The multiset cardinality records route length, so depth profiles are also
recoverable from C. Absolute source names may be consistently renamed; equality
across paths must be preserved. This is sufficient for all listed metrics,
with no claim of minimality or bounded memory independent of target size.

## RPA-05 — Information summaries (PROVED)

The length profile determines total routes and maximum depth. The source
spectrum determines total routes, source count, merger-source count and all
common-source pair counts, but it need not distinguish permutation and
different-content pairs. Finite counterexamples to that distinction are exported.
The content spectrum retains, for each source, the list of content-cell counts;
the formulas in RPA-04 therefore determine the merger counts from it. As the
content spectrum drops actual multisets, it need not determine maximum depth.

## RPA-06 — Finite recursive classification (VERIFIED-EXACT; global extension OPEN)

In 1..65536, E3 and Efull induce the same partition, with 1541 classes.
All six tested metrics are constant in every Efull class. E2 still has 7
classes with variable route counts, although different-content counts do not
vary within any E2 class in this domain. These are finite census facts.
Whether complete exponent-decorated predecessor trees determine merger counts
for every positive integer remains OPEN. No general conclusion follows merely
from absence of a counterexample through 65536.

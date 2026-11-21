# SIB-I v002 research register

## V2-01 — Exact all-depth powers-of-two threshold

**Status: PROVED existence and persistence; VERIFIED-EXACT minimality by exhaustive finite computation.**

The user supplied these two histories in the independent audit of v001:

    6 --6--> 49 --7--> 448 --7--> 4096
    6 --3--> 32 --2--> 144 --3--> 768 --3--> 4096

Every arrow is T_N with N written above it, and N divides its source state.
The words (6,7,7) and (3,2,3,3) have different multisets. For every r>=0,
multiply each state by 2^r. Homogeneity and preserved divisibility give the same
two words from 6*2^r to 2^(12+r). Hence every 2^k, k>=12, has such a merger.

Minimality is established by the complete 1..4096 census: no 2^k with 0<=k<12
has any pair of different-content histories from a common source. Completeness
follows from T_N(s)/s=N+2+1/N>=4 and strict growth, so every state of a history
ending at x<=4096 lies in the enumerated interval. Sources above 1024 cannot
produce a target <=4096. Every legal label at every remaining source is checked.
Forward propagation is exhaustive by induction on target value. A separately
implemented inverse recursion agrees on the entire set of histories at every target.

This strengthens the infinite-family onset to k=12. It does not change the correct
v001 statement that first activation within depth <=3 occurs at k=14. The family
has infinitely many targets; this statement alone does not assert unbounded
merger multiplicity for any one fixed target.

## V2-02 — What the exponent signature determines

**Status: PROVED; specialization of the existing incoming-fibre formula.**

For x=product p_i^e_i, an incoming edge corresponds to d>=2 with d^2|x.
Thus R_1(x)=product(floor(e_i/2)+1)-1. The exponent signature completely
determines this count and whether any incoming history exists. Prime identities
are needed to recover actual d values, labels d-1 and predecessors x(d-1)/d^2.

## V2-03 — Prime-square ancestry and insufficiency of exponent matching

**Status: PROVED.**

For a prime p, the only incoming edge to p^2 is (p-1) --(p-1)--> p^2.
Every length h>=2 history into p^2 is a length h-1 history into p-1 with the
label p-1 appended. Therefore H_h(p^2)=H_(h-1)(p-1), and the total number of
nonempty histories is 1+H_total(p-1).

In particular, 289=17^2 and 361=19^2 have the same exponent signature (2)
and bit length 9, with R_1=1 each. Their predecessors are 16 and 18, with
R_1(16)=2 and R_1(18)=1. Thus H_2(289)=2 and H_2(361)=1. Prime-exponent
architecture alone, even with binary magnitude matching, does not determine
the deeper induced geometry. The relevant additional arithmetic includes p-1,
and more generally the recursively generated factors d-1.

## V2-04 — An unavoidable missing-control case

**Status: PROVED.**

An integer with the exponent signature (k) of 2^k must be q^k for a prime q.
If q is distinct from 2 then q>=3. For k>=2, 3^k>=2^(k+1), since
(3/2)^k>=9/4>2. Hence q^k lies outside the bit-length bin
[2^k,2^(k+1)). There is no distinct same-signature, same-bin control for 2^k
when k>=2. This is independent of the finite census ceiling. The matched
powers-of-two summary covers only the inactive value 2, compared with 3.

## V2-05 — Limits of sequence-specific marginal claims

**Status: PROVED dependence statement; methodological consequence.**

Under this overlay every target's ancestry is a function of its integer value.
Two external sequences observing the same value induce the same ambient fibre
and histories at that value. Keeping the entire prime-labeled factorization
fixed keeps the integer fixed. Distinct-value controls must preserve selected
features, such as exponents, rather than the full factorization. Sequence-level
claims can concern distributions, repetition or ordered relations among values;
they require those layers to be specified independently.

## V2-06 — Finite architecture and order comparisons

**Status: COMPUTED descriptive comparisons with VERIFIED-EXACT census inputs.**

All nonempty arithmetic strata in 1..4096 and all control pools are enumerated.
Order controls use 32 reproducible permutations. Coverage, finite domain and
pool weighting are part of the result. No statistical significance, universal
sequence superiority or causal recurrence mechanism is established.

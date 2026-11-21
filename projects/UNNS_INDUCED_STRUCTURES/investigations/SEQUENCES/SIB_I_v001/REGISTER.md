# SIB-I v001 theorem and evidence register

## SIB-01 — Incoming fibre and all-depth obstruction (PROVED; baseline specialization)

For a positive integer target x, T_N(s)=x with N|s iff, with d=N+1>=2,
d^2|x and s=(x/d^2)(d-1). Indeed s=kN implies x=k(N+1)^2;
the converse is immediate. Thus R(x)=product_p(floor(v_p(x)/2)+1)-1.
An incoming positive-length history exists iff x is not squarefree, since every
history has a final edge and every incoming edge itself is a history.
All primes have empty incoming ancestry at every depth. This is inherited
arithmetic applied to the sequence panel, not a new primitive theorem.

## SIB-02 — Finite ancestry (PROVED)

T_N(s)/s=N+2+1/N>=4. A length-h history from s>=1 to x requires x>=4^h.
The recursion terminates, and h<=floor(log_4(x)). The released enumeration stops
at depth 3; the finite bound does not make that enumeration unrestricted.

## SIB-03 — Powers-of-two fibres and restricted chains (PROVED)

For x=2^k, d^2|x iff d=2^j, 1<=j<=floor(k/2).
Its incoming predecessors are 2^(k-2j)(2^j-1), with labels 2^j-1.
Hence R(2^k)=floor(k/2). Only j=1 gives a predecessor that is itself a power
of two. The graph restricted to all powers of two therefore consists of the
even-exponent and odd-exponent chains, using label N=1 and step k -> k+2.
Ambient ancestry also includes the non-power-of-two predecessors for j>=2.

## SIB-04 — Homogeneous transport (PROVED; baseline consequence)

If x divides y, multiplication by y/x transports any legal history ending at x
to a legal history ending at y with the same label word. Integrality and each
label divisibility are preserved, and T_N(cs)=cT_N(s).
This is conditional on divisibility, not a claim that consecutive sequence terms
always satisfy it. In particular, every powers-of-two history transports from
index k to k+1 by doubling all states.

## SIB-05 — Duplicate observations (PROVED; definition consequence)

The arithmetic fibre depends only on the value x. Repeated values at different
external indices have equal fibres but remain distinct indexed observations.
Totient multiplicity must therefore be separated from common-source route mergers.

## SIB-06 — Finite panel and controls (VERIFIED-EXACT after verifier passes)

The sequence-specific counts are exhaustive through depth 3 for the stated
indices. Eight-replicate control differences are descriptive computed results.
There is no inference of all-depth merger absence, statistical significance,
infinite Sylvester squarefreeness, or universal classification from this panel.

## SIB-07 — Infinite different-content merger family at powers of two (PROVED)

The following two admissible paths share source 63 and target 16384:

    63 --N=63--> 4096 --N=1--> 16384
    63 --N=7--> 576 --N=3--> 3072 --N=3--> 16384

Each label divides its source state. Their words (63,1) and (7,3,3) have
different label multisets and different lengths. By SIB-04, for every integer
r>=0 multiplication of all states by 2^r gives the same two words from
63*2^r to 2^(14+r). Thus every powers-of-two term with k>=14 admits a
common-source different-content merger. This proves an infinite family of
targets, not unbounded merger multiplicity at one target. Exhaustive enumeration
finds k=14 first within depth 3; earlier all-depth activation remains separate.

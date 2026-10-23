# FIELD-I  (v001) - Rational nest fibres. Status of results
Source rule: 2017 fixed-nest sequence S_N(M)=M(N+1)^2/N, d=N+1. v3 manuscript, RGG-1/2/2.1, SELECT-I/II untouched.

## Proved (elementary) and checked (field1.py, ALL PASS)
T1 Rational-Fibre Theorem. x=a/b lowest terms. Occurrences <-> {d>=2 : d^2|a, d=1 mod b}; N=d-1, M=(a/d^2)(d-1)/b.
   Proof: b M d^2 = a(d-1); gcd(d^2,d-1)=1 => d^2|a; a=kd^2 => bM=k(d-1), gcd(k,b)=1 => b|d-1. Converse by construction.
   Checked: independent brute force (N<x-1 bound) on all 109,557 reduced a/b, a<=1500,b<=120; 90,000 generated occurrences.
T1' Reparametrisation. M=kg, N=bg, gcd(k,b)=1: value k(bg+1)^2/b in lowest terms; denominator b=N/gcd(M,N).
T1'' Sub-fibre form. F(a/b) = {anchors of a with b | N} via (M,N)->(bM,N). Hence R(a/b)<=R(a).
T2 Cross-nest intersection. S_N1(Z>0) n S_N2(Z>0) = {jL^2/g}, L=lcm(N1+1,N2+1), g=gcd(N1,N2). (lcm of reduced lattices.)
   gcd(g,L)=1, so the first coincidence is an integer iff gcd(N1,N2)=1.
T3 Realisability. Non-integer a/b is realised iff a has a square divisor d^2 with d>1, d=1 mod b. Necessary a>=(b+1)^2, tight (=S_b(1)).
T4 Congruence obstruction. d,d' in D(a/b): lcm(d,d') in D(a/b) <=> gcd(d,d')=1 mod b (lcm = g^-1 mod b). Same criterion for gcd.
   Smallest failure: x=400/3, d=4,d'=10.
T5 Refinement T_q:(k,d)->(k/q^2,dq) preserves the rational fibre iff q=1 mod b.

## Data (not theorems)
Smallest non-integer value with R>=2: 81/2; R>=3: 225/2; R=5: 2025/2.  Realisable non-integers (a<1500,b<38): R=1:479, R=2:17, R=3:9.
Anchor pairs (m<=3000): first common future is an integer for 1108 pairs, non-integer for 169 (first: m=81, d=3,d'=9 -> 81+81/2).

## Proposed / status
F5 rendezvous: two same-value occurrences first re-coincide at x+L^2/gcd(N,N') (checked 5394 pairs). It is a rule-determined binary
 quantity, not a function of the manuscript distance D (22 of 44 D-values carry >1 rendezvous). It depends on (N,N') only, so it reads the labels.
F4 (label-free relational distinction): no result. F5 selection of a binary operation: no result.
Manuscript: no revision warranted yet.

# FIELD-I v002 — Intrinsic Relational Selection (SPEC)

Scope: FIELD-I v001, manuscript v3, RGG-1/2/2.1, SELECT-I/II are NOT modified. No physical or entanglement claim is made.
Labels: **proved** (proof in THEOREMS.md), **checked** (field2.py, exact arithmetic), **data** (finite observation, not a theorem), **open**.

## 1. Rule under study (only this)
Occurrence r = (M,N), M,N >= 1, d = N+1, value v(r) = M d^2 / N, fixed-nest successor F(r) = (M+1,N).
Step s_N = d^2/N is already reduced (gcd(d^2,N)=1). Fibre F(x) = occurrences with value x; R(x) = |F(x)|.
x = a/b (lowest terms): F(x) <-> D(x) = {d >= 2 : d^2 | a, d = 1 mod b}  (v001 T1).
Pair (r,s) in F(x), d,d' their moduli, L = lcm(d,d'), g = gcd(N,N'):  Delta_rs = L^2/g,  h_rs = x/Delta_rs.
Collective: Delta_coll = lcm(d_i^2)/gcd(N_i),  gamma(x) = x/Delta_coll.
Rendezvous spectrum H(x) = multiset { h_rs : {r,s} subset F(x) }.  Rendezvous graph G(x) = complete graph on F(x), edge weight h_rs.

## 2. Observation regimes (F7)
A  value only: O_A(r) = x.            B  successive values: O_B(r) = (x, v(F r)).
C  unlabelled collective: O_C(x) = H(x) (and its refinement G(x)).    D  one pair's first future intersection (x, Delta_rs).
Label-blindness is formalised as invariance under Pi = prod_x Sym(F(x)), the automorphism group of (Occ, v).

## 3. Candidate binary interaction (F8)
A pair operation * assigns to every pair of distinct occurrences of equal value x a result. Axioms:
- A1 domain: exactly the pairs of distinct occurrences with equal value.
- A2 symmetry: r*s = s*r.
- A3 common future: the result is a value y > x lying on both routes (value-valued), or an occurrence at such a y (occurrence-valued).
- A4 stationarity: for the pair shifted by i rendezvous periods, (r_i, s_i) at x+i*Delta_rs: (r_i * s_i) = (r * s) + i*Delta_rs.
- A6 label-blindness: Pi-equivariance (result unchanged by fibre-wise relabelling).
- A7 minimality: the result is the first common future.
Selection outcome: constraints force a unique *.  Non-selection outcome: two admissible, distinct *.
Gate (F8): decide between them for each constraint set; test with explicit competing operations and adversarial examples.

## 4. Verifier design (field2.py)
Exact Fractions/integers only. Independent constructions: (i) box enumeration of all occurrences with value <= X0 (no use of the T1 formula); (ii) brute-force common-future search by integer set intersection; (iii) formula corpus (a<=8000, b<=30) validated against (i).
Status tags PASS / FAIL / DATA / OPEN. Exit code 0 iff no FAIL. FIELD2_QUICK=1 shrinks bounds.
Test index: F0 construction; F6 spectrum (F6.1-F6.9); F7 regimes (F7.1-F7.9); F8 operations (F8.1-F8.9); F9 open items.

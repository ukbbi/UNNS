# SIB-I v005 - Recurrence-Mediated Structural Activation

Research release, not a manuscript. v001-v004 are unchanged. Substrate fixed (T_N(x)=x(N+1)^2/N, N|x).

Question (from the v004 review): can the external sequence's own recurrence operation create, suppress or reorganize admissible UNNS histories in a way pairwise ancestry overlap does not capture?

Declared joint system. State = vector of consecutive terms, e.g. s_n=(a_{n-1},a_n). Two operations act on states: the recurrence step R (s_n -> s_{n+1}) and the UNNS step T_N applied to every coordinate (admissible iff N divides every coordinate). Induced object: histories of a state under both operations; ancestors, word sets and their factorization.

## Findings (all exact or exhaustively verified on stated boxes; see REGISTER.md)
1. **Equivariance.** Every linear homogeneous recurrence commutes with T_N on its domain (T_N is a scalar). Nonlinear or affine recurrences (Sylvester x^2-x+1, 2x+1, x^2) violate this in 100% of tested cases.
2. **Alphabet gating.** The admissible UNNS alphabet of a state vector is W(gcd of its coordinates). For any linear recurrence, gcd(a_n,a_{n+1}) is constant, so the pair-level alphabet is recurrence-invariant: W(gcd(a_0,a_1)).
3. **Suppression.** Single terms carry more words than their pair-states: F_12=144 has 15 nonempty words, but the pair state (89,144) has none (gcd 1). The words that "activate" at a sum are not transportable to the pair state that generated it.
4. **Factorization (unimodular recurrences).** Joint ancestor sets factor as (T-ancestors) x (recurrence chain): |anc| = |T-anc| (k+1). Exhaustive on all pair states <=300 (Fibonacci-type, Pell-type) and triple states <=40 (tribonacci-type): 0 failures in 244,000 states; fails for non-unimodular a->2a (1908/5000) and a->3a (821/5000).
5. **Sunflower.** For coprime a,b and any h: W(ha), W(hb), W(h(a+b)) pairwise intersect exactly in W(h). The "emergent" words of the sum are a disjoint petal W(hc)\W(h), identical for every coprime split of c.
6. **Controls.** Matched integers: Fibonacci terms F_4..F_60 are active in 22.8% vs 39.0% for integers of matched magnitude; Lucas 28.1% vs 40.0% (full panels n<=84: 21.7% and 28.9%). Among the coprime splits (a,c-a) of c=F_n the Fibonacci split gives the unique maximal recurrence chain (n-2) for n=6..23 (classical Euclid/Lame extremality).

## Boundary
All results follow from linearity plus SCG-01 (W(x)∩W(y)=W(gcd)); equivariance holds for any scalar-multiplication grammar (doubling, tripling), so only the alphabet gating is UNNS-specific. No evidence of a UNNS-specific feature of the sequence-generating mechanism.

## Run (Python 3.10+, standard library only)

    py -3 scripts\run_sib.py      (about 1 minute)
    py -3 scripts\verify_sib.py   (independent; trial division + forward closure)

`scripts/arithmetic.py` is the v004 module, copied unchanged (sha256 72eb2db749bdf930...). The verifier does not import it.
Outputs: results/summary.json, petal_table.csv, same_sum_control.csv, product_formula_failures.csv, verification_results.json.

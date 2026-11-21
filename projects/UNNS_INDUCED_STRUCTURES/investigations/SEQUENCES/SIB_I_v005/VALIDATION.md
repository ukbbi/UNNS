# SIB-I v005 - Validation
- run_sib.py computes results from arithmetic.py (v004 module, unchanged). verify_sib.py recomputes with trial division and forward closure (no imports of arithmetic.py or run_sib.py): V1 sunflower on a fresh sample; V2 product formula by forward closure (Fibonacci/Pell boxes 120, tribonacci 30) and reproduces the stored failure counts for a->2a, a->3a; V3 commutation; V4 gcd invariance; V5 petal table (696 rows) by trial division; V6 same-sum control; V7 activation n<=40.
- Expected final line: SIB-I v005 VERIFY PASS.
- Not checked: other recurrence orders, non-unimodular order>=2 steps, terms beyond the declared panels (F_n, L_n for n<=84).

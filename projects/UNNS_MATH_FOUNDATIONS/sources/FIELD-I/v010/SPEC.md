# SPEC — FIELD-I v010
Question: can two distinct primes p != q both carry infinitely often in a persistent orbit of the collective map C (G = g, x = gamma L^2/g)?
Method: (1) restate T53-T56 as an exact deterministic scheduler (T59): at gamma = 1 the prime with the smallest pending carry p^j fires; (2) prove that in this scheduler the odometer with the largest worst-case pending carry always starves (T60);
(3) test the scheduler against the residue machine, exhaustively on abstract odometers, on odometers built from the arithmetic of g (Abs_p from the definition), and on random/adversarial real orbits closed by the T51 class-closure certificate.
Verdict tags: ABSTRACT_COEXISTENCE / ARITHMETIC_REALIZABLE / COLLECTIVE_CERTIFIED / EXCLUDED / UNRESOLVED.
Files: field10.py (verifier), THEOREMS.md, RESULTS.md, CONTEXT.md, RUN_TESTS.bat, q11_certificate.py, output/.

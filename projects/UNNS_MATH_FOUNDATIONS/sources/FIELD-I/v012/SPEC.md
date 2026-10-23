# SPEC — FIELD-I v012
Question (O11.1, "effective predictability"): how far can the transient continue before the rigid regime is certified? Not the exact time -- an explicit bound that depends on finite initial arithmetic data (g0, gamma0) only.
Method: (1) T69: reset-descent bound from T54, sharpened to kappa(gamma0) (iterations of f(a) = floor(a/4)+1) and shown attained; (2) T70: class counting (T51) after the first reset, entry index <= H(g)-1, certified entry state for prime g (T66 necessity);
(3) T71: epoch structure of the carry scheduler (L1 reduction, L2 frozen competitor, potential Phi) giving a cubic bound K_poly(g); (4) T72: chains of reducing events (strict divisor chain, gamma recursion g' (gamma_before+1)/g, G = 1 tail via T32), total bound R(g0, gamma0).
Tests: arithmetic of kappa (exhaustive), T54 inequality and K_reset <= kappa on thousands of exact machine starts with gamma0 up to 1e9, sharp witnesses re-run by exact iteration of C, class-entry/H/K_poly on prime-g reset seeds (random + adversarial competing),
epoch lemmas L1/L2/Phi/saturation, exact general stepper vs independent direct iteration, chain/segment/gamma-recursion/tail/total inequalities on thousands of orbits from composite/even g0, end-to-end certification of final cycles, scope data for composite g, controls.
Files: field12.py, THEOREMS.md, RESULTS.md, CONTEXT.md, RUN_TESTS.bat, output/.

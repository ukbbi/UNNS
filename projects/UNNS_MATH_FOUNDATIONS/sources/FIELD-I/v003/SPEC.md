# FIELD-I v003 — Collective Growth and Interaction Grammar (SPEC)

Decision recorded (research, not theorem): keep G1–G3 as an *experimental* grammar. Adopt **G1-C** (collective interaction), **G2 j=1** (first meeting, an added axiom) and **G3-V** (value output) as the primary model for iteration; keep **G1-R** as a comparison model, **G3-F** (fibre output) for structural-information questions, **G3-O** (occurrence output) unresolved. C is not claimed to be privileged by UNNS.
FIELD-I v001, v002, the standalone G1–G3 memo, manuscript v3 and SELECT-I/II are **unchanged**.

## Objects
C(x) = x + Δ_coll(x) = x(1+1/γ(x)), Δ_coll = lcm(d_i²)/gcd(N_i) over D(x) (v002 T8); orbit x_{n+1} = C(x_n); x_0 any realised value (R ≥ 1).
Growth event: D(x_{n+1}) ⊋ D(x_n). T(x) = least k ≥ 1 with D(x_k) ⊋ D(x).

## Tasks
- H1 formalise unbounded fibre growth along C-orbits; quantitative bound on the time to the next growth event.
- H2 test whether the non-rigidity of three-route rendezvous graphs follows from an exact arithmetic restriction.
- H3 maintenance: erratum to "only γ matters"; launcher runs field2.py, g_checks.py and field3.py.

## Verifier (field3.py)
Exact Fractions/integers. Independent construction: box enumeration + brute-force common-future search (H0.1). Tags PASS/FAIL/DATA/OPEN; exit 0 iff no FAIL. FIELD3_QUICK=1 shrinks bounds.

# ANS-I v001 — History Dirichlet structures of UNNS nesting generation

**State:** complete research release, awaiting review; not frozen.

## Run
    RUN_WINDOWS.bat            (Windows; stages A-C, ceiling 100,000)
    RUN_WINDOWS.bat E          (ceiling 10,000,000; about 1 GB of memory)
    python verify.py --stage E  (any platform)

Python 3.8 or newer, standard library only. `figures/make_figures.py` additionally needs matplotlib and is not part of verification. Outputs are rewritten in `results/`.

## Main results
1. Z_H(s,t) = zeta(s) G(s,t); more generally the series over all actual histories is zeta(s+u) F(s,u,t).
2. G(s,1) and Z_H(s,1) have abscissa sigma_c = 1.5463810..., the root of sum_N (N/(N+1)^2)^sigma = 1.
3. The histories from any single source, already from 1, number X^(sigma_c + o(1)) up to endpoint X.
4. Each fixed depth converges down to 1/2; depth two continues past it with a double pole of coefficient kappa/4, and A_2(X) ~ (kappa/2) sqrt(X) log X.

## Files
| File | Content |
|---|---|
| PLAN.md, THEOREMS.md, PROOFS.md | specification, register, proofs |
| generative_record.py | nesting, ordered histories, records (w,K,Q,E), source orbits |
| endpoint_engine.py | forward minimal-endpoint enumeration |
| ancestry_engine.py | backward ancestry enumeration |
| mobius_check.py | inversion and engine comparison |
| prime_dynamics.py | prime-coordinate law, drift and saturation |
| dirichlet.py | zeta, boundaries, depth-two analysis |
| grammar_controls.py | cross-grammar controls |
| verify.py, tests/, RUN_WINDOWS.bat | verification |
| results/ | machine-readable counts and check records |
| figures/, report/ | figures and research report (LaTeX and PDF) |

`generative_record.py` is an addition to the specified file list; it carries the preservation requirements.

## Acceptance register
| Criterion | State |
|---|---|
| Eight initial results formally proved and registered | Met (review pending) |
| Forward and backward engines independently agree | Met, all depths, n <= 10^7 |
| Depth-resolved Moebius inversion verified | Met |
| Prime-coordinate evolution verified | Met, words with E <= 10^5 |
| Nonmultiplicativity characterized by exact witnesses | Met (H, a, H_1..H_6) |
| Absolute-convergence bounds established | Met; sharp for t = 1 |
| Cross-grammar controls completed | Met, ceiling 2*10^4 |
| Endpoint census through at least 100,000 | Met, through 10^7 |
| Reproducible Windows runner operational | Written; NOT_RUN on Windows (verification ran under Linux) |
| Research report and open-problem register produced | Met |

## Limits of the evidence
Finite checks do not prove the infinite statements. The boundary constants are floating-point evaluations with analytic tail bounds, not interval arithmetic. Source-one and total counts approach the exponent sigma_c slowly (0.91 and 1.04 at X = 10^7); the limit rests on the proof.

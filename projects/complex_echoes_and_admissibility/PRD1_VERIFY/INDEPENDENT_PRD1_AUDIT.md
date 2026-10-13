# PRD-1 independent verification — 2026-10-13

## Sources and independence
- Source: user-provided `ESC_I(2).zip`; original project unchanged.
- A new standalone `independent_check_prd1.py` imports neither `admissibility.py` nor `esc_i.py`, uses independent Python `random.Random(20261014)`, uses exact `fractions.Fraction`, and implements projection maps and predicted classes separately.
- Fresh sample: 400 cases per projection family, 2,400 total.

## Fresh check outcome
| Family | Cases | Claims | Abstain | Contradictions / linear mismatches |
|---|---:|---:|---:|---:|
| Dead-zone | 400 | 400 | 0 | 0 |
| Clipping | 400 | 400 | 0 | 0 |
| Lattice rounding | 400 | 325 | 75 | 0 |
| State-gated | 400 | 400 | 0 | 0 |
| Linear P | 400 | 400 controls | 0 | 0 |
| Linear Q | 400 | 400 controls | 0 | 0 |

The independent checker uses exact rational iteration over 200 steps for nonlinear falsification, and compares the linear controls with directly derived, closed-form coordinate recurrences over 12 steps. These finite tests establish no asymptotic theorem by themselves.

## Mathematical review of rule statements
- **Dead-zone:** If `|lambda*u0| >= theta`, the expanding coordinate is never removed, so divergence follows for `|lambda| > 1`. Otherwise its first projected value is zero forever. The second coordinate evolves as `mu^n*w0`; zero, convergence, boundedness, and divergence branches follow from `|mu|` and `mu*w0`.
- **Clipping:** `Pi` has image in `[-c,c]^2`, yielding immediate uniform boundedness for every subsequent iterate.
- **Lattice rounding:** Coordinatewise rounding has error at most `h/2`. If an expanding coordinate starts above `h/[2(|lambda|-1)]`, the reverse triangle inequality yields strict growth and eventual divergence. The initial-collapse clause is safe at strict inequality. If the expanding coordinate is erased and `|mu|<=1`, rounded multiples of `h` cannot increase in magnitude under subsequent steps, giving the stated bound.
- **State gate:** The criterion compares `|lambda*u|` against `|mu*w|` at the first step. If the expanding coordinate survives, dominance increases because `|lambda|>|mu|`, so it is never gated. Otherwise it is zero from that step onward and the other coordinate follows `mu`.
- **Linear controls:** `LINP` evolves, after step 1, as `(0, mu^(n-1)*(a*lambda*u0+mu*w0))`; `LINQ` evolves as `(lambda^(n-1)*(lambda*u0+b*mu*w0),0)`. Therefore they reduce exactly to linear matrix iteration and earn no nonlinear credit.

## Audit of reported prior runs
The bundled report records 4,197 nonlinear cases, R: 3,978 predictions (3,159 labelled asymptotically confirmed and 819 finite-horizon-consistent), 219 abstentions, and no contradictions. It also preserves 144 linear control contradictions in the frozen first-run comparator and a separately labelled post-hoc corrected mapping with zero contradictions. The earlier AR-3.1 material is not modified here.

## Qualifications / outstanding checks
1. This independent verification uses a distinct sample design and seed, rather than reconstructing the exact original 5,637-case PRD-1 sample. Thus the precise reported case counts, hashes and timestamp ordering remain archive records rather than independently reproduced facts.
2. The first-run protocol's strict success criterion remains false; the amended criterion is a separate post-hoc result. Avoid rewriting the history as a frozen pass.
3. The chamber report's `CONFIRMED_ASYMPTOTIC` is an evidence label that relies on selected analytical certificates, not a formal proof-checker for every rule. Especially, 819 rule predictions in the original study remain explicitly finite-horizon consistent only.
4. The comparator C intentionally has only error-bound information for nonlinear projections. The larger coverage of R should not be interpreted as superiority over a classical analyst given full definitions of the same projections.
5. To close at formal theorem level, write concise propositions with their exact hypotheses and proofs; optionally re-run the fixed comparator mapping on another fully preregistered fresh sample.

## Verdict
**Independent corroboration PASS within the stated diagonal spectral-frame families, with qualifications.** No independently detected contradiction in 1,525 nonlinear predictions or 800 linear reductions on 2,400 fresh cases. This is not a universal projection-persistence theorem or a verified computational advantage over equally informed classical analysis.

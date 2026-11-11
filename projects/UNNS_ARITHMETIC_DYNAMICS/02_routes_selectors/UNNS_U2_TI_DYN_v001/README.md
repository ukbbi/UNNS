# UNNS-U2-TI-DYN v001

**Maximal-Neighbor Dynamics and Prime-Degree Rigidity in the Reversible SELECT-II Arithmetic Graph**

Separate research addendum to the frozen `UNNS_U2_TI_v001.zip`.

## Main proved statements

For the graph with vertices positive integers and edges `k*N <-> k*(N+1)^2`:

1. The complete neighborhood of `x` is the disjoint union of forward neighbors `x/d*(d+1)^2` for `d | x` and inverse neighbors `x/q^2*(q-1)` for `q>=2` and `q^2 | x`.
2. The largest neighbor is `(x+1)^2`, uniquely attained at forward label `N=x`. Iterating this local rule from 1 gives `1, 4, 25, 676, 458329, ...`.
3. `deg(x) = tau(x) + #{q>=2 : q^2 | x}`. Equivalently, for `x=prod(p^e)`, degree is `prod(e+1) + prod(floor(e/2)+1) - 1`.
4. `deg(1)=1`, primes have degree 2, no vertex has degree 3, and composites have degree at least 4. Primality is exactly `deg(x)=2` for `x>=2`.

## Status and limitations

- All general statements have self-contained proofs in the manuscript.
- Exact-integer bounded checks support the proofs; no proof assistant has been used.
- The recurrence is previously recorded in OEIS A004019. **No claim of sequence novelty.** No comprehensive graph-theorem priority review has been performed.
- The original TI experiment did **not** count the post hoc nonlinear trajectories as preregistered successes; this addendum does not change that.
- Degree-based prime recognition is a structural graph invariant, **not** a computationally free prime test. Complete neighbor generation can require divisor enumeration.
- No prime-generation selector and no UNNS-wide universality theorem are claimed.

## Contents

- `manuscript/UNNS_U2_TI_DYN_v001.pdf` — citable PDF addendum
- `manuscript/UNNS_U2_TI_DYN_v001.tex` — editable LaTeX source
- `figures/degree_gap.pdf`, `.png` — chart for the degree theorem
- `code/verify_dyn.py` — standalone, dependency-free exact verifier
- `reports/verification_report.json` — machine-readable verification result
- `PROVENANCE.json` — baseline archive fingerprint and status
- `SHA256SUMS.txt` — file hashes

## Reproduction

From the root of this release:

```bash
python code/verify_dyn.py reports/verification_report.json
cd manuscript
pdflatex -interaction=nonstopmode -halt-on-error UNNS_U2_TI_DYN_v001.tex
pdflatex -interaction=nonstopmode -halt-on-error UNNS_U2_TI_DYN_v001.tex
```

## Frozen baseline

Source archive `UNNS_U2_TI_v001.zip`, SHA256: `8eb9dc9a66bae45992fd7034f9d31677a01902094ce32b8789f5ae77e4b7bcca`.
Original archive is **not modified** and is **not embedded** in this new package.

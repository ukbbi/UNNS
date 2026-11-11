# UNNS-U2-FP-SYM v001

Symbolic certificates for bounded Fibonacci routes in the reversible SELECT-II graph.
Supplement to UNNS-U2-FP v001 (which is **unchanged**). Author line: UNNS Research Collective.

## Result in one paragraph
All 12 residue classes of k modulo 12 now have an exactly certified route from F_k to F_(k+1) of at most 12 moves
(lengths per class are in `manuscript/class_table.tex` and Fig. 1), so d(F_k, F_(k+1)) <= 12 for every k >= 2.
The three families found in U2-FP v001 (k = 4, 7, 10 mod 12) are proved; family k = 4 also has a hand proof (Theorem 3).
Under the reading of R3 stated in Section 6 of the manuscript, the pieces assemble into a finite-control Fibonacci
successor selector (99 path states). Routes are NOT shown to be shortest (exact distances for k <= 29 are 2..6).

## Contents
- `UNNS_U2_FP_SYM_v001.pdf` - manuscript (also `manuscript/`, with LaTeX sources, figures, generated tables)
- `code/` - exact library (`u1_bnd_lib.py`), search (`fibparam.py`, `fibsearch2.py`, `deep*.py`), certifier (`fibcert*.py`),
  selector simulation (`fibrecov.py`), verifier (`verify_u2_fp_sym.py`), builder (`build_symfp.py`)
- `data/` - `class_paths.json` (the 12 routes as found), `class_certificates.json` (states and labels as ring elements),
  `small_fib_paths.json` (exact distances and explicit paths, 2<=k<=29), `search_record.json`, `fibonacci_identities_raw.json`
- `reports/` - `verification_report.json` (deterministic), search logs `deep_*.log`, `family_certificates.json`

## Reproduce (about 3 minutes, Python 3.13, sympy, matplotlib, pdflatex)
```
cd code
python3 verify_u2_fp_sym.py --out ../reports/verification_report.json --data ../data
python3 build_symfp.py ../reports/verification_report.json ../manuscript ../data
cd ../manuscript && pdflatex UNNS_U2_FP_SYM_v001.tex && pdflatex UNNS_U2_FP_SYM_v001.tex
```
Verifier items: S1 closed forms (269 cases); S2 ring proofs of the three families with labels in x,y; S3/S3b ring certificate
per class and division-free step identities; S4 every step is an edge (independent predicate `is_edge`);
S5 end-to-end selector simulation from the integer alone (30<=k<700) and monotonicity of the recovery functions;
S6 exact small distances and explicit paths; S7 operation audit. Verifier SHA-256: `3ec2f6366a22735d3be8a328a744ccc3809a7868655c2225f81f3bf699f70f8d`.

## What is certified, what is only tested
- Exact computer-algebra certificates (SymPy, not a proof assistant): step identities in Q[b][a]/(a^2+ab-b^2-eps),
  integrality over a full Pisano period, positivity for b>=40, strict monotonicity of the state functions.
- Tested only: numerical replay (122 values of k per class below 1500), the selector simulation, monotonicity on 40..1999.
- Label interpolation used to find ring elements is a discovery device, not part of any certificate.

## NOT_RERUN
- The route searches (`fibsearch2.py`, `deep*.py`; minutes to about 20 minutes each, memory heavy). Their outputs are the inputs
  `data/class_paths.json`; logs are in `reports/`; the attempt history for class 11 is in `data/search_record.json`.
- The four inherited packages (frozen); SHA-256 of the archives as they were at the start of this work:
  - UNNS_U1_BND_v001.zip   912a068e2d26fb721c13d524f9bb18280e59a99fbafd79928781903c1c9d8e35
  - UNNS_U2_001_v001.zip   561a9558f713faa2905be18f2a6afc2d3aac6de955c58e73cace7051e057ca21
  - UNNS_U2_SQ_v001.zip    c13a9be6c9a3d1d9299a009ab08844a9840a8ec24236dd5da171806e14691733
  - UNNS_U2_FP_v001.zip    c8469e88b76c66b248c827f00edf6da07cb9af0d4daf14ed2db935951e89ee91

## Limits
No formal verification; no literature search for priority; the R3 reading (bisection on a polynomial in t and A(t)) may not be
the one intended by Definition 2.1; routes are upper bounds; prime generation is untouched.

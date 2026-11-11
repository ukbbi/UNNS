# UNNS-U2-KI v001 — Exact Knowledge Identities and Selector Reduction

Separate research addendum to UNNS-U2-FP-R3 v001. All earlier releases (U1-BND, U2-001, U2-SQ, U2-FP, U2-FP-SYM, U2-FP-R3) are frozen and unchanged. The R3 controllers are imported unchanged from `baseline_R3_frozen/` (hashes in the report); the optimized controllers are separate code in `code/ki_selectors.py`.

## Results
- KI-1: all 268 audited route steps (Fibonacci 99, squares direct 105, squares wrapper 64) re-derived symbolically; classification equals the R3 sample fits in every case. 186 steps have a certified state-only formula (48 constant, 63 affine, 75 one isqrt of an affine function of the state), including constant-sign certificates for the root branch.
- KI-2: for the other 82 steps the exact degree d of the label over Q(S) is computed (d>=3 for all). Ten unresolved Fibonacci labels: d in {8,10,10,10,12,12,12,14,14,16}; not in any radical tower over Q(S) (specialization certificate; standard theorem cited, not machine-checked). 72 further steps are excluded from "rational function" and "one square root" only; for 30 of them (d=4 or 8) the tower question was not analysed.
- KI-3: optimized controllers reproduce every baseline move and waypoint sequence on identical inputs (Fibonacci 900, squares 5,435 each, plus refusal tests); recoveries -38.4% / -77.8% / -92.4%; no input became more expensive. Fibonacci still needs bisection at 61 of 99 steps.

## Contents
- `UNNS_U2_KI_v001.pdf`, `manuscript/` (LaTeX source, tables, numbers.tex), `figures/`
- `code/`: `ki_core.py` (symbolic states/labels), `ki_ident.py` (exact identities, Sturm sign tests), `ki_degree.py` (exact degrees), `ki_run_ident.py`, `ki_run_degree.py`, `ki_selectors.py` (optimized controllers + comparison runners), `verify_u2_ki.py` (verifier), `build_ki.py`
- `data/`: `ki1_identities.json` (all coefficients), `ki2_degrees.json`, `cost_records_ki.json`
- `reports/`: `verification_report.json`, `verifier_stdout.log`, `timing_informational.json` (wall time, not part of the deterministic report)
- `baseline_R3_frozen/`: frozen R3 code and data (inherited route certificates, small tables)
- `SHA256SUMS.txt`

## Reproduce
    python3 code/ki_run_ident.py data/ki1_identities.json          # optional: regenerates KI-1 table
    python3 code/ki_run_degree.py data/ki2_degrees.json            # optional: regenerates KI-2 table (~4 min)
    python3 code/verify_u2_ki.py reports/verification_report.json data   # ~5 min; recomputes both and compares
    python3 code/build_ki.py reports/verification_report.json data manuscript figures
    cd manuscript && pdflatex UNNS_U2_KI_v001.tex && pdflatex UNNS_U2_KI_v001.tex
Requires Python 3 with SymPy 1.14, matplotlib; pdflatex.

## NOT_RERUN
The route certificates (`class_certificates.json`, `class_paths.json`, `small_fib_paths.json`) and the route searches that produced them are inherited from FP-SYM and are not recomputed here. The R3 audit table (`state_audit.json`) is read for comparison only.
Inherited package SHA-256:
- UNNS_U1_BND_v001.zip 912a068e2d26fb721c13d524f9bb18280e59a99fbafd79928781903c1c9d8e35
- UNNS_U2_001_v001.zip 561a9558f713faa2905be18f2a6afc2d3aac6de955c58e73cace7051e057ca21
- UNNS_U2_SQ_v001.zip c13a9be6c9a3d1d9299a009ab08844a9840a8ec24236dd5da171806e14691733
- UNNS_U2_FP_v001.zip c8469e88b76c66b248c827f00edf6da07cb9af0d4daf14ed2db935951e89ee91
- UNNS_U2_FP_SYM_v001.zip a614e196fa059bc58a7bea5bb3c616c8eaf0eead37945cb08bd56ecb982668c6
- UNNS_U2_FP_R3_v001.zip 3e0e27295c8a1189aff7c8d4f92678b2b34db75ae05e2d9ea5aa652764594923

## Limits and unverified assumptions
SymPy exactness and Sturm counts without a proof assistant; rank statements modulo 2^61-1; the tower exclusion uses a cited standard theorem (Dedekind/specialization); tower status of the d=4,8 steps not analysed; frozen U2-001 labels at non-shortcut wrapper steps use floating point (agreement observed to n=10^15, not proved); finite test ranges; cost counters are Python operation counts; no literature priority search; whether R3' is the intended reading of Definition 2.1 is a programme decision. Nothing here concerns primes or target-independent selection.

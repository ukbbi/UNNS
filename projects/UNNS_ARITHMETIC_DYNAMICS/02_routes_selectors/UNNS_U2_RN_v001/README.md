# UNNS-U2-RN v001 — Ranked-Neighbour Dynamics and Graph-Local Observability
Independent package. UNNS-U2-TI v001, TI-DYN v001 and earlier releases are untouched and not included.
Run verifier: `python3 code/verify_u2_rn.py reports/verification_report.json` (~4 min; needs sympy). Registered run: `code/rn_register.py` then `code/rn_run.py` (already executed; hashes in data/rn_registration.json). Build: `code/build_rn.py`, then pdflatex in manuscript/.
Certification policy: see manuscript RN-0. Undefined rank = stuck, never substituted.
Evidence labels: Proved / Verified-bounded / Registered observation / Exploratory / Prior art (manuscript Section 6).
Disclosures: rn_closed.orbit (registered, unused) can miss cycles shorter than four terms; verifier uses its own loop. One float exponent (.5) in rn_core.py line 9 (sieve bound), list re-verified exactly.
NOT_RERUN: nothing inherited; all numbers come from this package's verifier.

# UNNS_SCALE

Independent local research project on nested scales of the UNNS Substrate (see CHARTER.md).
Nothing here changes or publishes to GitHub.

```
UNNS_SCALE/
  CHARTER.md  PROVENANCE.md  REFERENCE_SURVEY_v001.md
  UNNS-SCALE-I/            first chamber
    SPEC_v001.md           gates, acceptance rules, next steps
    THEORY/UNNS_SCALE_I_THEORY_v001.md   theorems, proofs, status of every claim
    code/                  scale_lib.py, run_gate1/2/3.py, run_witness.py, verify_all.py
    results/               JSON outputs of the gates
    reports/               VERIFICATION_REPORT_v001.md
  SHA256SUMS.txt
```

Run everything: `python code/verify_all.py` (Python 3.9+, standard library; Gate 3 also needs numpy). About 10 seconds.

Headline results of v001: scale copy `x ↦ Bx` is an exact label-preserving isomorphism onto the induced subgraph on multiples of `B`; the exits from that copy are given exactly by the labels dividing `Bx` but not `x`; no quotient dynamics exists on the floor-projection outer coordinate; the copy is a thin skeleton (≈10⁻⁶ of the edges of the trillion window); shortcuts through off-lattice vertices exist and are certified in two cases.

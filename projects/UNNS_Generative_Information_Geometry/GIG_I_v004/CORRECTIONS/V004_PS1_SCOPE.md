# GIG_I_v004 — scope clarification for PS-1 and PS-4 (append-only)

Status: clarification only. No proof, computation, certificate or result file
of v004 is modified; THEORY/, RESULTS/ and CERTIFICATES/ are byte-identical.
Prompted by the independent v004 Mathematical Assessment.

## PS-1: what is and is not established

| Statement | Status |
|---|---|
| K_z | m and all three gates (roles 0, 1, 3) closed  =>  [z] != 0 in H_2(X; F_2) | [PROVED] (sufficient direction) |
| Gate 0 open  =>  z bounds (universal 34-face filling chain) | [PROVED] |
| Gate 1 open or gate 3 open  =>  z bounds | [FINITE-EXACT] only: no exception among the 18,998 census regimes containing z (labels <= 16); not proved in general |
| Full survival equivalence ([z] != 0  <=>  K_z | m and all gates closed) for arbitrary six-label content | [OPEN] |

PS-1 must therefore be read as a SUFFICIENT theorem. Any phrasing of PS-1 as an
"if and only if" / "exactly when" statement (including in the v004 delivery
message) overstates the proved content, except for the gate-0 direction.

## PS-4: scope

The exact existence criterion in PS-4 is proved for sources that satisfy the
PS-1 sufficient conditions (the hole-survival regime). It is not claimed for
every source whose complex has [z] != 0; whether the PS-1 conditions are
necessary for [z] != 0 is the open converse above.

## Related reading notes

- The 106 beta_2 > 0 regimes not explained by PS-1 are certified but only
  coarsely grouped (33 signatures); the signatures are not proved to be 33
  inequivalent mechanisms.
- The H_3 certificates (H3-1..4) and the census prediction are finite-exact;
  no dimension-raising theorem is claimed.
- Provenance: full runs were made under Python 3.13 (cloud); device checks
  under Python 3.10.12. The v004 tests do not rerun the external GEO-HD-1D
  engine.

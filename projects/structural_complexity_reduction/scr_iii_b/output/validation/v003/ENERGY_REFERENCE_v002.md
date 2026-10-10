# SCR-III-B Energy Reference Preflight v002

**Verdict:** `FORMULA_CROSSCHECK_PASS_FULL_REFERENCE_PENDING`

## Cross-language deterministic checks

| L | Spins | Pair coefficients | Max C++/Python coupling difference | Flip identity error | Ice ground? |
|---:|---:|---:|---:|---:|---|
| 1 | 4 | 6 | 5.2e-18 | 0 | False |
| 2 | 12 | 66 | 5.2e-18 | 3.47e-18 | False |
| 3 | 24 | 276 | 5.2e-18 | 4.34e-18 | not enumerated |

## Scope and limitations

- This is a deterministic, auditable C++ transcription of the original Dryad pair-coupling equation, compared with the independently written Python v001 expression. It is **not a comparison to energy output from the unmodified Dryad simulation**.
- The v001 non-ice ground states were reproduced using the Dryad coordinate orientation and sign convention in this harness, but physical identification of the normalized energy remains provisional.
- Direct full-reference validation, temperature normalization, H_full selection, interaction ranges, and 3×3 exact target solution remain open.
- No preregistration or physical-transfer outcome is claimed.

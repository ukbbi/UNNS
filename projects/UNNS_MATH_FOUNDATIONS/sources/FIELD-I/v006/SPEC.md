# FIELD-I v006 — G-Collapse and Arithmetic Phase Transitions

**Status:** stand-alone additive investigation; `v002`, `v003`, `v004`, `v005` and `synthesis/FIELD1_GRAMMAR_G1-G3_v001.md` are preserved byte-for-byte. Manuscript v3, SELECT-I and SELECT-II are not modified.

## Model

Original occurrence value: `S_N(M)=M(N+1)^2/N` for positive integers `M,N`. A rational value `x=a/b` (lowest terms) has fibre `D(x)={d>=2 : d^2|a, d≡1 mod b}`. For any realised value, `G(x)=gcd(d-1)`, `L(x)=lcm(d)`, `Δ=L²/G`, and `C(x)=x+Δ`.

`C` is an **experimentally adopted grammar extension**, not an intrinsically selected consequence of the original rule. Route-aware interactions remain separate controls.

## Investigation gates

- **K4:** Prove or falsify the universal assertion that all collective orbits reach `G=1`; identify modular obstructions and viable stable-`G` possibilities. Deliver partial exact theorems if no general proof exists.
- **K5:** Prove an exact finite upper bound on the length of a constant-fibre plateau while `G>1`, including parity-dependent formulas and bounded tests.
- **K6:** Establish the eventual three-step scaling identities for orbits that enter `G=1`, including multiplicity increments and reach-set counting.
- **K7:** Correct v005 T33's overstatement about zero density. Preserve its general non-universality conclusion.

## Acceptance discipline

- `PASS` = asserted finite check of a clearly stated proposition; a universal result requires an independent proof in `THEOREMS.md`.
- `DATA` = bounded observation not claimed as universal.
- `OPEN` = unresolved; do not mark it PASS.
- Use only exact rational arithmetic. No arbitrary floating-point equality.
- No edits to existing projects, prior FIELD-I releases, or GitHub.

## Reproduction

Open `FIELD-I/v006/` in Windows CMD and execute `RUN_TESTS.bat`. It runs earlier verifiers for regression (outputs stored only under v006/output) and then `field6.py`. To run only the new fast tests, execute `python field6.py`. Optional `set FIELD6_QUICK=1` for a shortened sample. New report: `output/field6_report.json`.

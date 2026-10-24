# The Mathematical Foundations of the UNNS Substrate — Volume II

**Collective Dynamics, Structural Rigidity, and Effective Predictability**
*From Generative Multiplicity to Exact Scaling and Arithmetic Certification*

Working manuscript, 23 October 2026. Theorem baseline: FIELD-I v012 (frozen) and the 128-record registry
(68 records assigned to this volume); reference collection `ukbbi/UNNS`, commit
`bb8b12d753c600c597feb00df17fe139c7cc65fa`, folder `projects/UNNS_MATH_FOUNDATIONS`. Nothing in that
collection or in the registry is modified by this package.

## Contents

| Path | Content |
|---|---|
| `UNNS_Math_Foundations_Vol_II.pdf` | the manuscript (7 chapters, appendices A–F) |
| `tex/` | LaTeX sources (`main.tex` builds the volume; generated tables `crosswalk.tex`, `deps.tex`, `audit.tex`, `checks_table.tex`) |
| `figs/` | the 13 figures (PDF and PNG) and `figdata.json`, the exact data behind them |
| `engine.py`, `engine_seeds.py` | exact arithmetic: direct iteration of the collective map, residue machine, carry-level predictor, odometer data, transient bounds |
| `check_volume_ii.py`, `checks_volume_ii.json` | verification suite (exact integer/Fraction arithmetic) and its recorded result |
| `mkfigs2.py` | regenerates every figure from exact orbits and tables |
| `gen_tables.py` | regenerates the crosswalk, dependency, audit and check tables and the two `.tsv` files |
| `witnesses.json` | sharp witnesses for the reset-descent bound, kappa = 1..11 |
| `registry.json` | read-only copy of the registry records used for the crosswalk |
| `THEOREM_CROSSWALK.tsv`, `AUDIT.tsv` | machine-readable crosswalk and proof-completeness audit of the 68 records |
| `SHA256_MANIFEST.sha256` | checksums of all files |

## Reproduction

```
python3 check_volume_ii.py          # full suite, fixed sample sizes; writes checks_volume_ii.run.json
                                    # (--record overwrites the archived checks_volume_ii.json)
python3 mkfigs2.py                  # figures (needs registry.json in the working directory)
python3 gen_tables.py tex/main.aux  # tables and .tsv files
cd tex && pdflatex main.tex && pdflatex main.tex
```

Python 3 with `matplotlib` and `numpy` is needed for the figures; the checks use only the standard library.

## Scope notes (also stated in the theorems)

* The principal bound of the dynamic-G theorem counts carry events; iterations follow from the plateau bound
  (at most 4g steps per plateau) and the G = 1 tail bound.
* The static survivor certificate is proved for prime g (or g with no prime factor <= m^2); it is not claimed for
  composite or even g (open problem O12.2).

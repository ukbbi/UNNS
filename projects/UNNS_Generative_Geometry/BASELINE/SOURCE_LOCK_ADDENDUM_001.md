# SOURCE_LOCK addendum 001 (2026-10-31) — Papers A and B now on GitHub

Read-only: `git fetch` and `git show` only. `SOURCE_LOCK.json` and `SOURCE_OVERLAP_MATRIX.tsv` are unchanged (HD-0 evidence, pinned at 343f9aef2b6697466058165c5fc2ddf0f00e882b).

New commit: `b238c5ec0ed015870c5e9f18579ac85f0c6a8ff6` (2026-10-30, "GEO-I: archive Papers A and B mathematical manuscripts"), 121 added files, nothing else changed since 343f9aef.
Paths: `projects/UNNS_Higher-Dimensional Geometry/Manuscripts/PAPER_A_manuscript_v1_2/` and `.../PAPER_B_manuscript_v001/` (extracted, not zipped).

| item | local zip (members) | vs GitHub b238c5e |
|---|---|---|
| Paper A v1.2 | 61 files | 57 byte-identical, including `tex/part1.tex` (SHA-256 40a7d674…, the d=1 remark of the erratum). Local-only: `PAPER_A_Arithmetic_Occurrence_Geometry.pdf`, `logs/verify_full.log`, `logs/verify_smoke.log`, `logs/realize.log`. GitHub-only: `PAPER_A_Arithmetic_Occurrence_Geometry_v1_2.pdf` (renamed PDF). No differing files. |
| Paper B v001 | 63 files | 56 byte-identical; 7 differ: `tex/part1.tex`, `tex/appendices.tex`, `tex/refs.tex`, `tex/main.pdf`, `PAPER_B_manuscript_v001.pdf`, `MANIFEST.sha256`, `VERIFICATION_REPORT.md`. |

Paper B direction of difference: the **local zip is the later text**. It adds §1.1 "Relation to arithmetic occurrence geometry", a terminology note in Appendix A, and a reworded Paper A reference; the local `VERIFICATION_REPORT.md` says no proof, theorem statement or computation changed. GitHub holds the earlier wording. I read only the text diffs of the four .tex/.md files; the PDFs and manifest follow from them and were not compared further. Scripts, certificates, logs and data are identical.

`MATH_FOUNDATIONS_REGISTRY/registry.csv` is still not in the GitHub tree (only an unrelated `source_registry.csv` under `regime_synthesis`).

Consequence for HD-0: none of the matrix rows change. The Paper A `part1.tex` rows now have a GitHub path at b238c5e with matching hash. Paper B is not cited by any matrix row, so its mismatch affects nothing there.

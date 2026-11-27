# UNNS Analytic Structures: reference collection v003

UNNS Research Collective. Built 27 November 2026.

## Scope
A consolidated record of Analytic Structures of the UNNS Substrate (ASUNNS) through **ANS-I v015**, **ANS-II v002** and **ANS-II-ND v003**, with the **Analytic Atlas**. Sequential ANS-I development is paused at v015. The catalogue, compendium and Atlas add no research result. The statements derived in `CROSS_STRUCTURES/` are new, unreviewed and not catalogued. The releases under `02_INVESTIGATIONS` remain the record.

v003 records ten review verdicts and the Atlas corrections of the review of 27 November 2026 (`PROVENANCE/REVIEW_CONSOLIDATION_v003.md`), restores two depth-two open questions, and adds the Cross-Structural Research Map. v002 recorded the foundational audit and added the Atlas.

## Navigation
| Start here | Content |
|--|--|
| `ATLAS/ATLAS.pdf` (entries in `ATLAS/entries/`) | The mathematics organized by phenomenon |
| `THEOREM_INDEX.md` | All catalogued results, with status, review code and source |
| `THEOREMS/COMPENDIUM.pdf` (also `.md`, `.tex`, `compendium.json`) | Standing definitions and statements copied from the proof files (review attribution standardised) |
| `CLAIM_BOUNDARIES.md` | What is established, under which hypotheses, and what is not |
| `DEPENDENCIES.md`, `DEPENDENCIES.json` | Citation-based dependency architecture |
| `PROOFS/` | Verbatim copies of proof files and release tables; classical source list |
| `OPEN_PROBLEMS/` | Conjectures and open questions |
| `BASELINES/` | Hashes of release archives and investigation files; index of computations |
| `PROVENANCE/` | Review records, audit reports, literature status, build program |
| `CROSS_STRUCTURES/` | Cross-Structural Research Map v001, with its proposal and finite checks |

## Three kinds of status
1. **Proof status:** whether a written argument or computation exists.
2. **Mathematical review:** who has checked it.
3. **Release and computational acceptance:** archive, execution checks, reruns.

A completed review does not complete an execution check, and a successful rerun does not prove a general statement. Literature novelty is a further, separate question.

## Rebuilding
From `PROVENANCE/build`, run `python3 -B build.py` (Python 3.8 or later, standard library only; it needs the surrounding project folders). `catalog.txt` holds identifiers, review codes, line ranges and dependencies; `atlas/` holds the Atlas text; `archive_records.json` holds the recorded facts about the release archives. PDF and LaTeX files are produced separately with pandoc and pdfLaTeX. The build rewrites generated files, so `PROVENANCE/MANIFEST.sha256` and the project `CHECKSUMS.sha256` must be regenerated after a change.

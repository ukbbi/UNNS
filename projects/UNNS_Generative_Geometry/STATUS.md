# GEO-HD-1 status — 2026-10-30

## Preflight disposition

**GEO-HD-1A — Mathematical preflight: PASS (internal exact verification).** **GEO-HD-1B — coupled-lattice geometry: OPEN.**

- PDF §2.2 previously displayed **4 selected** outgoing edges of 72. It has **12** total; the complete list is in `data/benchmark_72.json`.
- PDF §3's noncoverage example is a **trivial-relation-lattice origin-deletion obstruction, valid already for k=2**; it is not an intrinsically higher-dimensional obstruction. It persists in enlarged coordinate boxes under the coordinate-cell grammar.
- The `d=1` remark in Paper A v1.2 `tex/part1.tex` incorrectly claims coordinate parallelograms fill all of the hull when both box sides are >=2. The theorem explicitly assumes `d>=2` and is not changed. A proposed erratum is in `ERRATA/`.
- Exact SELECT-II transport identity has stronger content than fibre-preservation iff alone; but it is elementary arithmetic. This does **not** satisfy the new-theorem research gate.
- The parity-lattice family has genuine nontrivial congruence coupling, but **coverage and topology of its Graver-generated cells are not yet proved**.

## Frozen references

GEO-I v001–v012 and Papers A/B; SELECT-I/II/FIELD-I releases; Foundations Vol. I/II. No edits, renames, remote changes, or new paper are authorized by this package.

## Source-level cross-check

The attached pre-existing `ERRATA.zip` has a FIELD-I v012 F.T71 numerical erratum. It is retained as *read-only reference* and **must not be conflated** with the proposed Paper A d=1 erratum.

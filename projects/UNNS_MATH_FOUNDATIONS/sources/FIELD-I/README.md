# FIELD-I v001 — Rational Nest Fibres and Non-Anchor Structure

**Status:** runnable initial research release. F1–F3 mathematical arithmetic is established and tested; F4–F5 establish *limits and nonselection witnesses*, not a selected generative interaction.

This investigation uses the 2017 UNNS fixed-nest rule

`S_N(M) = M * (N+1)^2 / N`, positive integer modulus `M >= 1`, fixed nest `N >= 1`.

It extends the rational-occurrence analysis beyond integer anchors without altering RGG, SELECT-I/II, or the relational manuscript.

## Install and run (Windows 11)

1. Extract `FIELD1_v001.zip` into the parent `UNNS_ENTANGLE_I` directory; its root folder is `FIELD-I`.
2. Open `FIELD-I` and double-click `RUN_TESTS.bat`. It uses Python 3 via the `py -3` launcher, falling back to `python`.
3. Double-click `RUN_REPORT.bat` to regenerate reports and exact arithmetic witness tables.
4. Alternatively, from a terminal in this folder: `python field1.py` (both), `python field1.py --tests-only`, or `python field1.py --report-only`.

Requirements: **Python 3.10+** and Python standard library only. Nothing is downloaded, and no network or external dependencies are required.

## Frozen project structure

- `SPEC.md`: domain, requirements, success/failure criteria and scope.
- `THEOREMS.md`: statements and exact proofs.
- `RESULTS.md`: initial results, actual test findings and open obligations.
- `CONTEXT.md`: context handoff to another conversation.
- `src/`: independent mathematical implementation.
- `tests/`: unit tests including independent bounded enumeration and adversarial counterexamples.
- `field1.py`: deterministic run entrypoint.
- `output/`: generated reports, tables and witnesses, already populated on release.
- `synthesis/`: separate findings, limitations and scientific next steps.
- `manuscript/EXTENSION_NOTES.md`: potential later manuscript additions, no manuscript modification.
- `MANIFEST.json`: hashes and provenance for every included release file other than the manifest itself.

## Verification semantics

The test suite verifies concrete bounded cases and some exact arithmetic identities. **Proofs are in `THEOREMS.md`**; a passing finite test does not prove a general theorem.

A two-consecutive-value chart recovers `(M,N)` because its difference already encodes `N`. Such automatic label recovery is **not** accepted as discovery of a relational interaction.

Two deliberately proposed CAI binary operations satisfy identical simultaneous unary-successor covariance and agree within one nest, but differ between nests: this is a **nonselection witness**, not a physical or independently selected binary rule.

## Foundations and citations

Original fixed-nest sequence definitions: “Unbounded Nested Number Sequences” (2017-11-21, blogspot, preserved separately as `UNNS_from_blogspot.pdf`); proof and source status are not inferred from its historical date. Integer-anchor mathematical baseline: *Observable Equivalence and Relational Invariants in Recursive Generative Systems* (manuscript v3, Section 10–11). Earlier SELECT-II endpoint self-iteration is an **additional mathematical extension**, not the source definition used here.

No existing research package, GitHub repository, or manuscript was altered to create FIELD-I.

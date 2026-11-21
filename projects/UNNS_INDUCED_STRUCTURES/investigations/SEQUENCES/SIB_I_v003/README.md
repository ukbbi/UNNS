# SIB-I v003 — Recursive Predecessor Architecture

Separate research release, 2026-11-21. Prior v001 and v002 remain unchanged.
Research question: which predecessor information determines depth, route
multiplicity, and different-content common-source mergers?

## Run

Standard Python 3.10 or later, no external dependencies:

    py -3 scripts\run_sib.py
    py -3 scripts\verify_sib.py

The portable equivalent uses python in place of py -3. RUN_SIB.bat uses py -3.
The full run is a finite census, not a depth-capped sample. Read reports/RESULTS.md
and REGISTER.md after completion. Verifier counts appear in VALIDATION.md.

## Domain and representation

Targets are every integer from 1 through 65536, with all positive integer sources.
T_N(s)=s(N+1)^2/N, N divides s, remains fixed. Since T_N(s)>=4s, all histories
stay in the target interval and have length <=8. Empty histories are excluded.
For every target, complete forward and backward enumerations must agree as sets
of (source, ordered label word), not merely as aggregate counts.

An incoming edge at x corresponds to d>=2 with d^2|x, from x(d-1)/d^2 with
label d-1. All signature child collections are MULTISETS: repeated child
signatures remain repeated. Trees are unfolded; an ancestor reached by two
branches is copied in the tree, while the original network identifies its value.

## Signature ladder

| Name | Retained information |
|---|---|
| E0 | Sorted positive prime exponents of the current integer |
| E1, E2, E3 | Root exponents plus recursively decorated predecessor multisets |
| Efull | Exponent decorations recursively down to every predecessor leaf |
| Ufull | Full unlabelled unfolded predecessor-tree shape |
| length_profile | Number of histories of each positive length |
| source_spectrum | Sorted total route multiplicities per distinct source |
| content_spectrum | Sorted lists of content-class multiplicities per source |

Exact tuple interning assigns reproducible local integer IDs. IDs have meaning
only with results/signature_definitions.json; no cryptographic collision assumption
is involved in mathematical classification.

## Controls

Every signature class is an exhaustive reference group. Additional controls
intersect each class with bit-length bins. For each target, peers exclude that
target. Singleton classes have no comparison; coverage is reported. Class-size
and min/max metric ranges determine whether the signature suffices for that
metric on this finite domain. These are information-retention controls, not
independent causal tests or statistical significance estimates.

## Source/content recurrence

The generator also propagates counts indexed by source identity and commutative
label multiset. It does not store order in this representation, but preserves
how many ordered histories fall into each cell. It reproduces merger counts
exactly. Ordered-word enumeration is retained separately to verify it.

Full source integers are a convenient identity system. A consistent injective
renaming of sources leaves merger counts unchanged; preserving equality across
branches is what matters. No minimal sufficient representation is claimed.

## Evidence scope

Exact recursive formulas and explicit counterexamples have proofs in REGISTER.md.
E3 and Efull classify all tested metrics in this census. Their global sufficiency
for mergers remains open. Counterexample searches within a finite bound do not
settle that question. The content-spectrum's count sufficiency is an aggregation
identity, not an independent prediction of merger counts.

Output text is UTF-8/LF. MANIFEST.json contains release hashes and baseline ZIP
hashes. Existing investigations and GitHub are unchanged. Install alongside the
earlier releases at investigations/SEQUENCES/SIB_I_v003/.

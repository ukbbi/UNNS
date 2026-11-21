# Optional local root-register additions (apply only after local review)

This patch document does **not** modify the parent `UNNS_INDUCED_STRUCTURES` registers or archives. It records suggested lines to add manually after the v001 module is validated locally.

## Suggested addition to RESEARCH_REGISTER.md

`| FUG-I-v001 | Fibonacci induced transition geometry | Exhaustive 48-index search of SELECT-II paths of lengths 1..3: 8 labelled paths between 4 Fibonacci endpoint pairs; exact 5/8-to-36 reconvergence and 144 target histories; two simple arithmetic controls | VERIFIED-EXACT with independent backward oracle | Extend to larger indices and greater depth; search for all-index laws |`

## Suggested additions to THEOREM_REGISTER.md

`| FUG-T3 | No nonempty forward SELECT-II path from F_n to F_(n+1) or F_(n+2) for n>=1, by minimum factor 4 | PROVED — FUG-I v001 theory/THEOREMS.md |`

`| FUG-T4 | Exact predecessor enumeration P(y) enables a complete short-path search over any frozen positive-integer target window | PROVED — FUG-I v001 theory/THEOREMS.md |`

`| FUG-C1 | Exactly 8 paths of lengths 1..3 among 1..48 indexed Fibonacci observations, covering 4 pairs | VERIFIED-EXACT — independent forward and backward enumerators |`

`| FUG-C2 | 5 and 8 converge at non-Fibonacci state 36 and continue to 144; additional distinct paths exist via 20 and 32 | VERIFIED-EXACT — explicitly given label-word witnesses |`

## Manifest policy

The parent's old `MANIFEST.json` was built for its previous content snapshot. If updating the parent project files, rebuild the parent's manifest from the new complete local directory rather than editing stale size/hash records by hand. This FUG-I module carries its **own self-contained MANIFEST.json**.

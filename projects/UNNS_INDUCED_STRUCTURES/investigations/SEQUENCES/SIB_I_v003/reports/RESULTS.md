# SIB-I v003 вЂ” Recursive Predecessor Architecture

Complete census of all positive targets <=65536, with every admissible positive-length history. Forward and backward route sets agree at every target; the source/content recurrence agrees with explicit ordered-word enumeration.

## Classification

E0 is the sorted exponent list. E(h+1) retains the root exponent list and multiset of predecessor E(h) signatures. Efull recursively retains this decoration to all leaves. Ufull is the complete unlabelled predecessor tree unfolded without shared-source identities.

| Signature | Classes | Classes varying in route count | Classes varying in source count | Classes varying in different-content pairs |
|---|---:|---:|---:|---:|
| E0 | 145 | 107 | 107 | 88 |
| E1 | 1297 | 172 | 173 | 11 |
| E2 | 1534 | 7 | 7 | 0 |
| E3 | 1541 | 0 | 0 | 0 |
| Efull | 1541 | 0 | 0 | 0 |
| Ufull | 901 | 0 | 6 | 5 |
| length_profile | 873 | 0 | 18 | 6 |
| source_spectrum | 837 | 0 | 0 | 5 |
| content_spectrum | 842 | 0 | 0 | 0 |

Classifications use exact interned tuples, not probabilistic hashes. Zero variation is a finite observation unless a corresponding theorem is proved in REGISTER.md. Efull sufficiency for merger counts outside this domain remains OPEN.

## Explicit counterexamples

| Target | All routes | Distinct sources | Merger sources | Permutation pairs | Different-content pairs |
|---|---:|---:|---:|---:|---:|
| 100 | 9 | 7 | 2 | 2 | 0 |
| 896 | 9 | 8 | 1 | 1 | 0 |
| 300 | 10 | 8 | 2 | 2 | 0 |
| 14884 | 10 | 7 | 3 | 2 | 1 |

100 and 896 share Ufull; 300 and 14884 also share Ufull. All routes and the complete predecessor edges for these cases are exported. Matching a complete unfolded tree preserves depth and route counts, yet can lose convergence information and content distinctions. These named pairs need not share binary magnitude. Additional bit-length-matched counterexamples, where found, are in counterexamples.csv.

## Exact source/content recurrence

For each target retain a counter indexed by (source, label multiset). Each incoming edge appends its label to every predecessor content and contributes its direct one-step history. This computes exact multiplicities without retaining ordered words. Summing counters recovers route counts; grouping by source recovers merger multiplicities; splitting by content distinguishes permutation from different-content pairs. This is a sufficient representation, not a proven minimal signature.

## Controls and limitations

All targets in each signature class form an exhaustive finite control pool. A second analysis intersects classes with binary magnitude bins. For a target, its peers are the other members of its class; singleton classes have no controls. signature_controls.csv gives class sizes and metric ranges, and census.csv gives exact membership. There are no random trials or p-values. Matching on increasingly detailed recursively derived data is an information-sufficiency test, not independent causal evidence. The content-spectrum summary already encodes the partitions used in the merger counts; it is an exact aggregation, not a predictive discovery.

This release deliberately studies the predecessor architecture rather than ranking external sequences. The root and all sources remain ordinary positive integers in the unchanged grammar. Source identities affect merger classification; observed sequence multiplicities would form a separate layer.

The prior v001 and v002 releases are preserved; no GitHub changes are made.

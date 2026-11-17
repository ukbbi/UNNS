# Reference survey — `projects/` at commit cc77e91 (read-only)

| Collection | Size | Relevance to UNNS-SCALE | Used in SCALE-I |
|---|---|---|---|
| UNNS_ARITHMETIC_DYNAMICS | 663 files | Defines the graph, distances (U1-BND: sup d(n,n+1)=6), selectors (U2-001: sup d(n,2n)=5; U2-SQ: Scaling Lemma, power lifting), degree structure (U2-TI-DYN) | Yes: definitions, Scaling Lemma, degree formula, distance sanity value |
| structural_complexity_reduction | 6,964 files | Methodology for Gate 4: exact solver baselines, nulls, cost accounting. Warning case: contraction without target preservation (spin ice: 2,604 of 16,777,216 states; 10 of 26 targets retained) | Principle only |
| UNNS_Generative_Information_Geometry (GIG-INFO v004) | 617 files | Information recoverability: compact signatures need not recover topology (certified counterexample); recoverability on 609,983 arithmetic regimes | Not yet; relevant for "what is lost under π" |
| UNNS_Generative_Geometry (GEO-HD) / Higher-Dimensional Geometry (GEO-I) | 1,338 / 2,064 files | Occurrence geometry; candidate language for describing cross-scale (exit) structure | Not yet |
| UNNS_COMMON_REFINEMENT | 337 files | Route closure when several factorisations reach one endpoint; relevant to multiple nestings of 10^12 | Not yet |
| UNNS_MATH_FOUNDATIONS | 565 files | Frozen treatise and theorem registry; FIELD-I / SELECT definitions | Not yet |
| regime_synthesis, UNNS_YM_STRUCTURAL_SPECTRAL, complex_echoes_and_admissibility | 9,745 / 483 / 32 files | Physical/regime branches | Not relevant to SCALE-I |

## Findings that shape the plan
1. The Scaling Lemma already exists in frozen form; SCALE-I's new content is the converse (Theorem 2) and the exit law (Theorem 3).
2. SCR's standing lesson fixes the acceptance rule: reduction of size is never evidence of structural preservation; each preserved property needs its own test.
3. GIG-INFO v004 gives the information-theoretic vocabulary for Gate 3 follow-ups: what the outer coordinate `q` can and cannot recover.

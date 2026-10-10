# Pre-primary design audit

Before freezing v002 primary seeds, a non-primary audit was performed on five disjoint seeds: `2026100701`–`2026100705`, each with 10,000 P4 candidates.

The purpose was limited to two questions: does the source-equivalent target oracle produce a nonempty target population, and does the Python port remain deterministic? It was **not** used to tune G1–G4 or to select primary outcomes.

Frozen audit counts:

| Audit seed | Target-positive | G1→G4 survivors |
|---:|---:|---:|
| 2026100701 | 5252 | 775 |
| 2026100702 | 5294 | 791 |
| 2026100703 | 5297 | 806 |
| 2026100704 | 5243 | 809 |
| 2026100705 | 5271 | 813 |

The audit establishes a nonempty, nontrivial target and a strongly contracting gate chain. It also makes clear that exact preservation is not guaranteed by construction. No gate or target rule was changed after these audit results. Primary seeds `2026100801`–`2026100805` are disjoint and remained unevaluated when this preregistration was frozen.

# Controls — Phase 2

The same exact all-depth ancestry method was run on indices 1..84 for:

1. Fibonacci `F_1=1, F_2=1`.
2. Lucas `L_1=1, L_2=3`.
3. The shifted sequence `F_n+1`, retaining both indexed occurrences at 2.

| Sequence | Reachable endpoint pairs | Total routes, all lengths | Histogram by length |
|---|---:|---:|---|
| Fibonacci | 4 | 8 | 1:1, 2:4, 3:3 |
| Lucas | 3 | 3 | 1:2, 2:1 |
| Fibonacci+1 | 3 | 3 | 1:3 |

These finite controls show the count is sensitive to the external sequence. They do NOT establish a null probability, statistical significance, causal interaction, or universality. The 84-term samples have different arithmetic magnitude and multiplicity profiles; thus raw path counts should not be presented as a normalized empirical effect.

See `results/controls_84.json` for exact endpoint pairs and routes.

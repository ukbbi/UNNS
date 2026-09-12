# Adversarial Similarity Baseline Pipeline

This pipeline tests whether the `R_sim` similarity metric used in **Structural Universality Across Physical Systems** is genuinely discriminative or whether it compresses generic ordered sequences into high similarity.

## What it tests

It generates adversarial ladders:

- **R1** — uniform random gaps
- **R2** — heavy-tailed Pareto gaps
- **R3** — correlated random-walk ladders
- **R4** — shuffled real-gap controls, optional but strongest

Then it compares their CLE summary vectors against real domain summary vectors:

```text
(P_depth, sigma2_GR, frag_rate, adm_persist, aniso_persist)
```

## Recommended workflow

### 1. Generate adversarial ladders

```bash
python adversarial_similarity_baseline_pipeline.py generate \
  --output-dir ./adversarial_Rsim_test \
  --n-ladders-per-class 100 \
  --n-min 10 \
  --n-max 1000 \
  --seed 42
```

Optional R4 shuffled-real controls:

```bash
python adversarial_similarity_baseline_pipeline.py generate \
  --output-dir ./adversarial_Rsim_test \
  --real-ladder-dir ./real_ladders_for_shuffle \
  --n-shuffles-per-ladder 5
```

This produces:

```text
adversarial_Rsim_test/
  R1_uniform_random_gaps/
  R2_pareto_heavy_tailed_gaps/
  R3_correlated_random_walk/
  R4_shuffled_real_gaps/          optional
  adversarial_ladder_manifest.csv
```

### 2. Run CLE / STRUC-PERC on generated ladders

Evaluate every generated ladder using the same CLE v2.0.0 / STRUC-PERC-I settings used for the real manuscript.

Required output columns:

```text
item_id, group, P_depth, sigma2_GR, frag_rate, adm_persist, aniso_persist
```

The `group` column should be one of:

```text
R1_uniform_random_gaps
R2_pareto_heavy_tailed_gaps
R3_correlated_random_walk
R4_shuffled_real_gaps
helium
cosmology
neutrino
```

### 3. Create a real-domain summary template

```bash
python adversarial_similarity_baseline_pipeline.py template \
  --output real_summary_template.csv
```

Fill it with the actual domain vectors from the manuscript/CLE output.

### 4. Analyze similarity distributions

```bash
python adversarial_similarity_baseline_pipeline.py analyze \
  --real-summary ./real_summary_vectors.csv \
  --synthetic-summary ./synthetic_summary_vectors.csv \
  --output-dir ./adversarial_Rsim_report
```

Outputs:

```text
similarity_baseline_results.csv
similarity_baseline_diagnostics.json
all_summary_vectors_used.csv
```

## Pass/fail interpretation

The current manuscript’s real-real reference values are:

```text
helium-cosmology = 0.993
helium-neutrino = 0.901
neutrino-cosmology = 0.882
```

The metric passes the adversarial baseline if:

```text
median(random-real R_sim) < 0.80
```

It is borderline if:

```text
0.80 <= median(random-real R_sim) <= 0.85
```

It fails if:

```text
median(random-real R_sim) > 0.85
```

Additional severe failure condition:

```text
R4 shuffled-real vs original real > 0.85
```

That would suggest the metric mostly reads marginal gap statistics rather than structural order.

## Why this matters

If the adversarial baselines stay low, the manuscript’s `0.993` helium-cosmology similarity becomes much more meaningful.

If random or shuffled controls score high, the similarity metric must be redesigned before making strong structural-universality claims.

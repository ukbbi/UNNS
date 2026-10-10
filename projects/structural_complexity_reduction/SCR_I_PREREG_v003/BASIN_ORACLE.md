# Basin Oracle

Basin discovery is frozen from Chamber LIII's `clusterResiduals` geometry.

Normalized feature vector:

`x = (gamma0/2, beta/2, d/5, kmax/6, locality_score)`

Distance is Euclidean. Two target-positive candidates are neighbors when distance `< 0.25`. A density seed requires at least 20 neighbors. Expansion order follows candidate order, matching the pinned LIII implementation semantics.

The basin oracle is applied to **target-positive candidates only**, where target positivity comes from the unchanged independent viability oracle.

Preservation geometry:

- Basin recall: every baseline basin must remain represented.
- Minimum target survivors per basin: 20.
- Coverage: ≥95% of baseline basin members must lie within radius 0.25 of a target-positive SCR survivor in the same basin.
- Centroid drift: normalized distance between baseline and survivor centroids ≤ 0.125 (= half the frozen adjacency radius).
- Unclustered target fraction: ≤5%.

These thresholds were frozen using design-only seeds. Primary seeds were not inspected.

# TEL-FINGERPRINT-I — Teleportation Route Fingerprint Protocol

**Protocol status:** ENGINEERING PROTOTYPE — NOT YET REGISTERED  
**Chamber version:** `0.1.0`  
**Object:** four correction-conditioned teleportation routes  
**Primary ordering:** physical perturbation coordinate `lambda`

## 1. Question

> Do the four corrected Bell routes form one reproducible structural fingerprint class over a physically ordered perturbation axis, and where does that class first deform, bifurcate, or fragment?

This protocol treats teleportation as multi-route closure. Conventional quantum invariants supply physically defined coordinates; the chamber evaluates the relational identity and persistence of the four routes.

## 2. Included

- exact four-route grouping;
- physically normalized defect fingerprints;
- all six pairwise route distances;
- route-class topology at every `lambda`;
- closure persistence and bifurcation onset;
- repeated-realization identity retrieval when identifiable;
- route-label permutation invariance;
- deterministic `lambda` thinning;
- leave-one-coordinate-out sensitivity;
- explicit technical and scientific boundaries.

## 3. Excluded

- derivation of density, Choi, Kraus, or process matrices from counts;
- arbitrary matrix flattening;
- detector timestamp ladders;
- analyst-selected post-hoc coordinates;
- interpolation between missing perturbation levels;
- automatic physical naming of a threshold;
- claims of quantum advantage or universal transition.

## 4. Frozen fingerprint

For each route, the chamber constructs:

\[
\mathcal D_b(\lambda)=
[q_b,\delta_b,1-F_b,m_b,s_b,e_b,c_{1b},c_{2b},c_{3b},t_b],
\]

where:

- \(q_b=|p_b-1/4|/(3/4)\);
- \(\delta_b\) is the declared terminal closure defect;
- \(1-F_b\) is process infidelity;
- \(m_b=1-(P_b-1/4)/(3/4)\) is normalized Choi mixing;
- \(s_b\) is normalized Choi entropy;
- \(e_b=1-2N_b\) is Choi-entanglement loss from negativity \(N_b\);
- \(c_{ib}=|1-\sigma_{ib}|\) are PTM contraction defects;
- \(t_b\) is nonunital displacement.

Every coordinate is clipped to `[0,1]`. Equal coordinate weight is frozen for v0.1.0.

## 5. Primary distance

For routes \(b,c\):

\[
D(b,c\mid\lambda)=
\sqrt{\frac{1}{10}\sum_{j=1}^{10}
(\mathcal D_{b,j}-\mathcal D_{c,j})^2}.
\]

This is a relational route distance, not a Hilbert-space or diamond norm. Its interpretation is restricted to the locked fingerprint coordinates.

## 6. Route-class states

Default frozen thresholds:

```text
closed pairwise maximum   0.05
connected-graph edge      0.15
```

At each `lambda`:

- `CLOSED`: every pairwise distance is at most the closed threshold;
- `DEFORMED`: not closed, but the four-route graph is connected at the edge threshold;
- `BIFURCATED`: the graph has two or three components;
- `FRAGMENTED`: the graph has four singleton components.

The component-size topology is retained separately, such as `3+1`, `2+2`, or `2+1+1`.

## 7. Trajectory verdict

- `INITIAL_CLOSURE_NOT_ESTABLISHED`: the minimum-`lambda` state is not `CLOSED`;
- `ROUTE_CLASS_CLOSED`: every perturbation level remains `CLOSED`;
- `ROUTE_CLASS_PERSISTENT`: baseline closure is established and the graph remains connected, although it may deform;
- `ROUTE_CLASS_BIFURCATED`: at least one later level bifurcates and the final state is not fully fragmented;
- `ROUTE_CLASS_FRAGMENTED`: the final state is fragmented;
- `INSUFFICIENT_EVIDENCE`: fewer than two valid perturbation levels.

The chamber reports both first deformation and first bifurcation. It does not silently equate either with a physical phase transition.

## 8. Persistence coordinates

Every trajectory reports:

```text
minimum and maximum lambda
route-class diameter at every lambda
mean pairwise route distance
first deformation lambda
first bifurcation lambda
connected persistence fraction
diameter integral over normalized lambda span
maximum diameter slope
final topology
```

## 9. Identity retrieval

When at least two scenarios and two realizations per scenario share one exact `lambda` grid, each realization becomes a query.

Its fingerprint concatenates, at every `lambda`:

```text
10 route-centroid defect coordinates
10 route-dispersion coordinates
route-class diameter
mean pair distance
```

The reference for a scenario is the coordinate-wise mean of its other realizations. Features are standardized from the query's reference gallery only. Distance is equal-coordinate RMS. The chamber reports own-source rank, top-1, top-5, own/nearest-wrong ratio, and margin.

## 10. Controls

### Route-label permutation

Aggregate route-class results must remain identical when route labels are permuted. Failure is an engine error.

### Deterministic lambda thinning

Retain perturbation indices `0,2,4,...` and always retain the final level. Compare the full and thinned trajectory verdicts and onset coordinates.

### Leave-one-coordinate-out

Repeat the route-class analysis after omitting each of the ten fingerprint coordinates. A result dependent on one coordinate is reported, not repaired.

### Wrong-correction and classical controls

When present, these are analyzed as separate scenario/control classes. They are not merged into the corrected-route primary class.

## 11. Stop rules

Stop and assign `INVALID_INPUT` when schema, four-route completeness, physical ranges, physicality, uniqueness, or PTM ordering fails.

Do not adjust thresholds after seeing results. A later registered protocol may replace prototype thresholds only before confirmatory data are analyzed.

## 12. Required exports

```text
TEL_FINGERPRINT_I_RESULT_RECORD.json
TEL_FINGERPRINT_I_LAMBDA_SUMMARY.csv
TEL_FINGERPRINT_I_PAIR_DISTANCES.csv
TEL_FINGERPRINT_I_TRAJECTORY_SUMMARY.csv
TEL_FINGERPRINT_I_RETRIEVAL.csv
TEL_FINGERPRINT_I_CONTROLS.csv
```

## 13. Interpretation ceiling

A positive result supports a reproducible structural equivalence class under the declared fingerprint and controls. It does not establish that the chamber distance is a fundamental quantum metric, that a detected onset is a thermodynamic transition, or that teleportation is successful independently of conventional fidelity and physicality checks.
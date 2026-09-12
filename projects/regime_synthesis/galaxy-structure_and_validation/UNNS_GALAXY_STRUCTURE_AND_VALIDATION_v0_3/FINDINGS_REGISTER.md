# Findings register

## Interpretation principle

> **State what the data positively show. Add limitations where they matter. Do not let a limitation erase the finding.**

## F1. Galaxy-specific structural fingerprints are reproducible

Across five unchanged-ladder STRUC-I executions:

- top-1 source retrieval = **1.000**;
- top-5 source retrieval = **1.000**;
- median own/nearest-wrong distance ratio = **0.1179**;
- median ICC across ρ PC1–PC3 = **0.99985**;
- median top-five neighbour Jaccard = **1.000**.

**Finding:** the complete curves form stable galaxy-specific structural identities. Native chamber variation is much smaller than between-galaxy separation.

## F2. Fingerprint expression responds strongly to sampling and preparation

| Branch | Top-1 | Top-5 | Median own/wrong | Geometry-matched top-1 |
|---|---:|---:|---:|---:|
| Leave one radius out | 0.551 | 0.730 | 0.916 | 0.726 |
| Deterministic n=10 thinning | 0.165 | 0.314 | 1.835 | 0.347 |
| Fixed-count coverage | 0.050 | 0.198 | 2.138 | 0.256 |
| M/L sensitivity | 0.517 | 0.619 | 0.916 | 0.649 |

**Finding:** the fingerprint has a measurable transformation under point deletion, thinning, coverage change, and baryonic preparation. Gate C maps the response of the fingerprint to representation changes.

**Scope:** the current coordinates combine galaxy structure with the observational channel through which that structure is measured. The next step is normalization, not denial of the fingerprint.

## F3. The structural atlas is strongly organized

First-three-component variance:

| Channel | Variance retained |
|---|---:|
| ρ(κ) | **90.8%** |
| ν(Vκ)(κ) | **88.5%** |
| Aκ(κ) | **55.9%** |
| combined | **61.0%** |

**Finding:** ρ and ν form compact dominant response families, while Aκ carries a richer and more heterogeneous structure.

## F4. Chamber regime is a major atlas coordinate

Median ρ-PC1:

```
Stable Structure     -2.109
Weak Persistence     11.218
```

Median combined structural-PC1:

```
Stable Structure     -0.794
Weak Persistence      3.076
```

**Finding:** Weak Persistence is not a minor label variation; it is a pronounced multiscale response regime.

## F5. The atlas carries physical galaxy information

Selected Spearman alignments:

```
structural-PC2 vs effective surface brightness     +0.463
structural-PC2 vs 3.6 μm luminosity                +0.456
structural-PC2 vs flat rotation velocity           +0.404
structural-PC2 vs H I mass                         +0.391
```

**Finding:** a major structural coordinate organizes galaxies by broad physical scale, surface brightness, rotation, and gas content.

## F6. The atlas also records observation geometry

```
final ρ vs median ladder gap                       -0.541
structural-PC3 vs valid radial-point count          -0.493
vulnerability fraction vs median ladder gap         +0.455
```

**Finding:** the chamber is sensitive to how densely and over what radial structure a galaxy is measured. This supplies a second, observational layer of the fingerprint atlas.

## F7. Structural neighbours preserve conventional similarity

Median nearest-neighbour differences are smaller than all-pair medians:

| Property | Structural neighbour | All galaxy pairs |
|---|---:|---:|
| Hubble type | 2 | 3 |
| flat velocity | 62.7 km/s | 80.1 km/s |
| 3.6 μm luminosity | 37.3 × 10⁹ L☉ | 65.6 × 10⁹ L☉ |
| effective surface brightness | 275.1 L☉/pc² | 396.1 L☉/pc² |
| H I mass | 2.41 × 10⁹ M☉ | 3.80 × 10⁹ M☉ |

**Finding:** structural proximity is not arbitrary. The fingerprint atlas preserves recognizable galaxy organization while also revealing cross-class analogues.

## F8. Persistence, fragmentation, and connectivity are distinct

```
Stable Structure               110 / 121
Weak Persistence                11 / 121
HARD_FRAGMENTATION             103 / 121
FULL_PERCOLATION                17 / 121
Stable + HARD_FRAGMENTATION     94 / 121
```

All full-percolation cases reached connectivity only in the adaptive extension.

**Finding:** stable structural persistence can coexist with fragmentation and without native-range global connectivity. The chambers expose several independent dimensions of organization.

## F9. The tested static global gravity architecture did not transfer

Compact model comparison:

```
ordinary profile baseline M2 RMSE     0.188389
combined chamber M-IP RMSE            0.194554
relative change                       -3.272%
verdict                               NON_GENERALIZING_SIGNAL
```

Full-curve comparison:

```
aggregate improvement                  0.435%
positive folds                         1 / 5
bootstrap interval                    crossed zero
verdict                               WEAK_FOLD_DEPENDENT_FULL_CURVE_SIGNAL
```

**Finding:** one static whole-galaxy representation is not the correct transfer architecture for the structural fingerprints.

This result does not remove the structural signal: correct curve assignment beats shuffled assignment, and complete curves retain recoverable galaxy identity.

## F10. ρ is the leading transfer-sensitive channel

```
ρ(κ)    +1.142% aggregate; 4 / 5 positive folds
Aκ      +0.457% aggregate; 3 / 5 positive folds
ν       -1.516% aggregate; 1 / 5 positive folds
```

**Finding:** the channels are not interchangeable. ρ is the strongest candidate for a new local or regime-conditioned transfer experiment; ν is counterproductive for the present target; Aκ carries weaker transfer structure.

## Consolidated conclusion

The programme has gained:

- a reproducible galaxy structural fingerprint;
- a multiscale galaxy atlas;
- a measurable representation-response law;
- a separation of persistence, fragmentation, and connectivity;
- a verified distinction between identity and transfer;
- a clear next candidate in ρ-based local and regime-conditioned analysis.

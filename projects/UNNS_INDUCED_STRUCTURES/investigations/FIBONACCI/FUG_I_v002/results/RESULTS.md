# FUG-I v002 — exact finite results

**Experiment:** all directed SELECT-II ancestry paths for Fibonacci observations `F_1,...,F_84`, with all non-Fibonacci intermediate states allowed and no search-depth cutoff. Maximum integer target `F_84=160500643816367088`.

## Endpoint reachability

| Source | Target | Minimum length | Exact labelled routes |
|---|---|---:|---:|
| F3 = 2 | F6 = 8 | 1 | 1 |
| F3 = 2 | F12 = 144 | 3 | 3 |
| F5 = 5 | F12 = 144 | 2 | 2 |
| F6 = 8 | F12 = 144 | 2 | 2 |

Eight total routes, four distinct endpoint pairs. No additional Fibonacci-to-Fibonacci directed paths through index 84 even at arbitrary length. v001 found all eight already within its smaller search domain, but did not certify the absence of longer paths.

## Ancestral geometry

| Target | Backward height h | Nonempty ancestry routes | Distinct ancestor nodes, excluding target | Squarefree terminal roots |
|---|---:|---:|---:|---:|
| F12 = 144 | 3 | 15 | 10 | 4 |
| F24 = 46368 | 4 | 24 | 14 | 5 |
| F48 = 4807526976 | 4 | 49 | 26 | 8 |
| F72 = 498454011879264 | 5 | 40 | 22 | 7 |
| F84 = 160500643816367088 | 3 | 15 | 10 | 4 |

The root set of F12 is `{2,5,6,11}`. Its index-divisible successor F24 has an entirely different squarefree root set. What is preserved by scaling is the set of **labelled histories up to injective transport**, not root identities.

## F72 exact five-step witness

```
82416337943 --1--> 329665351772
            --2--> 1483494082974
            --6--> 12115201677621
            --7--> 110767558195392
            --2--> 498454011879264 = F72
```

The recorded labels are positive integers dividing each previous state. All steps are exact. This demonstrates that the ambient ancestry geometry can be deeper than the observed Fibonacci-to-Fibonacci links.

## Controls

| Indexed observation sequence | Reachable pairs | Total routes |
|---|---:|---:|
| Fibonacci | 4 | 8 |
| Lucas | 3 | 3 |
| Fibonacci+1 | 3 | 3 |

These counts are mathematical observations only, not significance tests. For full records see `controls_84.json`.

## Evidence status

- General arithmetic inverse, root characterization, finite-depth bound, multiplicity recurrence, scale lifting, gcd edge criterion: **PROVED** (mostly consequences/reformulations of existing SELECT-II / FIELD-I results).
- Census of 84 indexed Fibonacci observations and its 84-layer ancestry geometry: **VERIFIED-EXACT**, bounded numerical result, not a theorem about every Fibonacci index.
- Universal characterization of Fibonacci-to-Fibonacci reachability, infinite families of branching geometry, and physical or universal interpretation: **OPEN**.

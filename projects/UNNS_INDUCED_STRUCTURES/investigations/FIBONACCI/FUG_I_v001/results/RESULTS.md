# FUG-I v001 — Exact finite results

**Input:** Fibonacci indices `1..48`; positive integers `F_n`; selected `T_N(x)` for `N|x`. Paths use 1, 2 or 3 directed moves, with *all* positive integer intermediate states allowed. `F_1=F_2=1` remain distinct indexed observations. No external data or randomized choices.

## Incoming fibre geometry

- `48` indexed Fibonacci layers examined.
- `9` nonempty layers: `n=6,12,18,24,25,30,36,42,48`.
- `27` indexed occurrence points in total.
- Peak incoming fibre within this range: `R(F_48)=7`; `R(F_12)=R(F_24)=R(F_36)=5`.
- All `2,304` index-pair meet identities verified. These instances check a preexisting proved law, not a new theorem.

## Actual generative transition geometry

| Route length | Labelled routes | Distinct indexed pairs |
|---|---:|---:|
| 1 | 1 | 1 |
| 2 | 4 | 2 |
| 3 | 3 | 1 |
| **All** | **8** | **4** |

Complete route register:

| Source and target | Label word `(N1,...,Nell)` | Full ambient path |
|---|---|---|
| F3=2 to F6=8 | `(1)` | `2 -> 8` |
| F5=5 to F12=144 | `(1,5)` | `5 -> 20 -> 144` |
| F5=5 to F12=144 | `(5,1)` | `5 -> 36 -> 144` |
| F6=8 to F12=144 | `(1,2)` | `8 -> 32 -> 144` |
| F6=8 to F12=144 | `(2,1)` | `8 -> 36 -> 144` |
| F3=2 to F12=144 | `(1,1,2)` | `2 -> 8 -> 32 -> 144` |
| F3=2 to F12=144 | `(1,2,1)` | `2 -> 8 -> 36 -> 144` |
| F3=2 to F12=144 | `(2,1,1)` | `2 -> 9 -> 36 -> 144` |

The exact source-to-target counts are path counts, *not* incoming occurrence counts. Specifically `R(F_12)=5`, while there are `4` two-step paths from Fibonacci observations to `F_12=144` and `3` three-step paths from `F_3=2` to `F_12=144`.

## First finite geometry

The source-to-target network contains both a shared intermediate node `36` and alternative intermediate nodes `20` and `32`. The ambient node `36` is not a Fibonacci number: `F_9=34<F_10=55`.

Two consecutive Fibonacci values, `F_5=5` and `F_6=8`, *do not* connect directly to one another, but both generate the shared ambient state `36` using distinct labels. Hence we have a concrete substrate-mediated convergence, not a statement about the Fibonacci recurrence itself.

## Discrimination controls (same bounded algorithm)

| Independent indexed input | Direct routes | Two-step routes | Three-step routes |
|---|---:|---:|---:|
| Fibonacci F_n | 1 | 4 | 3 |
| Lucas L_n | 2 | 1 | 0 |
| Perturbed F_n+1 | 3 | 0 | 0 |

For `F_n+1`, the duplicate values at indices 1 and 2 are counted as distinct **indexed** observations. These are illustrative arithmetic controls, not matched statistical nulls or novelty evidence. Their different counts demonstrate sensitivity to the imposed sequence, not a physical effect.

## Evidence status

- **PROVED:** ambient monotonicity and finite search completeness, no SELECT-II forward paths between adjacent/next-nearest Fibonacci terms, inherited occurrence/divisibility theorems.
- **VERIFIED-EXACT:** 48-index finite route catalogue, 27 incidence points, 2,304 intersection checks, Lucas and F+1 finite controls.
- **PROPOSED:** treating the union of incidence, index transports, and ambient paths as one decorated "Fibonacci–UNNS induced geometry".
- **OPEN:** all-index edge and path classification, geometric invariants beyond the displayed bounded network, representation-stable predictions.

**Conclusion:** We have an exact induced structure with genuine branching, multiple legal histories and reconvergence, rather than merely a list of square divisors. The small finite network should be studied further without interpreting it as a hidden generative law for Fibonacci.

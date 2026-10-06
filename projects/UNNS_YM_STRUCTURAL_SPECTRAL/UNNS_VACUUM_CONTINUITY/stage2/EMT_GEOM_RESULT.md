# EMT_GEOM_RESULT.md

**Project:** `UNNS_VACUUM_CONTINUITY`  
**Stage:** 2  
**Branch:** Yanagihara EMT secondary geometry checks  
**Status:** **FROZEN — COMPLETE**  
**Frozen synthesis:** **GEOMETRY-ROBUST-NO-FLOOR**  
**Date:** 2026-10-05

---

## 1. Locked primary result

The primary Yanagihara EMT-I branch remains:

```text
R = 0.69 fm
EMT-UNCERTAINTY-LIMITED
```

Its four-component norm is vacuum-directed, while the frozen zero-floor versus positive-floor AICc comparisons remain below the decisive threshold.

This result is not rewritten by the secondary geometry checks.

---

## 2. Secondary geometry results

### R = 0.46 fm

```text
Outcome:
EMT-UNCERTAINTY-LIMITED

Four-component norm path:
VACUUM-DIRECTED

Tail coordinates:
156
```

Component checks:

```text
epsilon      UNCERTAINTY-LIMITED
sigma_zz     UNCERTAINTY-LIMITED
sigma_rr     UNCERTAINTY-LIMITED
sigma_theta  UNCERTAINTY-LIMITED
```

No component returned `NONZERO-FLOOR`.

### R = 0.92 fm

```text
Outcome:
EMT-UNCERTAINTY-LIMITED

Four-component norm path:
VACUUM-DIRECTED

Tail coordinates:
88
```

Component checks:

```text
epsilon      NONMONOTONE
sigma_zz     UNCERTAINTY-LIMITED
sigma_rr     UNCERTAINTY-LIMITED
sigma_theta  UNCERTAINTY-LIMITED
```

No component returned `NONZERO-FLOOR`.

---

## 3. Frozen geometry synthesis

The secondary branch satisfies the preregistered condition for:

```text
GEOMETRY-ROBUST-NO-FLOOR
```

because:

1. both secondary four-component EMT norms are vacuum-directed;
2. neither secondary geometry returns `EMT-POSITIVE-FLOOR`;
3. neither geometry contains a component classified `NONZERO-FLOOR`;
4. the result is obtained under the same four-component norm, the same zero-floor / positive-floor model families, the same tail-sensitivity rule, and the same `|Delta AICc| >= 6` threshold used for the primary geometry.

The synthesis is therefore:

\[
\boxed{
R=0.46,\ 0.69,\ 0.92\ {\rm fm}
\quad\Rightarrow\quad
\text{vacuum-directed EMT structure with no detected positive structural floor}
}
\]

with the explicit qualification that all three source-separation branches remain uncertainty-limited with respect to a decisive asymptotic zero-floor proof.

---

## 4. Scope

`GEOMETRY-ROBUST-NO-FLOOR` is a structural statement about the published continuum, vacuum-subtracted EMT representation.

It does not establish:

- that the physical Yang–Mills Hamiltonian mass gap vanishes;
- that the mathematical Yang–Mills mass-gap problem is solved;
- that `D_struct -> 0` has been proven as a theorem;
- that every possible Yang–Mills representation must show the same behavior.

It does establish that the independent EMT representation does not reveal the positive structural exclusion floor required by the old universal non-crossability picture across the three tested source separations.

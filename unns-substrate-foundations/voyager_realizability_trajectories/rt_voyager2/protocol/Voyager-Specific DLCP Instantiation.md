# Voyager-Specific DLCP Instantiation  
## (Voyager Plasma Time Series → UNNS Ladder Family)

---

## Overview

This document instantiates the **Dynamic Ladder Construction Protocol (DLCP)** for the Voyager 2 Plasma Science (PLS) high-resolution dataset:

    VOYAGER2_PLS_HIRES_PLASMA_DATA_HSH

It defines the exact methodological steps required to convert raw spacecraft plasma measurements into **admissible UNNS ladders** and **trajectory-level structural objects**.

---

## 1. Data Source

Primary dataset:

- NASA CDAWeb  
- Voyager 2 Plasma Science (PLS)  
- High-resolution plasma data (heliosheath)

Reference:

    https://cdaweb.gsfc.nasa.gov/cgi-bin/eval3.cgi

Files:

    voyager2_pls_hires_plasma_data_hsh_YYYYMMDD_v01.cdf

Time range used:

    2007-08-27 → 2018-11-05

---

## 2. Available Observables

From CDF structure:

| Variable | Description |
|----------|------------|
| `V`      | Plasma bulk speed (scalar) |
| `V_rtn`  | Plasma velocity vector (RTN coordinates) |
| `dens`   | Plasma density |
| `T`      | Temperature |
| `w`      | Thermal speed |
| `Epoch`  | Time axis |

---

## 3. Primary Observable Selection

### Default ladder basis:

    x(t) = V(t)

Rationale:
- directly measured scalar speed
- no transformation required
- physically interpretable
- stable across dataset

---

## 4. State Construction

A state is defined as:

    S(t, Δ) = { V(t_i) | t ≤ t_i < t + Δ }

Where:

- `Δ` = fixed time window
- `t_i` = measurement timestamps

---

## 5. Window Specification

### Recommended baseline:

- Window size:  
      Δ = 512 – 2048 samples

- Step size:  
      Δ_step = Δ / 4 (overlapping windows)

---

## 6. Stationarity Enforcement

Each window must satisfy:

- no abrupt jumps in V(t)
- bounded variance
- absence of strong discontinuities

Optional operational checks:

- rolling variance threshold
- outlier density check

Non-stationary windows must be discarded.

---

## 7. Data Cleaning

For each window:

Remove:

- NaN values
- fill values (from CDF attributes)
- extreme outliers (instrument artifacts)

Constraint:

    |S_valid| ≥ 0.95 · |S_raw|

---

## 8. Ladder Construction

After filtering:

    L = sort(S_valid)

This produces a valid UNNS ladder.

---

## 9. Ladder Normalization (optional)

Two valid modes:

### Raw mode (default)

    L = sort(V)

### Normalized mode

    L = sort( (V - mean(V)) / std(V) )

Constraint:

- Do not mix modes within the same experiment.

---

## 10. Ladder Family

Full dataset produces:

    𝓛 = { L₁, L₂, ..., Lₙ }

Each ladder:

    L_i = ladder from S(t_i, Δ)

---

## 11. Derived Structural Quantities

Each ladder is evaluated via STRUC-PERC-I:

    L_i → (m(L_i), κ_conn(L_i), GR(L_i))

Where:

- `m(L)` = connectivity margin  
- `κ_conn` = connectivity capacity  
- `GR` = giant ratio  

---

## 12. Trajectory Interpretation

The ladder family defines:

    Γ = { (m_i, κ_i, GR_i) }

This is a **trajectory in realizability space**.

---

## 13. Physical Interpretation

### Velocity ladder:

- macroscopic plasma flow structure
- solar wind / heliosheath dynamics

### Density ladder:

- compression / rarefaction regimes

### Temperature ladder:

- energy dispersion

### Thermal speed ladder:

- turbulence / microstructure proxy

---

## 14. Multi-Observable Extension

Independent ladder families:

    𝓛_V, 𝓛_ρ, 𝓛_T, 𝓛_w

These define:

    multi-chart embedding of the same physical system

---

## 15. Expected Structural Regimes

Typical observed transitions:

    FULL → GIANT → TAIL → GIANT → FULL

Interpretation:

- shocks
- heliopause crossing
- plasma regime shifts

---

## 16. Resolution Dependence

Window size Δ controls:

| Δ size | Effect |
|------|--------|
| small | noisy, high-resolution dynamics |
| large | smoothed, stable regimes |

This directly manifests:

    Dual Observability (Theorem-level behavior)

---

## 17. Critical Constraints

The following must be enforced:

- fixed window size
- single observable per ladder
- stationarity per window
- filtering before sorting
- consistent ladder size

---

## 18. Known Limitations

- temporal coverage gaps
- instrument noise
- heliosheath regime complexity
- resolution dependence of classification

---

## 19. Extension Path

This dataset enables:

- dynamic manifold exploration
- regime transition detection
- boundary tracking in time
- multi-chart canonicalization

---

## 20. Status

This instantiation represents:

    first dynamic DLCP application on real spacecraft data

within the UNNS Substrate framework.

---

## 21. Next Steps

- extract ladders for V(t)
- run STRUC-PERC-I per ladder
- build trajectory Γ
- compare across observables
- integrate into Local Geometry manuscript

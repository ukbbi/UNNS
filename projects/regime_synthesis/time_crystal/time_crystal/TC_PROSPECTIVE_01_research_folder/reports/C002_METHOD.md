# TC_P01_C002 v001 — Adapter Method

## Candidate type

C002 is a **numerical quantum-many-body prospective candidate**.

It is not represented as experimental data.

## Source representation

Both source files contain signed:

```text
index, x, y, z
```

for source indices 0 through 300000.

## Frozen stroboscopic adapter

The source protocol uses `N=300`.

The adapter performs only:

```text
(x_t, y_t, z_t)
→
(x_{300n}, y_{300n}, z_{300n})
```

using source indices:

```text
0, 300, 600, ..., 300000
```

This yields 1001 stroboscopic observations.

## Adapter firewall

The adapter does not:

- provide the expected recurrence period;
- multiply by an alternating sign;
- align to a 2T template;
- Fourier filter;
- smooth;
- interpolate;
- choose a favorable subwindow;
- change qmax;
- change any TIME-CRYSTAL-I threshold;
- manufacture rigidity, collective, or spectral evidence.

## Blind IDs

Candidate:

```text
TC_P01_C002
```

Matched control:

```text
TC_P01_C002_CTRL
```

Ground truth is stored separately.

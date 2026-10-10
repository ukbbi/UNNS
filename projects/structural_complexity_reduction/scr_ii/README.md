# SCR-II Structure v001

## Purpose

SCR-II is the first cross-domain computational-transfer phase of Structural Complexity Reduction (SCR).

SCR-I established controlled mechanism-space compression with basin/class preservation above a representation floor. SCR-II asks a stronger question:

> Can a frozen UNNS structural filter reduce the search space of an unseen discrete problem family while preserving the complete exact solution set and lowering total downstream computational cost?

The first benchmark family is `ROUTE_CSP_I`: a layered binary route/CSP family with exact ground truth, a frozen route grammar, independent arithmetic solution constraints, matched nulls, and separate calibration/design/primary seeds.

## Placement

Merge the `scr_ii/` folder into the existing project root:

```text
structural_complexity_reduction/
├── scr_ii/
│   ├── benchmark/
│   ├── config/
│   ├── grammar/
│   ├── generator/
│   ├── solver/
│   ├── filter/
│   ├── nulls/
│   ├── analysis/
│   ├── schemas/
│   ├── scripts/
│   ├── tests/
│   └── output/
└── ...
```

The SCR-I v003 project remains frozen and is not modified.

## Execution philosophy

SCR-II separates five roles:

1. **Instance generator** — produces unseen route/CSP instances from frozen rules and seeds.
2. **Exact downstream solver** — defines ground truth independently of UNNS structural gates.
3. **UNNS structural filter** — prunes prefixes using only structural route metadata and the frozen grammar.
4. **Controls/nulls** — measure whether any advantage is more than generic pruning.
5. **Analysis** — evaluates exact solution preservation, node/leaf reduction, total cost, and scale transfer.

No primary seed may be used for calibration, threshold selection, grammar modification, or debugging.

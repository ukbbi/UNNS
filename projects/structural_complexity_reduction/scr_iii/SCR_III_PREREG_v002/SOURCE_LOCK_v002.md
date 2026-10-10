# SOURCE_LOCK_v002

**Phase:** SCR-III-A v002  
**Status:** `FROZEN_SOURCE_LOCK`  
**Frozen:** 2026-10-08

The following files are immutable inputs to `SCR_III_ENGINE_v002`. Preflight must recompute every hash before the acceptance-only preflight and again before audit.

## Frozen SCR-II v002 sources

| File | SHA-256 |
|---|---|
| `scr_ii/grammar/route_grammar.py` | `f0b855b8201a23ba6abb175b8b342627fd4e389fc41608fe7b3b27958946c1a0` |
| `scr_ii/filter/structural_filter.py` | `162d91a9e75af7c7569069ec8049c5089c555a003a04e8a718dc84776c5f5be6` |
| `scr_ii/solver/exact_solver.py` | `f981bc237e99e605ea66b93a5175e0145110a9cff02236c11cdc39ee486539b0` |
| `scr_ii/nulls/controls.py` | `83451edaa2c1da0657cf7a21394944541be7d6f7929e5aae50bcc677f7f0caf1` |
| `scr_ii/generator/route_csp_i_v002.py` | `9f7e38c95e00f930af437a92fca3981344acb888d6a8fdb754ee1d2bc4f88d98` |
| `scr_ii/engine_common.py` | `4bd542d52e236248d8453bf00e8871335eadf9df6def44ee312c258a56a40bfe` |
| `scr_ii/analysis/metrics.py` | `58ddf67184cd53794174d69aaf52c88777cdc9c5d2b6cbceec3c54b3836b9cfd` |
| `scr_ii/generator/route_csp_i.py` | `e38a89cb42e046604e065a3e1cdcc6a0306879b504bd91d5e65b97ab69e0bed6` |

## Immutable SCR-III v001 implementation reused by v002

| File | SHA-256 |
|---|---|
| `scr_iii/compat.py` | `7f8b1f969ee4b8dc2a092d065654fe9b5122b541362fabcf83905fcdf59a853d` |
| `scr_iii/engine_common.py` | `c6e595a2972fcad4b33a99c1566b7de560d5fae38fc16ea25bc32f26fbcbbcb9` |
| `scr_iii/generator/route_csp_c_v001.py` | `9cf6c4e60ac1cfbb9f5555613a368487bc169a37712ffe158ad7c2b6215d71c1` |
| `scr_iii/nulls/controls_v001.py` | `9295dd0e43e493f3ba7cf932e93d4c6f9f75eaa3c6ebb7d517aeb1cbe04ef608` |
| `scr_iii/analysis/metrics_v001.py` | `2006885ca614e6ab1a1c42b8f2b8954123082647960e8961b4bef49af3124054` |
| `scr_iii/analysis/estimators_v001.py` | `e919eb0af814b17b398769478023d550cca9c130354f0d5116ff1686f22efd28` |
| `scr_iii/analysis/structure_stats_v001.py` | `172d4a4bb8bc35914bc0e1c332c82992c49a1febda0ad3104dc4b71cfd0a0923` |
| `scr_iii/source_lock.py` | `4f75fd3dc227ba89f38115e66b990127ae1a4f9f81a6f69403bdc922c89fa7d9` |

`route_csp_c_v001.py` remains the benchmark generator in v002. There is no `route_csp_c_v002.py` unless the construction itself changes in a later specification.

Allowed new/changed executable code for v002 is versioned additively and is limited to:
- acceptance-only real-engine preflight runner;
- v002 audit runner/grid;
- realized-C trend/PG5a implementation;
- v002 primary verdict/consolidation logic;
- v002 seed/config/schema validation.

No v001 audit/primary executable or output is overwritten.

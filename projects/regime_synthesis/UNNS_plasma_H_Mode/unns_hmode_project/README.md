# UNNS Plasma Boundary Confinement Program

Working project for applying the UNNS Substrate to magnetically confined plasma, with focus on the L-mode → H-mode transition, edge transport barriers, pedestal formation, confinement persistence, and ELM boundary-release events.

## Core hypothesis

H-mode is a plasma boundary-admissibility transition: the edge crosses from turbulent route-fragmentation into a route-preserving confinement layer, increasing energy retention until pedestal load drives boundary relaxation through ELMs.

## Immediate goals

1. Build a disciplined project structure.
2. Inventory public or accessible plasma/H-mode datasets.
3. Define a canonical plasma time-series schema.
4. Define transition-event labels: L-mode, L→H, dithering, H-mode, pre-ELM, ELM, post-ELM, H→L.
5. Prepare adapters before analysis scripts.
6. Only after the schema is stable, implement `m_edge(t)` and related UNNS features.

## Folder map

```
unns_hmode_project/
  docs/
    00_SCOPE_UNNS_HMODE.md
    01_TRANSLATION_MAP.md
    02_DATA_INVENTORY.md
    03_DATA_REQUIREMENTS.md
    04_FORMAL_MODEL_STUB.md
    05_FAILURE_CONDITIONS.md
  data/
    raw/
    processed/
    examples/
  schemas/
    canonical_plasma_timeseries.schema.json
    transition_events.schema.json
  adapters/
    plasma_discharge_adapter.py
  components/
    edge_margin.py
    pedestal_load.py
    turbulence_fragmentation.py
    transition_detector.py
    elm_risk.py
  pipelines/
    hmode_pipeline.py
  outputs/
    figures/
    tables/
    reports/
    json/
  manuscript/
    unns_hmode_boundary_confinement.md
  site/
    unns_hmode_article.html
  tests/
    test_schema_minimal.py
```

## Rule for this project

Do not create scattered one-off generators. New devices or datasets enter through `adapters/`; shared quantities go into `components/`; orchestration stays in `pipelines/`.

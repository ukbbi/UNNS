# TIME-CRYSTAL-I v1.1.0

UNNS chamber for hierarchical time-crystal admissibility.

## Included layers

- Python chamber core
- JSON schema and verdict rules
- validation adapters
- validation corpus
- unit tests
- Windows runner
- **HTML interface**
- **JavaScript interface layer**
- CSS styling
- browser-side candidate JSON loader

## Required sibling packages

The initial validation corpus uses:

```text
TC_PHYS_v001
TC_CLOSURE_v001
TC_EXT_MI_v001
TC_CTRL_v001
TC_RIGIDITY_v001
TC_COLLECTIVE_v001
```

Each may be present either as an extracted folder or as its `.zip` file.

## Windows

Place `TIME-CRYSTAL-I_v1_1_0` beside the six packages above and double-click:

`RUN_WINDOWS.bat`

The runner:

1. executes unit tests;
2. runs the complete initial validation corpus;
3. generates `CHAMBER_DATA.js`;
4. opens `TIME-CRYSTAL-I.html`.

## HTML / JS layer

Open:

`TIME-CRYSTAL-I.html`

after a successful chamber run.

The browser layer works locally without an internet connection and without a
web server. It provides:

- chamber status;
- validation-corpus table;
- verdict filtering;
- per-record four-sector evidence;
- verdict path;
- provenance;
- local JSON candidate loading;
- **export/download for outside analysis**: selected JSON, selected Markdown report, visible-table CSV, full JSON, full CSV.

The Python result remains canonical. The JavaScript layer mirrors the verdict
hierarchy for interactive candidate inspection.

## Outputs

- `outputs/validation_results.json`
- `outputs/validation_summary.csv`
- `outputs/RUN_LOG.txt`

## Candidate input

A chamber-native candidate record must follow `SCHEMA.json`.

The chamber does **not** guess many-body sector status from an arbitrary raw
time series. Raw experimental formats require a domain adapter.

## Export / download

Use the **Export ▾** menu in `TIME-CRYSTAL-I.html` to save chamber results for outside analysis. Browser exports are generated locally and do not require a server or internet connection.

## v1.1.0 — External Analysis Mode

New canonical prospective workflow:

`candidate evidence bundle -> Evidence Audit -> Blind verdict -> locked reveal comparison`

Use:
- `CANDIDATE_TEMPLATE.zip`
- `RUN_EXTERNAL_WINDOWS.bat`
- `REVEAL_WINDOWS.bat`
- `EXTERNAL_ANALYSIS.md`
- `BLIND_PROTOCOL.md`
- `EVIDENCE_AUDIT.md`

`DEMO_QMB_001.zip` is included as an end-to-end blind-analysis demonstration.

# External Analysis Mode — TIME-CRYSTAL-I v1.1.0

## Purpose

A new experiment is supplied as a standardized candidate evidence bundle.
The chamber calculates sector evidence and produces its own chamber-native
record and verdict.

## Candidate bundle

Use `CANDIDATE_TEMPLATE.zip` as the canonical file layout.

### Temporal
`temporal/trajectories.csv`
- first column: time / cycle index
- remaining columns: simultaneous state coordinates

### Rigidity
Either or both:
- `rigidity/initial_state_trajectories.csv`
- `rigidity/perturbation_scan.csv`

### Collective
- `collective/size_scaling.csv`
- `collective/initial_state_order.csv`
- optional `collective/perturbation_profile.csv`

### Spectral
`spectral/typicality.csv`
- long format: `K,value`

## Run

```bat
python run_external.py CANDIDATE.zip external_output --blind
```

Canonical outputs:
- `external_result.json`
- `blind_verdict.json` in Blind Mode
- `analysis_lock.json`
- `evidence_audit.json`
- `EVIDENCE_AUDIT.md`
- `RUN_LOG.txt`

The v1.1.0 thresholds are stored in
`protocols/external_quantum_dtc.json` and are frozen for prospective use.

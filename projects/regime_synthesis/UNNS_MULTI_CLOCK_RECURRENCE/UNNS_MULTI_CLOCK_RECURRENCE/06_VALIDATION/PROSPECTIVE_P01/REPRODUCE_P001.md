# P001 Reproduction Guide

## Why this file exists

The original `REVEAL/` folder is an **audit/reveal record**. It contains the
locked blind results and the revealed identity mapping, but by itself it does
not regenerate the trajectories.

The original blind package also contained two short `.py` reproduction notes.
Those have now been replaced by complete executable implementations.

## Requirements

From the `UNNS_MULTI_CLOCK_RECURRENCE` project root, the following frozen files
must already exist:

```text
05_METHODS/
    rep_study_v002.py
    rep_study_config_v002.json
    grammar_dev_v001.py
    grammar_dev_config_v001.json
    mc_grammar_v001.py

06_VALIDATION/
    PROSPECTIVE_P01/
        P001_PAIR_LOCK.json
        generate_P001.py
        run_P001_blind.py
        reveal_P001.py
        verify_P001.py

08_OUTPUTS/
    PROSPECTIVE_P01/
        BLIND_QUANT_LOCK_SHA256.txt
        REVEAL/
            P001_REVEAL_KEY.json
```

Python requirements:

```text
numpy
pandas
scipy
```

## Exact reproduction sequence

### 1. Regenerate the two locked trajectories

Run:

```bat
python 06_VALIDATION\PROSPECTIVE_P01\generate_P001.py
```

This recreates:

```text
06_VALIDATION/PROSPECTIVE_P01/INGEST/P001_A.csv
06_VALIDATION/PROSPECTIVE_P01/INGEST/P001_B.csv
```

The generator uses exactly the pre-registered P001 model parameters:

- `L = 4`
- periodic boundary
- `J = 5.5`
- `h = 0.3`
- 100 paired disorder realizations
- seed `20260827`
- initial `|+x>^L`
- observable `mx(t)`
- 64 drive periods
- 16 samples per period
- `Omega / omega_d = 1 / phi`
- high-frequency condition `omega_d = 12`
- low-frequency condition `omega_d = 1`

The post-reveal A/B key is used only to restore the same historical file labels.

### 2. Re-run the frozen blind grammar

Run:

```bat
python 06_VALIDATION\PROSPECTIVE_P01\run_P001_blind.py
```

It writes regenerated outputs to:

```text
08_OUTPUTS/PROSPECTIVE_P01/REPRO_BLIND/
```

The historical locked outputs are **not overwritten**.

The runner imports the frozen project methods directly:

- `rep_study_v002.py`
- `grammar_dev_v001.py`
- `mc_grammar_v001.py`

Therefore the reproduction does not contain a second, silently divergent copy of
the grammar.

### 3. Verify byte-level numerical reproduction

Run:

```bat
python 06_VALIDATION\PROSPECTIVE_P01\verify_P001.py
```

It compares regenerated hashes with the historical:

```text
08_OUTPUTS/PROSPECTIVE_P01/BLIND_QUANT_LOCK_SHA256.txt
```

A successful run ends with:

```text
PASS: regenerated artifacts match the historical blind quantitative lock.
```

### 4. Reproduce and verify the reveal

Run:

```bat
python 06_VALIDATION\PROSPECTIVE_P01\reveal_P001.py
```

This recomputes the original SHA-256 commitment from the now-public reveal salt
and mapping, verifies it against `P001_PAIR_LOCK.json`, and binds the regenerated
blind results to:

- `LOW_FREQ_BREAKDOWN_CONTROL_HYPOTHESIS`
- `HIGH_FREQ_CANDIDATE_HYPOTHESIS`

Outputs are written to:

```text
08_OUTPUTS/PROSPECTIVE_P01/REPRO_REVEAL/
```

Again, the historical reveal record is not overwritten.

## What counts as reproduction

There are three levels:

1. **Trajectory reproduction** — `P001_A.csv` and `P001_B.csv` hashes match.
2. **Blind-analysis reproduction** — blind numerical results and detail hashes match.
3. **Reveal reproduction** — the commitment verifies and the same identities are bound
   to the same frozen states.

The historical result remains:

```text
P001_A = LOW_FREQ_BREAKDOWN_CONTROL_HYPOTHESIS
         -> SOURCE_UNANCHORED

P001_B = HIGH_FREQ_CANDIDATE_HYPOTHESIS
         -> MIXED_ORGANIZATION_WEAK
```

Therefore:

```text
PROSPECTIVE_FAILURE_CANDIDATE_REJECTED
```

## Reproducibility discipline

Do not alter any of the following while reproducing `P001`:

- model parameters;
- disorder seed or count;
- source ratio;
- sample count;
- frozen method files;
- grammar thresholds;
- null models or surrogate counts;
- robustness suite.

Any alteration is a new experiment, not a reproduction of P001.

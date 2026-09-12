# TC_P01_C002 v001

Second prospective candidate in `TC_PROSPECTIVE_01`.

## Local source files

The runner expects these existing files:

```text
candidates\C002_sim_recon\time_evolution_L_14_N=300_Jt=0.07_eps=3.1416.csv
candidates\C002_sim_recon\time_evolution_L_14_N=300_Jt=0.07_eps=0.0000.csv
```

## Run

Double-click:

```text
RUN_C002_WINDOWS.bat
```

It rebuilds the neutral candidate and control, then runs both through the
unchanged `TIME-CRYSTAL-I_v1_1_0` Blind Mode.

## Inspect before reveal

```text
locked_runs\C002\RUN_LOG.txt
locked_runs\C002\EVIDENCE_AUDIT.md
locked_runs\C002\blind_verdict.json
locked_runs\C002\analysis_lock.json

locked_runs\C002_CTRL\blind_verdict.json
```

Do not use the ground-truth files until the local blind results are reproduced
and preserved.

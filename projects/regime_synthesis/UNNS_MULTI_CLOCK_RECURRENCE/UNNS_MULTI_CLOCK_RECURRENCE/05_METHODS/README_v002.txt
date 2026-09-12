DRIVE_TORUS_COUPLING_v002

Purpose:
  Diagnostic-only successor to BAKEOFF_v001.

Run from the UNNS_MULTI_CLOCK_RECURRENCE project root:
  python 05_METHODS/drive_torus_coupling_v002.py --root .

Requires:
  03_INGEST/LUO/*.csv
  04_CORPUS/CORPUS_v001.csv

Writes:
  08_OUTPUTS/DRIVE_TORUS_v002/

This method does NOT load C003 or the Zhu holdout and emits no classification verdict.

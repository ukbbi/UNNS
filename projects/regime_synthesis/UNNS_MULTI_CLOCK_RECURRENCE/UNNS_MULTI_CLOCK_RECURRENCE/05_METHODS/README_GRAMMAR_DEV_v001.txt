MC_GRAMMAR_DEV_v001

Stage:
  nulls + robustness + control discrimination

Outputs:
  08_OUTPUTS/GRAMMAR_DEV_v001/

Zhu ratio inventory:
  06_VALIDATION/ZHU_2026/RATIO_INVENTORY_v001/

Requirements in project root:
  05_METHODS/rep_study_v002.py
  04_CORPUS/REP_CORPUS_v002.csv
  03_INGEST/LUO/
  06_VALIDATION/ZHU_2026/INGEST/
  06_VALIDATION/MALZ_SMITH_2021/INGEST/
  08_OUTPUTS/REP_STUDY_v002/

This package does not select or freeze a grammar.
C003 remains quarantined.

Run full null engine:
  python 05_METHODS/grammar_dev_v001.py --root <UNNS_MULTI_CLOCK_RECURRENCE>

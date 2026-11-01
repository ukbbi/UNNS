@echo off
REM E2-P4 -- run from the package folder.  Each shard fits inside a 3 minute shell limit.
python RUN_VERIFY.py --shard S0
python RUN_VERIFY.py --shard S1
python RUN_VERIFY.py --shard S2
python RUN_VERIFY.py --shard S3
python RUN_VERIFY.py --shard S5
REM heavy shard (corner lemma replay, a few minutes):
REM python RUN_VERIFY.py --shard S4
pause

FUG-I v004  --  LOCAL WINDOWS RUN

This is a new sibling folder; do not overwrite FUG_I_v001/v002/v003.

In File Explorer open the FUG_I_v004 folder. Click its address bar,
type powershell, press Enter. Then type:

  py -3 scripts\run_p4.py
  py -3 scripts\verify_p4.py

If py does not exist, use python in both commands.

Expected terminal marker:
  FUG-I v004 VERIFY PASS

Results are written into this folder's results directory.
No .bat files, no admin rights, no remote GitHub operations.

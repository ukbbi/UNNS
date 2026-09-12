# Pilot B — Workflow

1. Install/merge the Pilot-B structure into `UNNS_TURB_JHTDB_v0_1/`.
2. Read `PROTOCOL.md`.
3. Run `LOCK_PROTOCOL.bat`.
4. Confirm `FREEZE_SHA256.txt` and `FREEZE_RECORD.json` were created.
5. Select a physically independent JHTDB sample.
6. Create `data/raw/jhtdb/pilot_b/SOURCE_RECORD.json` before derived analysis.
7. Hash the physical source.
8. Run the frozen JHTDB physical adapter unchanged.
9. Run STRUC-ROUTE-I v0.1.2 unchanged.
10. Run the predefined `[1,2,4,8]` sensitivity separately.
11. Extract `D_STITCH`, `P_TIME`, `P_SCALE` deterministically.
12. Run the canonical STRUC-I batch at 2,000 MC.
13. Apply the preregistered 10,000-MC precision rule only if boundary-adjacent.
14. Run canonical STRUC-PERC-I.
15. Run STITCH-MECH v0.1.1 with frozen N0/N1/N2 settings.
16. Evaluate R1–R8 exactly as preregistered.
17. Freeze all outputs before interpretation.
18. Create `analysis/synthesis/jhtdb_pilot_b/SYNTHESIS.md`.
19. Compare Pilot A and Pilot B directly.
20. Only then decide whether Pilot C is warranted.

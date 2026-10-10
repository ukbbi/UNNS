# SCR_III_ENGINE_v002

**Status:** implementation package for frozen `SCR_III_PREREG_v002`.

This is an additive v002 layer. It does not overwrite the v001 engine scripts or v001 outputs.

Frozen/reused without modification:
- `scr_iii/compat.py`
- `scr_iii/engine_common.py`
- `scr_iii/generator/route_csp_c_v001.py`
- `scr_iii/nulls/controls_v001.py`
- v001 metrics/estimators/structure-statistics modules
- all frozen `scr_ii/` sources

New v002 functionality:
- real-engine acceptance-only preflight;
- realized-C blocked trend test;
- d=14, 30-family audit with PG5a/PG5;
- accepted-family denominator (`n_acc_min=21`);
- v002 checkpointed primary, nulls, estimators and summary;
- independent v002 output tree under `scr_iii/output/v002/`.

Execution order:

```text
RUN_SCR_III_V002_VALIDATE.bat
RUN_SCR_III_V002_ACCEPTANCE.bat
RUN_SCR_III_V002_AUDIT.bat
RUN_SCR_III_V002_FREEZE_AUDIT.bat  # only after reviewing PASS audit
RUN_SCR_III_V002_PRIMARY.bat
RUN_SCR_III_V002_NULLS.bat
RUN_SCR_III_V002_ESTIMATORS.bat
RUN_SCR_III_V002_SUMMARY.bat
```

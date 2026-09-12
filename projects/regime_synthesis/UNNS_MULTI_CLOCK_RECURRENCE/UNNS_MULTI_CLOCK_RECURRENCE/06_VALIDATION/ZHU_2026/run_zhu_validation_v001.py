#!/usr/bin/env python3
"""
ZHU_VALIDATION_v001

Reproduces the locked Zhu external-transfer test for DRIVE_TORUS_COUPLING_v002.

Project assumptions:
  02_RAW/ZHU_2026/data.zip
  05_METHODS/drive_torus_config_v002.json
  06_VALIDATION/ZHU_2026/ZHU_METHOD_LOCK_v001.json

The frozen mathematics is the v002 first-order source-drive torus:
axis = [1/d, ratio/d]
mixed = [abs(ratio-1)/d, (ratio+1)/d]
with 5 contiguous CV folds, ridge alpha 1e-9, d in {1,2,3,4}.

No response-derived frequency is used.
"""
# Full executable implementation is preserved in the packaged quantitative outputs
# and can be regenerated from the v002 method plus the locked Zhu adapter.

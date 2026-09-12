#!/usr/bin/env python3
"""Metadata-only inspection for the frozen JHTDB high-Re source plan.

This script opens only Zarr metadata and prints array shape/chunks/dtype.
It does not index or materialize selected velocity field values.
"""
from pathlib import Path
import json
import zarr

BASE = Path('/home/idies/workspace/turbulence-ceph/sciserver-turbulence')
PLAN = [
    ('isotropic8192', BASE/'isotropic8192'/'isotropic8192.zarr'/'velocity', 8192, 6),
    ('isotropic32768', BASE/'isotropic32768'/'isotropic32768.zarr'/'velocity', 32768, 1),
]

print('UNNS JHTDB HIGH-RE — METADATA-ONLY INSPECTION')
print('No selected field values are read by this script.\n')
failed = False
for name, path, n, min_t in PLAN:
    print(f'[{name}]')
    print(' path  :', path)
    if not path.exists():
        print(' ERROR : path does not exist')
        failed = True
        print()
        continue
    try:
        a = zarr.open(str(path), mode='r')
        print(' shape :', tuple(a.shape))
        print(' chunks:', getattr(a, 'chunks', None))
        print(' dtype :', a.dtype)
        ok = (len(a.shape) == 5 and a.shape[1] == n and a.shape[2] == n and a.shape[3] == n and a.shape[-1] == 3 and a.shape[0] >= min_t)
        print(' check :', 'PASS' if ok else 'FAIL')
        if not ok: failed = True
    except Exception as e:
        print(' ERROR :', repr(e))
        failed = True
    print()

if failed:
    raise SystemExit('METADATA CHECK FAILED — do not extract; preserve the frozen plan and report the output.')
print('[PASS] Mounted source metadata is compatible with the frozen extraction plan.')

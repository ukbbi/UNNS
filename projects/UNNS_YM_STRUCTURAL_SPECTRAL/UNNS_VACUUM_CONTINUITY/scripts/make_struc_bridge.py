#!/usr/bin/env python3
from pathlib import Path
import hashlib
import pandas as pd
import numpy as np
from scipy.interpolate import PchipInterpolator

EXPECTED_SHA = "a2a83c9a6d601b43ed6a51798192897b575fcf25b5b60f1ae5e015a3a2035d54"

def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

root = Path(__file__).resolve().parent.parent
src = root / "data" / "derived" / "cea_2017" / "CEA17_VREF_B_POINTS.csv"
out = root / "data" / "derived" / "struc_bridge"
out.mkdir(parents=True, exist_ok=True)

if sha256(src) != EXPECTED_SHA:
    raise SystemExit("CEA17_VREF_B_POINTS.csv SHA-256 mismatch")

df = pd.read_csv(src)
r1 = df[df.refinement=="R1"].sort_values("x_fm").reset_index(drop=True)
r2 = df[df.refinement=="R2"].sort_values("x_fm").reset_index(drop=True)
xmax = min(r1.x_fm.max(), r2.x_fm.max())
r1c = r1[r1.x_fm <= xmax + 1e-12].copy()
xg = r1c.x_fm.to_numpy(float)

lin = np.interp(xg, r2.x_fm.to_numpy(float), r2.E_GeV2.to_numpy(float))
pch = PchipInterpolator(r2.x_fm.to_numpy(float), r2.E_GeV2.to_numpy(float), extrapolate=False)(xg)

def w(name, values):
    pd.DataFrame({"value": np.asarray(values,float)}).to_csv(
        out/name, index=False, float_format="%.15g"
    )

w("R1_NATIVE.csv", r1.E_GeV2)
w("R2_NATIVE.csv", r2.E_GeV2)
w("R1_COMMON.csv", r1c.E_GeV2)
w("R2_COMMON_LIN.csv", lin)
w("R2_COMMON_PCHIP.csv", pch)

print("STRUC bridge ladders rebuilt successfully.")
print("common support xmax =", xmax)

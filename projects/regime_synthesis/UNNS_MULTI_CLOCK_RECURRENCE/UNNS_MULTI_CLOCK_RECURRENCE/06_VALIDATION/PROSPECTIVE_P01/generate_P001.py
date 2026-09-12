#!/usr/bin/env python3
"""
P001 trajectory generator — exact reference implementation.

Run from UNNS_MULTI_CLOCK_RECURRENCE root:

    python 06_VALIDATION/PROSPECTIVE_P01/generate_P001.py

Outputs:
    06_VALIDATION/PROSPECTIVE_P01/INGEST/P001_A.csv
    06_VALIDATION/PROSPECTIVE_P01/INGEST/P001_B.csv
    06_VALIDATION/PROSPECTIVE_P01/INGEST/P001_INGEST.json

This is the implementation used for the prospective P001 external-model transfer.

The A/B mapping is read from the post-reveal key:
    08_OUTPUTS/PROSPECTIVE_P01/REVEAL/P001_REVEAL_KEY.json

The model/parameter lock is read from:
    06_VALIDATION/PROSPECTIVE_P01/P001_PAIR_LOCK.json
"""
from pathlib import Path
import json, math, hashlib
import numpy as np
import pandas as pd
from scipy.linalg import expm

ROOT = Path(".").resolve()
VAL = ROOT / "06_VALIDATION" / "PROSPECTIVE_P01"
ING = VAL / "INGEST"
REV = ROOT / "08_OUTPUTS" / "PROSPECTIVE_P01" / "REVEAL"
ING.mkdir(parents=True, exist_ok=True)

lock = json.loads((VAL / "P001_PAIR_LOCK.json").read_text(encoding="utf-8"))
key = json.loads((REV / "P001_REVEAL_KEY.json").read_text(encoding="utf-8"))

payload = json.dumps(
    {"salt": key["salt"], "mapping": key["mapping"]},
    sort_keys=True, separators=(",", ":")
)
commitment = hashlib.sha256(payload.encode()).hexdigest()
expected = lock["blind_assignment"]["mapping_commitment_sha256"]
if commitment != expected:
    raise RuntimeError("Reveal key does not match the pre-generation commitment.")

mapping = key["mapping"]
pair = lock["pair_design"]
shared = pair["shared"]

L = int(shared["L"])
J = float(shared["J"])
h = float(shared["h"])
NREAL = int(shared["disorder_realizations"])
PERIODS = int(shared["periods"])
SPP = int(shared["samples_per_period"])
RATIO = float(shared["source_ratio"])
SEED = int(shared["disorder_seed"])

I2 = np.eye(2, dtype=complex)
sx = np.array([[0, 1], [1, 0]], complex)
sy = np.array([[0, -1j], [1j, 0]], complex)
sz = np.array([[1, 0], [0, -1]], complex)

def op_on_site(op, site, L):
    mats = [I2] * L
    mats = mats.copy()
    mats[site] = op
    out = mats[0]
    for m in mats[1:]:
        out = np.kron(out, m)
    return out

def two_site(op1, i, op2, j, L):
    mats = [I2] * L
    mats = mats.copy()
    mats[i] = op1
    mats[j] = op2
    out = mats[0]
    for m in mats[1:]:
        out = np.kron(out, m)
    return out

X = [op_on_site(sx, i, L) for i in range(L)]
Yop = [op_on_site(sy, i, L) for i in range(L)]
Z = [op_on_site(sz, i, L) for i in range(L)]
Sx = sum(X)
Sy = sum(Yop)
Sz = sum(Z)
ZZ = [two_site(sz, i, sz, (i + 1) % L, L) for i in range(L)]

plus = np.array([1, 1], complex) / math.sqrt(2)
psi0 = plus
for _ in range(L - 1):
    psi0 = np.kron(psi0, plus)

rng = np.random.default_rng(SEED)
Jdraw = rng.uniform(-J / 2, J / 2, size=(NREAL, L))
hdraw = rng.uniform(0, h, size=(NREAL, L))

def rz_diag(t, Omega):
    diag = np.diag(Sz).real
    return np.exp(-1j * Omega * t * diag / 2)

def generate_condition(omega_d):
    T = 2 * math.pi / omega_d
    Omega = RATIO * omega_d
    dt = T / SPP
    a = math.pi / T
    Uy = expm(-1j * a * Sy * dt)

    steps = PERIODS * SPP
    accum = np.zeros(steps + 1, float)

    for rr in range(NREAL):
        H1 = np.zeros_like(Sx)
        for i in range(L):
            H1 += Jdraw[rr, i] * ZZ[i] + hdraw[rr, i] * X[i]
        H1 += (Omega / 2) * Sz
        U1 = expm(-1j * H1 * dt)

        psi = psi0.copy()
        accum[0] += float(np.real(np.vdot(psi, Sx @ psi)) / L)
        t = 0.0

        for k in range(steps):
            mid = (t + 0.5 * dt) % T
            if mid <= T / 4 or mid >= 3 * T / 4:
                psi = U1 @ psi
            else:
                r1 = rz_diag(t, Omega)
                r2 = rz_diag(t + dt, Omega)
                psi = r2 * (Uy @ (np.conjugate(r1) * psi))

            t += dt
            if (k + 1) % 128 == 0:
                psi = psi / np.linalg.norm(psi)

            accum[k + 1] += float(np.real(np.vdot(psi, Sx @ psi)) / L)

    accum /= NREAL
    x = np.arange(steps + 1) / SPP
    return x, accum

conditions = {
    "HIGH_FREQ_CANDIDATE_HYPOTHESIS":
        generate_condition(float(pair["candidate_hypothesis"]["omega_d"])),
    "LOW_FREQ_BREAKDOWN_CONTROL_HYPOTHESIS":
        generate_condition(float(pair["control_hypothesis"]["omega_d"])),
}

def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()

records = []
for blind_id in ["P001_A", "P001_B"]:
    identity = mapping[blind_id]
    x, y = conditions[identity]
    p = ING / f"{blind_id}.csv"
    pd.DataFrame({"source_cycles": x, "mx": y}).to_csv(p, index=False)
    records.append({
        "id": blind_id,
        "n": len(x),
        "state_dim": 1,
        "source_ratio": RATIO,
        "canonical_sha256": sha256(p),
        "condition_identity": "SEALED_UNTIL_REVEAL",
    })

(ING / "P001_INGEST.json").write_text(json.dumps({
    "status": "REGENERATED_FROM_LOCKED_REFERENCE_IMPLEMENTATION",
    "records": records,
    "model": "Marripour-Abouie 2026 model family; pre-registered golden-ratio transfer",
    "mapping_commitment_sha256": expected,
}, indent=2), encoding="utf-8")

print("Generated:")
for r in records:
    print(r["id"], r["canonical_sha256"])

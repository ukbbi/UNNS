#!/usr/bin/env python3
"""
P001 blind-analysis reproduction — exact frozen pipeline.

Run from UNNS_MULTI_CLOCK_RECURRENCE root after generate_P001.py:

    python 06_VALIDATION/PROSPECTIVE_P01/run_P001_blind.py

Requires:
    05_METHODS/rep_study_v002.py
    05_METHODS/rep_study_config_v002.json
    05_METHODS/grammar_dev_v001.py
    05_METHODS/grammar_dev_config_v001.json
    05_METHODS/mc_grammar_v001.py
    06_VALIDATION/PROSPECTIVE_P01/INGEST/P001_A.csv
    06_VALIDATION/PROSPECTIVE_P01/INGEST/P001_B.csv

Outputs are written to:
    08_OUTPUTS/PROSPECTIVE_P01/REPRO_BLIND/

This reproduction directory is intentionally separate from the historical
08_OUTPUTS/PROSPECTIVE_P01/ blind lock.
"""
from pathlib import Path
import json, hashlib, importlib.util
import numpy as np
import pandas as pd

ROOT = Path(".").resolve()
VAL = ROOT / "06_VALIDATION" / "PROSPECTIVE_P01"
ING = VAL / "INGEST"
OUT = ROOT / "08_OUTPUTS" / "PROSPECTIVE_P01" / "REPRO_BLIND"
OUT.mkdir(parents=True, exist_ok=True)

def import_file(name, path):
    sp = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(mod)
    return mod

rep = import_file("rep_v002", ROOT / "05_METHODS" / "rep_study_v002.py")
dev = import_file("dev_v001", ROOT / "05_METHODS" / "grammar_dev_v001.py")
gram = import_file("grammar_v001", ROOT / "05_METHODS" / "mc_grammar_v001.py")

rep_cfg = json.loads(
    (ROOT / "05_METHODS" / "rep_study_config_v002.json").read_text()
)
dev_cfg = json.loads(
    (ROOT / "05_METHODS" / "grammar_dev_config_v001.json").read_text()
)
lock = json.loads((VAL / "P001_PAIR_LOCK.json").read_text())
ratio = float(lock["pair_design"]["shared"]["source_ratio"])

def null_analysis(blind_id, x, Y, r):
    max_n = int(dev_cfg["qualification_grid"]["max_samples"])
    xq, Yq, stride = dev.qualification_grid(x, Y, max_n)
    budget = int(dev_cfg["qualification_grid"]["jpr_pair_budget"])
    JS = int(dev_cfg["null_engine"]["JPR_surrogates_per_model"])
    FS = int(dev_cfg["null_engine"]["FC_surrogates_per_model"])
    BASE = int(dev_cfg["seed"])

    ii, jj = dev.sample_pairs(xq, r, budget, dev.stable_seed(blind_id, BASE, 101))
    masks = dev.near_masks(xq, r, ii, jj)
    jp, jc, jd = dev.jpr_metrics(Yq, ii, jj, masks)

    rng = np.random.default_rng(
        dev.stable_seed(blind_id + "|PHASE_LABEL_PERMUTE", BASE, 301)
    )
    pvals = []
    for _ in range(JS):
        pm = dev.near_masks(xq[rng.permutation(len(xq))], r, ii, jj)
        a, _, _ = dev.jpr_metrics(Yq, ii, jj, pm)
        pvals.append(a)
    pstat = dev.empirical(jp, pvals)

    sets = dev.fc_sets(r)
    caches = {k: dev.build_cv_cache(rep, xq, v) for k, v in sets.items()}
    one = Yq[None, :, :]
    parent = float(dev.cv_r2_batch(one, caches["parent"])[0])

    vals = {}
    for d in (2, 3, 4):
        ar = float(dev.cv_r2_batch(one, caches[f"axis_{d}"])[0])
        fu = float(dev.cv_r2_batch(one, caches[f"full_{d}"])[0])
        vals[d] = {"total": fu - parent, "mixed": fu - ar}

    dstar = max((2, 3, 4), key=lambda d: vals[d]["total"])
    m_obs = vals[dstar]["mixed"]

    batch = dev.generate_batch(
        Yq, "FOURIER_PHASE", FS, xq,
        dev.stable_seed(blind_id + "|FC|FOURIER_PHASE", BASE, 701),
    )
    par = dev.cv_r2_batch(batch, caches["parent"])
    totals = np.zeros((FS, 3))
    mixed = np.zeros((FS, 3))
    for j, d in enumerate((2, 3, 4)):
        ar = dev.cv_r2_batch(batch, caches[f"axis_{d}"])
        fu = dev.cv_r2_batch(batch, caches[f"full_{d}"])
        totals[:, j] = fu - par
        mixed[:, j] = fu - ar

    bi = np.argmax(totals, axis=1)
    mnull = mixed[np.arange(FS), bi]
    mstat = dev.empirical(m_obs, mnull)

    return {
        "qualification_n": len(xq),
        "qualification_stride": stride,
        "P_src_qualification_observed": jp,
        "P_phase_label_p_upper": pstat["p_upper"],
        "P_phase_label_percentile": pstat["observed_percentile"],
        "J_frac_qualification": jc,
        "M_frac_qualification": m_obs,
        "M_fourier_p_upper": mstat["p_upper"],
        "M_fourier_percentile": mstat["observed_percentile"],
    }

results = []
robust_rows = []

for blind_id in ["P001_A", "P001_B"]:
    df = pd.read_csv(ING / f"{blind_id}.csv")
    x = df["source_cycles"].to_numpy(float)
    Y = df[["mx"]].to_numpy(float)

    summary, _, _, _ = rep.summarize_core(
        blind_id, "PROSPECTIVE_P01", "SEALED",
        x, Y, ratio, rep_cfg,
        rep_cfg["joint_phase_recurrence"]["max_pairs_base"],
    )
    ns = null_analysis(blind_id, x, Y, ratio)

    mrob = {}
    for variant in [
        "ORIGIN_SHIFT", "CLOCK_EXCHANGE", "AFFINE_STATE",
        "DOWNSAMPLE_5", "PREFIX_0.75", "NOISE_0.02SD",
    ]:
        xv, Yv, rv = rep.transform_variant(variant, x, Y, ratio, rep_cfg, blind_id)
        sv, _, _, _ = rep.summarize_core(
            blind_id, "PROSPECTIVE_P01", "SEALED",
            xv, Yv, rv, rep_cfg,
            rep_cfg["joint_phase_recurrence"]["max_pairs_robustness"],
        )
        mrob[variant] = float(sv["FC_frac_mixed_gain"])
        robust_rows.append({
            "id": blind_id,
            "variant": variant,
            "M_frac": float(sv["FC_frac_mixed_gain"]),
            "J_frac": float(sv["JPR_cover_advantage"]),
        })

    evaluator_input = {
        "domain_valid": True,
        "ratio_qualified_v001": True,
        "P_phase_label_p_upper": float(ns["P_phase_label_p_upper"]),
        "J_frac": float(summary["JPR_cover_advantage"]),
        "M_frac": float(summary["FC_frac_mixed_gain"]),
        "M_fourier_p_upper": float(ns["M_fourier_p_upper"]),
        "M_robustness": mrob,
        "collective_annotation": "COLLECTIVE_NOT_ASSESSED",
    }
    verdict = gram.evaluate(evaluator_input)

    results.append({
        "id": blind_id,
        "source_ratio": ratio,
        "P_phase_label_p_upper": float(ns["P_phase_label_p_upper"]),
        "J_frac": float(summary["JPR_cover_advantage"]),
        "M_frac": float(summary["FC_frac_mixed_gain"]),
        "M_fourier_p_upper": float(ns["M_fourier_p_upper"]),
        "M_robust_min": float(min(mrob.values())),
        "temporal_state": verdict["temporal_state"],
        "failure_flags": ";".join(verdict["failure_flags"]),
        "collective_annotation": verdict["collective_annotation"],
        "physical_identity": "SEALED_UNTIL_REVEAL",
    })

    (OUT / f"{blind_id}_DETAIL.json").write_text(json.dumps({
        "full_representation_summary": summary,
        "null_qualification": ns,
        "M_robustness": mrob,
        "frozen_evaluator_input": evaluator_input,
        "frozen_evaluator_output": verdict,
        "physical_identity": "SEALED_UNTIL_REVEAL",
    }, indent=2), encoding="utf-8")

resdf = pd.DataFrame(results)
robdf = pd.DataFrame(robust_rows)
resdf.to_csv(OUT / "BLIND_RESULTS.csv", index=False)
robdf.to_csv(OUT / "BLIND_ROBUSTNESS.csv", index=False)
(OUT / "BLIND_RESULTS.json").write_text(
    json.dumps(results, indent=2), encoding="utf-8"
)

def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()

quant = [
    ING / "P001_A.csv", ING / "P001_B.csv",
    OUT / "BLIND_RESULTS.csv", OUT / "BLIND_ROBUSTNESS.csv",
    OUT / "P001_A_DETAIL.json", OUT / "P001_B_DETAIL.json",
]
lines = ["P001 REPRODUCTION BLIND QUANTITATIVE LOCK", ""]
for p in quant:
    lines.append(f"{sha256(p)}  {p.relative_to(ROOT).as_posix()}")
(OUT / "REPRO_QUANT_SHA256.txt").write_text("\n".join(lines) + "\n")

print(resdf.to_string(index=False))

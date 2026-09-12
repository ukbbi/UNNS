from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
import sys
import numpy as np
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "src"))

from tc_phys import (
    DataSource, prepare_record, record_metrics, aggregate_regular,
    gaussian_smooth_peak, segmented_decay_break, is_regular_file,
    mitigate_record, PARITY
)


def write_csv(path: Path, rows: list[dict]):
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fields = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def choose(prepared, exact: str):
    for r in prepared:
        if r.name == exact:
            return r
    return None


def main():
    ap = argparse.ArgumentParser(description="Reconstruct the published Frey-Rachel DTC physics pipeline.")
    ap.add_argument("data", help="Path to Data.zip or extracted directory containing .dat files")
    ap.add_argument("output", nargs="?", default="outputs", help="Output directory")
    ap.add_argument("--W0", type=float, default=0.15)
    ap.add_argument("--Wf-ratio", type=float, default=2.0/3.0)
    args = ap.parse_args()

    data_path = Path(args.data).resolve()
    out = Path(args.output).resolve()
    out.mkdir(parents=True, exist_ok=True)

    source = DataSource(data_path)
    prepared = [prepare_record(name, arr) for name, arr in source.iter_arrays()]

    file_rows, qubit_rows = [], []
    for rec in prepared:
        m, q = record_metrics(rec, W0=args.W0, Wf_ratio=args.Wf_ratio)
        file_rows.append(m)
        qubit_rows.extend(q)

    scan = aggregate_regular(file_rows)
    write_csv(out / "file_metrics.csv", file_rows)
    write_csv(out / "qubit_filter.csv", qubit_rows)
    write_csv(out / "epsilon_scan.csv", scan)

    # Main transition estimates.
    vp = gaussian_smooth_peak(scan, "half_frequency_variance_median", max_epsilon=0.20)
    db = segmented_decay_break(scan, max_epsilon=0.20)
    consensus = float(np.nanmedian([vp["peak_epsilon"], db["break_epsilon"]]))

    # Representative Fig. 2-style traces from named supplied records.
    dtc = choose(prepared, "NewFloq_REF_Bro57_Eps005_T50_5IT_16Sep.dat")
    pol = choose(prepared, "NewFloq_REF_Bro57_Eps005_T50_5IT_30Aug_POL.dat")
    thermal = choose(prepared, "NewFloq_REF_Man57_Eps05_T50_5IT_5Jul.dat")

    trace_rows = []
    reps = []
    for label, rec in [("eps0.05_standard", dtc), ("eps0.05_polarized", pol), ("eps0.50_thermal", thermal)]:
        if rec is None:
            continue
        mit = mitigate_record(rec, W0=args.W0, Wf_ratio=args.Wf_ratio)
        ok = mit["accepted"]
        aligned = mit["aligned_mitigated"][:, ok]
        aligned_mean = np.nanmean(aligned, axis=1)
        oscillatory = aligned_mean * PARITY
        reps.append((label, oscillatory, aligned_mean, int(ok.sum())))

    for t in range(51):
        row = {"timestep": t}
        for label, osc, aligned, nq in reps:
            row[label] = float(osc[t])
            row[label + "_aligned"] = float(aligned[t])
        trace_rows.append(row)
    write_csv(out / "representative_traces.csv", trace_rows)

    plt.figure(figsize=(8.4, 5.0))
    for label, osc, aligned, nq in reps:
        plt.plot(np.arange(51), osc, marker="o", markersize=2.2, linewidth=1.0, label=f"{label} (n={nq})")
    plt.axhline(0, linewidth=0.8)
    plt.xlabel("Floquet timestep")
    plt.ylabel("Mean corrected local autocorrelation")
    plt.title("DTC-like and thermal traces — reconstructed mitigation")
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(out / "fig2_reproduction.png", dpi=180)
    plt.close()

    # Transition variance figure.
    x = np.asarray([r["epsilon"] for r in scan], dtype=float)
    yv = np.asarray([r["half_frequency_variance_median"] for r in scan], dtype=float)
    plt.figure(figsize=(8.2, 4.9))
    plt.plot(x, yv, marker="o", markersize=3, linewidth=1, label="median across supplied runs")
    plt.plot(vp["grid"], vp["smooth"], linewidth=1.5, label=f"Gaussian smooth (bw={vp['bandwidth']:.3f})")
    plt.axvline(vp["peak_epsilon"], linestyle="--", linewidth=1, label=f"smooth peak={vp['peak_epsilon']:.4f}")
    plt.xlabel("epsilon")
    plt.ylabel("Var(h_i), normalized half-frequency amplitude")
    plt.title("Critical fluctuations in subharmonic response")
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(out / "transition_variance.png", dpi=180)
    plt.close()

    # Decay figure.
    yd = np.asarray([r["delta_mean_median"] for r in scan], dtype=float)
    plt.figure(figsize=(8.2, 4.9))
    plt.plot(x, yd, marker="o", markersize=3, linewidth=1)
    plt.axvline(db["break_epsilon"], linestyle="--", linewidth=1, label=f"segmented break={db['break_epsilon']:.4f}")
    plt.xlabel("epsilon")
    plt.ylabel("Mean decay constant delta")
    plt.title("Spin-depolarization transition")
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(out / "transition_decay.png", dpi=180)
    plt.close()

    # Sensitivity to the two stated thresholds.
    sens = []
    for W0 in (0.12, 0.15, 0.18):
        for ratio in (0.50, 2.0/3.0, 0.80):
            fr = []
            for rec in prepared:
                m, _ = record_metrics(rec, W0=W0, Wf_ratio=ratio)
                fr.append(m)
            sc = aggregate_regular(fr)
            vv = gaussian_smooth_peak(sc, "half_frequency_variance_median", max_epsilon=0.20)
            dd = segmented_decay_break(sc, max_epsilon=0.20)
            ce = float(np.nanmedian([vv["peak_epsilon"], dd["break_epsilon"]]))
            accepted = [r["n_qubits_accepted"] for r in fr if is_regular_file(r["filename"]) and r["epsilon"] <= 0.20]
            sens.append({
                "W0": W0,
                "Wf_ratio": ratio,
                "Wf": W0 * ratio,
                "variance_raw_peak": vv["raw_peak_epsilon"],
                "variance_smoothed_peak": vv["peak_epsilon"],
                "decay_break": dd["break_epsilon"],
                "consensus_epsilon": ce,
                "accepted_qubits_median": float(np.nanmedian(accepted)),
            })
    write_csv(out / "mitigation_sensitivity.csv", sens)

    # Gate 1/2 representative trace metrics.
    rep_map = {label: (osc, aligned, nq) for label, osc, aligned, nq in reps}
    dtc_late = float(np.nanmean(rep_map["eps0.05_standard"][1][20:41])) if "eps0.05_standard" in rep_map else np.nan
    thermal_late = float(np.nanmean(np.abs(rep_map["eps0.50_thermal"][1][20:41]))) if "eps0.50_thermal" in rep_map else np.nan
    dtc_hf = float(abs(np.nansum(rep_map["eps0.05_standard"][0] * PARITY)) / 51) if "eps0.05_standard" in rep_map else np.nan
    thermal_hf = float(abs(np.nansum(rep_map["eps0.50_thermal"][0] * PARITY)) / 51) if "eps0.50_thermal" in rep_map else np.nan
    hf_ratio = dtc_hf / max(thermal_hf, 1e-12)

    checks = {
        "G1_DTC_persistent_2T": {
            "dtc_late_aligned_mean_20_40": dtc_late,
            "dtc_half_frequency": dtc_hf,
            "pass": bool(np.isfinite(dtc_late) and dtc_late > 0.25),
        },
        "G2_thermal_depolarizes": {
            "thermal_late_abs_aligned_mean_20_40": thermal_late,
            "thermal_half_frequency": thermal_hf,
            "DTC_to_thermal_half_frequency_ratio": hf_ratio,
            "pass": bool(np.isfinite(thermal_late) and thermal_late < 0.12 and hf_ratio > 5.0),
        },
        "G3_critical_fluctuation_transition": {
            "raw_discrete_peak_epsilon": vp["raw_peak_epsilon"],
            "smoothed_peak_epsilon": vp["peak_epsilon"],
            "smoothing_bandwidth": vp["bandwidth"],
            "published_target": 0.075,
            "pass": bool(abs(vp["peak_epsilon"] - 0.075) <= 0.02),
        },
        "G4_decay_transition": {
            "segmented_break_epsilon": db["break_epsilon"],
            "left_slope": db["left_slope"],
            "right_slope": db["right_slope"],
            "published_target": 0.075,
            "pass": bool(abs(db["break_epsilon"] - 0.075) <= 0.02 and db["right_slope"] > db["left_slope"]),
        },
    }
    status = "PASS_PHYSICS_RECONSTRUCTION" if all(v["pass"] for v in checks.values()) else "PARTIAL_PHYSICS_RECONSTRUCTION"

    validation = {
        "status": status,
        "scope": "Independent reconstruction from the supplied raw .dat corpus and the Methods equations/thresholds; original unpublished figure-analysis code was not supplied.",
        "input": {
            "path": str(data_path),
            "sha256": sha256(data_path) if data_path.is_file() else None,
            "dat_files": len(source.names()),
        },
        "parameters": {
            "W0": args.W0,
            "Wf_ratio": args.Wf_ratio,
            "Wf": args.W0 * args.Wf_ratio,
            "final_points_for_eq4": 5,
            "post_transient_window": [13, 17],
            "eq7_fit_start": 13,
            "decay_fit_window": [13, 30],
        },
        "transition": {
            "variance_raw_peak_epsilon": vp["raw_peak_epsilon"],
            "variance_smoothed_peak_epsilon": vp["peak_epsilon"],
            "decay_break_epsilon": db["break_epsilon"],
            "consensus_epsilon": consensus,
            "published_reference_epsilon_c": 0.075,
            "absolute_consensus_difference": abs(consensus - 0.075),
        },
        "checks": checks,
        "notes": [
            "No UNNS metric is calculated in this package.",
            "Repeated supplied files at the same epsilon are aggregated by median; file-level results are preserved.",
            "The variance raw discrete maximum and the smoothed peak are both reported to avoid hiding corpus scatter.",
            "The Gaussian smoothing bandwidth is generated from the data grid: 2.5 times the median epsilon spacing below 0.20.",
            "Because the authors' separate analysis/error-mitigation code is not in the supplied Qiskit notebook, this is a transparent reconstruction rather than a byte-for-byte reproduction."
        ],
    }
    (out / "physics_validation.json").write_text(json.dumps(validation, indent=2), encoding="utf-8")

    log = [
        f"STATUS: {status}",
        f"DAT files: {len(source.names())}",
        f"variance raw peak epsilon: {vp['raw_peak_epsilon']:.6f}",
        f"variance smoothed peak epsilon: {vp['peak_epsilon']:.6f}",
        f"decay segmented break epsilon: {db['break_epsilon']:.6f}",
        f"consensus epsilon: {consensus:.6f}",
        f"published reference epsilon_c: 0.075000",
        f"|consensus - 0.075|: {abs(consensus-0.075):.6f}",
        f"DTC/thermal half-frequency ratio: {hf_ratio:.3f}",
        f"DTC late aligned mean: {dtc_late:.6f}",
        f"thermal late abs aligned mean: {thermal_late:.6f}",
    ]
    (out / "RUN_LOG.txt").write_text("\n".join(log) + "\n", encoding="utf-8")
    print("\n".join(log))


if __name__ == "__main__":
    main()

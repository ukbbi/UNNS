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

from tc_closure import (
    load_phys_module, reconstruct_unaligned_trajectory, closure_spectrum,
    detect_fundamental_q, family_contrast, plateau_exit_boundary, shuffle_null
)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024*1024), b""):
            h.update(block)
    return h.hexdigest()


def write_csv(path: Path, rows: list[dict]):
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fields = []
    for r in rows:
        for k in r:
            if k not in fields:
                fields.append(k)
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


def aggregate_spec(file_spec_rows, eps_subset):
    out = []
    qs = sorted(set(r["q"] for r in file_spec_rows))
    for q in qs:
        vals = [
            r["closure"] for r in file_spec_rows
            if r["regular"] and r["epsilon"] in eps_subset and r["q"] == q
        ]
        out.append({"q": q, "closure": float(np.nanmedian(vals))})
    return out


def main():
    ap = argparse.ArgumentParser(description="UNNS temporal closure spectrum, exploratory v001.")
    ap.add_argument("data", help="Path to original Data.zip")
    ap.add_argument("phys", help="Path to frozen TC_PHYS_v001")
    ap.add_argument("output", nargs="?", default="outputs")
    ap.add_argument("--qmax", type=int, default=10)
    ap.add_argument("--W0", type=float, default=0.15)
    ap.add_argument("--Wf-ratio", type=float, default=2.0/3.0)
    args = ap.parse_args()

    data = Path(args.data).resolve()
    phys = Path(args.phys).resolve()
    out = Path(args.output).resolve()
    out.mkdir(parents=True, exist_ok=True)

    # ---- Firewall gate: only the PASS status is read before closure analysis.
    phys_validation_path = phys / "outputs" / "physics_validation.json"
    if not phys_validation_path.exists():
        raise FileNotFoundError(f"Missing physics validation: {phys_validation_path}")
    phys_gate = json.loads(phys_validation_path.read_text(encoding="utf-8"))
    if not str(phys_gate.get("status", "")).startswith("PASS"):
        raise RuntimeError(f"Physics layer is not frozen PASS: {phys_gate.get('status')}")

    tc_phys = load_phys_module(phys)
    source = tc_phys.DataSource(data)

    file_spec = []
    ladder_rows = []
    record_summary = []
    trajectories = {}

    for name, arr in source.iter_arrays():
        rec, mit, x = reconstruct_unaligned_trajectory(
            tc_phys, name, arr, W0=args.W0, Wf_ratio=args.Wf_ratio
        )
        ok = mit["accepted"]
        if int(ok.sum()) < 5:
            continue

        spec, ladders, amp0 = closure_spectrum(x, ok, qmax=args.qmax)
        trajectories[name] = (x, ok, rec)

        for s in spec:
            file_spec.append({
                "filename": name,
                "epsilon": rec.epsilon,
                "regular": bool(tc_phys.is_regular_file(name)),
                "device": rec.meta["device"],
                "initial_state": rec.meta["initial_state"],
                "disorder": rec.meta["disorder"],
                **s,
            })
        for lr in ladders:
            ladder_rows.append({
                "filename": name,
                "epsilon": rec.epsilon,
                "regular": bool(tc_phys.is_regular_file(name)),
                **lr,
            })

        record_summary.append({
            "filename": name,
            "epsilon": rec.epsilon,
            "regular": bool(tc_phys.is_regular_file(name)),
            "device": rec.meta["device"],
            "initial_state": rec.meta["initial_state"],
            "disorder": rec.meta["disorder"],
            "accepted_qubits": int(ok.sum()),
            "early_RMS_reference": amp0,
        })

    # ---- Generic recurrence depth detection from the first five epsilon points.
    regular_eps = sorted(set(r["epsilon"] for r in file_spec if r["regular"]))
    seed_eps = regular_eps[:5]
    seed_spec = aggregate_spec(file_spec, set(seed_eps))
    qdet = detect_fundamental_q(seed_spec)
    q0 = qdet["q0"]

    # ---- Build epsilon scan. No physical labels are used.
    scan = []
    for eps in regular_eps:
        rows_e = [r for r in file_spec if r["regular"] and r["epsilon"] == eps]
        by_file = {}
        for r in rows_e:
            by_file.setdefault(r["filename"], []).append(r)
        fam = []
        c_q0 = []
        first_peak = []
        for name, sr in by_file.items():
            sr = sorted(sr, key=lambda z: z["q"])
            fc = family_contrast(sr, q0)
            fam.append(fc["family_contrast"])
            qrow = next(z for z in sr if z["q"] == q0)
            c_q0.append(qrow["closure"])

            cs = {z["q"]: z["closure"] for z in sr}
            peaks = [
                q for q in range(2, args.qmax)
                if cs[q] > cs[q-1] and cs[q] > cs[q+1]
            ]
            first_peak.append(peaks[0] if peaks else np.nan)

        scan.append({
            "epsilon": eps,
            "n_files": len(by_file),
            "closure_q0_median": float(np.nanmedian(c_q0)),
            "family_contrast": float(np.nanmedian(fam)),
            "first_local_peak_q_median": float(np.nanmedian(first_peak)) if np.isfinite(first_peak).any() else np.nan,
        })

    # ---- Exploratory closure-basin boundary.
    basin = plateau_exit_boundary(
        scan, key="family_contrast", seed_n=5, sigma_mult=3.0, consecutive=2
    )

    # ---- Sensitivity of the basin rule itself (not physics mitigation thresholds).
    basin_sensitivity = []
    for seed_n in (4, 5, 6):
        for sm in (2.0, 2.5, 3.0):
            b = plateau_exit_boundary(
                scan, key="family_contrast", seed_n=seed_n,
                sigma_mult=sm, consecutive=2
            )
            basin_sensitivity.append({
                "seed_n": seed_n,
                "sigma_mult": sm,
                "consecutive": 2,
                "boundary_epsilon": b["boundary_epsilon"],
                "lower_threshold": b["lower_threshold"],
            })

    # ---- Physics-mitigation threshold sensitivity of the closure boundary.
    threshold_sensitivity = []
    for W0 in (0.12, 0.15, 0.18):
        for ratio in (0.50, 2.0/3.0, 0.80):
            local_file_spec = []
            for name, arr in source.iter_arrays():
                rec, mit, x = reconstruct_unaligned_trajectory(
                    tc_phys, name, arr, W0=W0, Wf_ratio=ratio
                )
                ok = mit["accepted"]
                if int(ok.sum()) < 5:
                    continue
                spec, _, _ = closure_spectrum(x, ok, qmax=args.qmax)
                if not tc_phys.is_regular_file(name):
                    continue
                for s in spec:
                    local_file_spec.append({
                        "filename": name, "epsilon": rec.epsilon, **s
                    })

            local_eps = sorted(set(r["epsilon"] for r in local_file_spec))
            local_scan = []
            for eps in local_eps:
                rows_e = [r for r in local_file_spec if r["epsilon"] == eps]
                by_file = {}
                for r in rows_e:
                    by_file.setdefault(r["filename"], []).append(r)
                fcs = [family_contrast(sorted(sr, key=lambda z: z["q"]), q0)["family_contrast"]
                       for sr in by_file.values()]
                local_scan.append({
                    "epsilon": eps,
                    "family_contrast": float(np.nanmedian(fcs)),
                })
            bb = plateau_exit_boundary(
                local_scan, key="family_contrast",
                seed_n=5, sigma_mult=3.0, consecutive=2
            )
            threshold_sensitivity.append({
                "W0": W0,
                "Wf_ratio": ratio,
                "Wf": W0*ratio,
                "boundary_epsilon": bb["boundary_epsilon"],
            })

    # ---- Controls at epsilon 0.05 and time-shuffle null.
    controls = []
    for name, (x, ok, rec) in trajectories.items():
        if abs(rec.epsilon - 0.05) > 1e-12:
            continue
        spec, _, _ = closure_spectrum(x, ok, qmax=args.qmax)
        fc = family_contrast(spec, q0)
        controls.append({
            "filename": name,
            "regular": bool(tc_phys.is_regular_file(name)),
            "device": rec.meta["device"],
            "initial_state": rec.meta["initial_state"],
            "disorder": rec.meta["disorder"],
            "accepted_qubits": int(ok.sum()),
            "closure_q0": next(r["closure"] for r in spec if r["q"] == q0),
            **fc,
        })

    # Fixed representative low-epsilon standard run for null.
    null_name = "NewFloq_REF_Bro57_Eps005_T50_5IT_16Sep.dat"
    null_result = None
    if null_name in trajectories:
        x, ok, _ = trajectories[null_name]
        null_result = {"filename": null_name, **shuffle_null(x, ok, q0)}

    # ---- Write primary closure result BEFORE reading physical epsilon_c.
    closure_result = {
        "status": "TC_CLOSURE_V001_COMPLETE",
        "scope": "Exploratory UNNS temporal-closure construction on the frozen physics-validated trajectories.",
        "firewall": {
            "physics_gate_status_checked": phys_gate["status"],
            "physics_transition_value_used_in_metric": False,
            "physical_phase_labels_used_in_metric": False,
            "period_q_hardcoded": False,
            "note": "q0 is detected from the closure spectrum itself. This v001 analysis is exploratory, not a prospective preregistration."
        },
        "parameters": {
            "qmax": args.qmax,
            "early_amplitude_points": 5,
            "physics_W0": args.W0,
            "physics_Wf_ratio": args.Wf_ratio,
            "seed_epsilon_points_for_q_detection": seed_eps,
            "basin_detector": {
                "seed_n": 5,
                "sigma_mult": 3.0,
                "consecutive": 2,
            },
        },
        "fundamental_recurrence": qdet,
        "closure_basin": basin,
        "shuffle_null": null_result,
    }
    (out / "closure_result.json").write_text(json.dumps(closure_result, indent=2), encoding="utf-8")

    write_csv(out / "closure_spectrum.csv", file_spec)
    write_csv(out / "ladder_closure.csv", ladder_rows)
    write_csv(out / "record_summary.csv", record_summary)
    write_csv(out / "closure_scan.csv", scan)
    write_csv(out / "control_comparison.csv", controls)
    write_csv(out / "basin_sensitivity.csv", basin_sensitivity)
    write_csv(out / "threshold_sensitivity.csv", threshold_sensitivity)

    # ---- Figures.
    # Aggregate seed spectrum.
    plt.figure(figsize=(8.0, 4.8))
    plt.plot(
        [r["q"] for r in seed_spec],
        [r["closure"] for r in seed_spec],
        marker="o", linewidth=1.3
    )
    plt.axvline(q0, linestyle="--", linewidth=1, label=f"detected q0={q0}")
    plt.xlabel("Recurrence depth q")
    plt.ylabel("Temporal closure C(q)")
    plt.title("Low-perturbation temporal closure spectrum")
    plt.xticks(range(1, args.qmax+1))
    plt.legend()
    plt.tight_layout()
    plt.savefig(out / "closure_spectrum.png", dpi=180)
    plt.close()

    xeps = np.asarray([r["epsilon"] for r in scan], dtype=float)
    c0 = np.asarray([r["closure_q0_median"] for r in scan], dtype=float)
    fc = np.asarray([r["family_contrast"] for r in scan], dtype=float)

    plt.figure(figsize=(8.2, 4.9))
    plt.plot(xeps, c0, marker="o", markersize=3, linewidth=1.1)
    plt.xlabel("epsilon")
    plt.ylabel(f"Median C({q0})")
    plt.title(f"Fundamental temporal closure across perturbation space (q0={q0})")
    plt.tight_layout()
    plt.savefig(out / "closure_q0_scan.png", dpi=180)
    plt.close()

    plt.figure(figsize=(8.2, 4.9))
    plt.plot(xeps, fc, marker="o", markersize=3, linewidth=1.1, label="recurrence-family contrast")
    plt.axhline(basin["lower_threshold"], linestyle=":", linewidth=1, label="seed-basin lower edge")
    if np.isfinite(basin["boundary_epsilon"]):
        plt.axvline(basin["boundary_epsilon"], linestyle="--", linewidth=1,
                    label=f"exploratory basin exit={basin['boundary_epsilon']:.3f}")
    plt.xlabel("epsilon")
    plt.ylabel("Family closure contrast")
    plt.title("Temporal recurrence-family rigidity")
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(out / "closure_basin.png", dpi=180)
    plt.close()

    if controls:
        names = [Path(r["filename"]).stem[-22:] for r in controls]
        vals = [r["family_contrast"] for r in controls]
        plt.figure(figsize=(9.0, 5.0))
        plt.bar(range(len(vals)), vals)
        plt.xticks(range(len(vals)), names, rotation=40, ha="right", fontsize=7)
        plt.ylabel("Family closure contrast")
        plt.title("epsilon=0.05 supplied-state/control comparison")
        plt.tight_layout()
        plt.savefig(out / "controls.png", dpi=180)
        plt.close()

    # ---- Post-lock comparison: only now read the frozen physical transition.
    phys_transition = phys_gate.get("transition", {}).get("published_reference_epsilon_c")
    closure_boundary = basin["boundary_epsilon"]
    posthoc = {
        "comparison_stage": "POST_LOCK",
        "closure_boundary_epsilon": closure_boundary,
        "physical_reference_epsilon_c": phys_transition,
        "absolute_difference": (
            abs(float(closure_boundary) - float(phys_transition))
            if np.isfinite(closure_boundary) and phys_transition is not None else None
        ),
        "epsilon_grid_note": "The closure boundary is a discrete observed epsilon grid value; no interpolation toward the physical target is performed.",
    }
    (out / "posthoc_comparison.json").write_text(json.dumps(posthoc, indent=2), encoding="utf-8")

    log = [
        "STATUS: TC_CLOSURE_V001_COMPLETE",
        f"Physics firewall gate: {phys_gate['status']}",
        f"DAT files examined: {len(source.names())}",
        f"qmax: {args.qmax}",
        f"Detected fundamental recurrence q0: {q0}",
        f"q0 local spectral contrast: {qdet['local_contrast']:.6f}",
        f"Exploratory family-closure basin exit epsilon: {closure_boundary:.6f}",
        f"Physical reference epsilon_c (post-lock comparison only): {phys_transition:.6f}",
        f"Absolute boundary difference: {posthoc['absolute_difference']:.6f}",
    ]
    if null_result:
        log += [
            f"Shuffle-null observed C(q0): {null_result['observed']:.6f}",
            f"Shuffle-null mean: {null_result['null_mean']:.6f}",
            f"Shuffle-null empirical p_ge: {null_result['empirical_p_ge']:.6f}",
        ]
    (out / "RUN_LOG.txt").write_text("\n".join(log) + "\n", encoding="utf-8")
    print("\n".join(log))


if __name__ == "__main__":
    main()

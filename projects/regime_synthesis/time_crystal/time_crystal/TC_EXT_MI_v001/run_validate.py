from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import numpy as np
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "src"))
from mi_adapter import (
    load_fig2d_state_trajectories,
    load_fig3a_initial_state_trajectories,
    load_fig3a_pairwise_trajectories,
)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def write_csv(path: Path, rows: list[dict]):
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fields = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)


def load_locked_metric(lock_root: Path):
    lock = json.loads((lock_root / "LOCK.json").read_text(encoding="utf-8"))
    metric_path = lock_root / "src" / "tc_closure.py"
    got = sha256(metric_path)
    expected = lock["frozen_files"]["src/tc_closure.py"]
    if got != expected:
        raise RuntimeError(
            "Frozen metric hash mismatch.\n"
            f"Expected: {expected}\n"
            f"Observed: {got}"
        )

    spec = importlib.util.spec_from_file_location("tc_closure_LOCKED", metric_path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return lock, module, got


def run_locked(tc, X: np.ndarray, label: str) -> dict:
    accepted = np.ones(X.shape[1], dtype=bool)
    spectrum, ladders, amp0 = tc.closure_spectrum(X, accepted, qmax=10)
    qdet = tc.detect_fundamental_q(spectrum)
    fam = tc.family_contrast(spectrum, qdet["q0"])
    null = tc.shuffle_null(X, accepted, qdet["q0"])
    return {
        "label": label,
        "n_time": int(X.shape[0]),
        "n_coordinates": int(X.shape[1]),
        "early_RMS_reference": float(amp0),
        "spectrum": spectrum,
        "q_detection": qdet,
        "family": fam,
        "shuffle_null": null,
    }


def compact(result: dict, class_name: str, source_figure: str) -> dict:
    return {
        "label": result["label"],
        "source_figure": source_figure,
        "comparison_class": class_name,
        "n_time": result["n_time"],
        "n_coordinates": result["n_coordinates"],
        "detected_q0": result["q_detection"]["q0"],
        "q0_local_contrast": result["q_detection"]["local_contrast"],
        "closure_q0": next(
            r["closure"] for r in result["spectrum"]
            if r["q"] == result["q_detection"]["q0"]
        ),
        "family_mean": result["family"]["family_mean"],
        "nonfamily_mean": result["family"]["nonfamily_mean"],
        "family_contrast": result["family"]["family_contrast"],
        "shuffle_null_mean": result["shuffle_null"]["null_mean"],
        "shuffle_null_q99": result["shuffle_null"]["null_q99"],
        "shuffle_p_ge": result["shuffle_null"]["empirical_p_ge"],
    }


def main():
    ap = argparse.ArgumentParser(
        description="External Mi et al. validation using frozen TC_CLOSURE_LOCK_v001."
    )
    ap.add_argument("data", help="Path to DTC_Data.zip")
    ap.add_argument("lock", help="Path to TC_CLOSURE_LOCK_v001")
    ap.add_argument("output", nargs="?", default="outputs")
    args = ap.parse_args()

    data = Path(args.data).resolve()
    lock_root = Path(args.lock).resolve()
    out = Path(args.output).resolve()
    out.mkdir(parents=True, exist_ok=True)

    lock, tc, metric_sha = load_locked_metric(lock_root)

    fig2 = load_fig2d_state_trajectories(data)
    fig3 = load_fig3a_initial_state_trajectories(data)
    pairs = load_fig3a_pairwise_trajectories(data)

    results = {}
    for label, X in {**fig2, **fig3, **pairs}.items():
        results[label] = run_locked(tc, X, label)

    summary_rows = [
        compact(results["fig2d_g097"], "MBL-DTC positive", "Fig. 2d"),
        compact(results["fig2d_g060"], "thermal control", "Fig. 2d"),
        compact(results["fig3a_mbl"], "MBL-DTC initial-state set", "Fig. 3a"),
        compact(results["fig3a_prethermal"], "prethermal DTC-like control", "Fig. 3a"),
    ]
    write_csv(out / "external_summary.csv", summary_rows)

    spectrum_rows = []
    for key in ["fig2d_g097", "fig2d_g060", "fig3a_mbl", "fig3a_prethermal"]:
        rr = results[key]
        for row in rr["spectrum"]:
            spectrum_rows.append({
                "label": key,
                "q": row["q"],
                "closure": row["closure"],
                "similarity": row["similarity"],
                "support": row["support"],
                "n_pairs": row["n_pairs"],
            })
    write_csv(out / "external_spectra.csv", spectrum_rows)

    pair_rows = []
    for key in sorted(pairs):
        rr = results[key]
        pair_rows.append({
            "label": key,
            "regime": "prethermal" if "prethermal" in key else "mbl",
            "detected_q0": rr["q_detection"]["q0"],
            "closure_q0": next(
                r["closure"] for r in rr["spectrum"]
                if r["q"] == rr["q_detection"]["q0"]
            ),
            "family_contrast": rr["family"]["family_contrast"],
            "shuffle_p_ge": rr["shuffle_null"]["empirical_p_ge"],
        })
    write_csv(out / "initial_state_pairwise.csv", pair_rows)

    # Fixed descriptive universality summary across all 3 choose 2 pairs.
    universality = {}
    for regime in ("mbl", "prethermal"):
        vals = np.asarray(
            [r["family_contrast"] for r in pair_rows if r["regime"] == regime],
            dtype=float,
        )
        ps = np.asarray(
            [r["shuffle_p_ge"] for r in pair_rows if r["regime"] == regime],
            dtype=float,
        )
        universality[regime] = {
            "pairwise_family_contrast_mean": float(np.mean(vals)),
            "pairwise_family_contrast_std": float(np.std(vals, ddof=1)),
            "pairwise_family_contrast_min": float(np.min(vals)),
            "pairwise_family_contrast_max": float(np.max(vals)),
            "significant_shuffle_pairs_p_lt_0_05": int(np.sum(ps < 0.05)),
            "pair_count": int(len(vals)),
        }

    # Result object. No numerical thresholds are retrofitted into the frozen metric.
    validation = {
        "status": "EXTERNAL_VALIDATION_COMPLETE",
        "dataset": "Mi et al. DTC_Data.zip",
        "data_sha256": sha256(data),
        "frozen_lock_id": lock["lock_id"],
        "frozen_metric_sha256": metric_sha,
        "metric_modified": False,
        "adapter_scope": [
            "transpose Fig. 2d qubit-by-time matrices into X_t vectors",
            "group all three Fig. 3a initial-state traces into an X_t vector",
            "evaluate all 3 choose 2 initial-state pairs without selection",
        ],
        "primary_results": {
            "mbl_dtc_fig2d": summary_rows[0],
            "thermal_fig2d": summary_rows[1],
            "mbl_initial_states_fig3a": summary_rows[2],
            "prethermal_fig3a": summary_rows[3],
        },
        "pairwise_initial_state_universality": universality,
        "interpretation_guardrail": (
            "This is an independent-dataset test of a frozen metric, but the "
            "Mi-specific adapter was constructed after inspecting the public CSV "
            "layout. Treat the result as external metric validation, not as a "
            "fully preregistered end-to-end experiment."
        ),
    }
    (out / "external_validation.json").write_text(
        json.dumps(validation, indent=2), encoding="utf-8"
    )

    # Figures.
    plt.figure(figsize=(8.2, 4.9))
    for key in ["fig2d_g097", "fig2d_g060"]:
        rr = results[key]
        plt.plot(
            [r["q"] for r in rr["spectrum"]],
            [r["closure"] for r in rr["spectrum"]],
            marker="o",
            linewidth=1.2,
            label=key,
        )
    plt.xlabel("Recurrence depth q")
    plt.ylabel("Frozen temporal closure C(q)")
    plt.title("Independent site-resolved test: MBL-DTC vs thermal")
    plt.xticks(range(1, 11))
    plt.legend()
    plt.tight_layout()
    plt.savefig(out / "fig2d_closure_spectra.png", dpi=180)
    plt.close()

    plt.figure(figsize=(8.2, 4.9))
    for key in ["fig3a_mbl", "fig3a_prethermal"]:
        rr = results[key]
        plt.plot(
            [r["q"] for r in rr["spectrum"]],
            [r["closure"] for r in rr["spectrum"]],
            marker="o",
            linewidth=1.2,
            label=key,
        )
    plt.xlabel("Recurrence depth q")
    plt.ylabel("Frozen temporal closure C(q)")
    plt.title("Independent initial-state test: MBL-DTC vs prethermal")
    plt.xticks(range(1, 11))
    plt.legend()
    plt.tight_layout()
    plt.savefig(out / "fig3a_closure_spectra.png", dpi=180)
    plt.close()

    labels = ["MBL-DTC\nFig.2d", "thermal\nFig.2d", "MBL\nFig.3a", "prethermal\nFig.3a"]
    vals = [r["family_contrast"] for r in summary_rows]
    plt.figure(figsize=(7.8, 4.8))
    plt.bar(range(len(vals)), vals)
    plt.xticks(range(len(vals)), labels)
    plt.ylabel("Frozen recurrence-family contrast")
    plt.title("External control separation")
    plt.tight_layout()
    plt.savefig(out / "family_contrast_comparison.png", dpi=180)
    plt.close()

    # Pairwise initial-state stability.
    mbl_vals = [r["family_contrast"] for r in pair_rows if r["regime"] == "mbl"]
    pre_vals = [r["family_contrast"] for r in pair_rows if r["regime"] == "prethermal"]
    plt.figure(figsize=(7.8, 4.8))
    x1 = np.arange(len(mbl_vals))
    x2 = np.arange(len(pre_vals)) + len(mbl_vals) + 1
    plt.scatter(x1, mbl_vals, s=45, label="MBL-DTC pairs")
    plt.scatter(x2, pre_vals, s=45, label="prethermal pairs")
    plt.axhline(np.mean(mbl_vals), linewidth=1)
    plt.axhline(np.mean(pre_vals), linewidth=1)
    plt.xticks([])
    plt.ylabel("Frozen recurrence-family contrast")
    plt.title("All pairwise initial-state combinations")
    plt.legend()
    plt.tight_layout()
    plt.savefig(out / "initial_state_pairwise.png", dpi=180)
    plt.close()

    # Compact log.
    a, b, c, d = summary_rows
    log = [
        "STATUS: EXTERNAL_VALIDATION_COMPLETE",
        f"LOCK VERIFIED: {lock['lock_id']}",
        f"Metric SHA256: {metric_sha}",
        "",
        "FIG. 2d SITE-RESOLVED TEST",
        f"MBL-DTC g=0.97: q0={a['detected_q0']}, C(q0)={a['closure_q0']:.6f}, family={a['family_contrast']:.6f}, shuffle p={a['shuffle_p_ge']:.6f}",
        f"Thermal g=0.60: q0={b['detected_q0']}, C(q0)={b['closure_q0']:.6f}, family={b['family_contrast']:.6f}, shuffle p={b['shuffle_p_ge']:.6f}",
        "",
        "FIG. 3a INITIAL-STATE TEST",
        f"MBL-DTC g=0.94: q0={c['detected_q0']}, C(q0)={c['closure_q0']:.6f}, family={c['family_contrast']:.6f}, shuffle p={c['shuffle_p_ge']:.6f}",
        f"Prethermal g=0.94: q0={d['detected_q0']}, C(q0)={d['closure_q0']:.6f}, family={d['family_contrast']:.6f}, shuffle p={d['shuffle_p_ge']:.6f}",
        "",
        "PAIRWISE INITIAL-STATE STABILITY",
        f"MBL family contrast mean±sd: {universality['mbl']['pairwise_family_contrast_mean']:.6f} ± {universality['mbl']['pairwise_family_contrast_std']:.6f}",
        f"Prethermal family contrast mean±sd: {universality['prethermal']['pairwise_family_contrast_mean']:.6f} ± {universality['prethermal']['pairwise_family_contrast_std']:.6f}",
        f"MBL shuffle-significant pairs: {universality['mbl']['significant_shuffle_pairs_p_lt_0_05']}/3",
        f"Prethermal shuffle-significant pairs: {universality['prethermal']['significant_shuffle_pairs_p_lt_0_05']}/3",
    ]
    (out / "RUN_LOG.txt").write_text("\n".join(log) + "\n", encoding="utf-8")
    print("\n".join(log))


if __name__ == "__main__":
    main()

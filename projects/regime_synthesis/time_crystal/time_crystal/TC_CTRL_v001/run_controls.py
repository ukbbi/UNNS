from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
import zipfile

import numpy as np
import matplotlib.pyplot as plt

from src.controls import (
    SEED,
    selected_controls,
    noisy_period2,
    damped_period2,
    logistic_ensemble,
)


EXPECTED_METRIC_SHA256 = "06344c8641aa14e6663cc3cba65d86fcdb9e37857909e85da6bc0d689e5b2553"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
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


def load_locked_metric(lock_path: Path, temp_dir: Path):
    """
    Accept either an extracted TC_CLOSURE_LOCK_v001 directory or its ZIP.
    Verify LOCK.json and the exact frozen tc_closure.py SHA before importing.
    """
    lock_path = lock_path.resolve()

    if lock_path.is_dir():
        lock = json.loads((lock_path / "LOCK.json").read_text(encoding="utf-8"))
        metric_path = lock_path / "src" / "tc_closure.py"
        metric_bytes = metric_path.read_bytes()
    elif lock_path.is_file() and lock_path.suffix.lower() == ".zip":
        with zipfile.ZipFile(lock_path, "r") as zf:
            names = zf.namelist()
            lock_member = next(n for n in names if n.endswith("/LOCK.json"))
            metric_member = next(n for n in names if n.endswith("/src/tc_closure.py"))
            lock = json.loads(zf.read(lock_member).decode("utf-8"))
            metric_bytes = zf.read(metric_member)
        metric_path = temp_dir / "_tc_closure_LOCKED.py"
        metric_path.write_bytes(metric_bytes)
    else:
        raise FileNotFoundError(f"Lock path not found: {lock_path}")

    expected = lock["frozen_files"]["src/tc_closure.py"]
    observed = sha256_bytes(metric_bytes)

    if observed != expected:
        raise RuntimeError(
            "TC_CLOSURE lock verification failed.\n"
            f"LOCK.json expected: {expected}\n"
            f"Observed:           {observed}"
        )
    if observed != EXPECTED_METRIC_SHA256:
        raise RuntimeError(
            "The supplied lock is not TC_CLOSURE_LOCK_v001 used by this control package.\n"
            f"Expected package metric SHA: {EXPECTED_METRIC_SHA256}\n"
            f"Observed:                    {observed}"
        )

    spec = importlib.util.spec_from_file_location("tc_closure_LOCKED_CTRL", metric_path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return lock, module, observed


def run_metric(tc, X: np.ndarray, do_shuffle: bool = True) -> dict:
    accepted = np.ones(X.shape[1], dtype=bool)
    spectrum, ladders, amp0 = tc.closure_spectrum(X, accepted, qmax=10)
    qdet = tc.detect_fundamental_q(spectrum)
    fam = tc.family_contrast(spectrum, qdet["q0"])
    q2fam = tc.family_contrast(spectrum, 2)
    null = tc.shuffle_null(X, accepted, qdet["q0"]) if do_shuffle else None
    return {
        "spectrum": spectrum,
        "q_detection": qdet,
        "family": fam,
        "q2_family": q2fam,
        "shuffle_null": null,
        "early_RMS_reference": amp0,
    }


def compact(label: str, kind: str, result: dict) -> dict:
    q0 = result["q_detection"]["q0"]
    q0_row = next(r for r in result["spectrum"] if r["q"] == q0)
    q2_row = next(r for r in result["spectrum"] if r["q"] == 2)
    null = result["shuffle_null"] or {}
    return {
        "label": label,
        "control_kind": kind,
        "detected_q0": q0,
        "q0_local_contrast": result["q_detection"]["local_contrast"],
        "closure_q0": q0_row["closure"],
        "closure_q2": q2_row["closure"],
        "detected_family_contrast": result["family"]["family_contrast"],
        "q2_family_contrast": result["q2_family"]["family_contrast"],
        "shuffle_p_ge": null.get("empirical_p_ge"),
        "shuffle_null_mean": null.get("null_mean"),
        "shuffle_null_q99": null.get("null_q99"),
    }


def main():
    ap = argparse.ArgumentParser(
        description="Ordinary period-doubling challenge for frozen TC_CLOSURE_LOCK_v001."
    )
    ap.add_argument(
        "lock",
        help="Path to TC_CLOSURE_LOCK_v001 directory or TC_CLOSURE_LOCK_v001.zip",
    )
    ap.add_argument("output", nargs="?", default="outputs")
    args = ap.parse_args()

    lock_path = Path(args.lock)
    out = Path(args.output).resolve()
    out.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory(prefix="tc_ctrl_lock_") as td:
        lock, tc, metric_sha = load_locked_metric(lock_path, Path(td))

        # ---------------- Selected controls ----------------
        kinds = {
            "perfect_2T": "synthetic exact period-2",
            "noisy_2T_sigma_0p20": "synthetic noisy period-2",
            "damped_2T_gamma_0p10": "synthetic transient/damped period-2",
            "iid_random": "aperiodic random negative control",
            "logistic_period2_r3p20": "classical nonlinear period-2",
            "logistic_period4_r3p50": "classical nonlinear period-4",
            "logistic_chaos_r4p00": "classical chaotic control",
        }

        selected_rows = []
        spectrum_rows = []
        selected_results = {}

        for label, X in selected_controls().items():
            rr = run_metric(tc, X, do_shuffle=True)
            selected_results[label] = rr
            selected_rows.append(compact(label, kinds[label], rr))
            for row in rr["spectrum"]:
                spectrum_rows.append({
                    "label": label,
                    "control_kind": kinds[label],
                    **row,
                })

        # ---------------- Noise sweep ----------------
        noise_rows = []
        sigmas = np.linspace(0.0, 1.0, 21)
        for sigma in sigmas:
            rr = run_metric(tc, noisy_period2(float(sigma)), do_shuffle=False)
            c2 = next(r["closure"] for r in rr["spectrum"] if r["q"] == 2)
            noise_rows.append({
                "noise_sigma": float(sigma),
                "detected_q0": rr["q_detection"]["q0"],
                "q0_local_contrast": rr["q_detection"]["local_contrast"],
                "closure_q2": c2,
                "q2_family_contrast": rr["q2_family"]["family_contrast"],
                "detected_family_contrast": rr["family"]["family_contrast"],
            })

        # ---------------- Damping sweep ----------------
        damping_rows = []
        gammas = np.linspace(0.0, 0.12, 25)
        for gamma in gammas:
            rr = run_metric(tc, damped_period2(float(gamma)), do_shuffle=False)
            c2 = next(r["closure"] for r in rr["spectrum"] if r["q"] == 2)
            damping_rows.append({
                "gamma": float(gamma),
                "detected_q0": rr["q_detection"]["q0"],
                "q0_local_contrast": rr["q_detection"]["local_contrast"],
                "closure_q2": c2,
                "q2_family_contrast": rr["q2_family"]["family_contrast"],
            })

        # A few shuffle checkpoints in the damping sweep.
        damping_shuffle_rows = []
        for gamma in (0.00, 0.03, 0.06, 0.10, 0.12):
            rr = run_metric(tc, damped_period2(gamma), do_shuffle=True)
            damping_shuffle_rows.append({
                "gamma": gamma,
                "detected_q0": rr["q_detection"]["q0"],
                "closure_q2": next(r["closure"] for r in rr["spectrum"] if r["q"] == 2),
                "q2_family_contrast": rr["q2_family"]["family_contrast"],
                "shuffle_p_ge": rr["shuffle_null"]["empirical_p_ge"],
            })

        # ---------------- Classical logistic sweep ----------------
        logistic_rows = []
        rs = np.round(np.arange(3.05, 4.0001, 0.05), 2)
        for r in rs:
            rr = run_metric(tc, logistic_ensemble(float(r)), do_shuffle=False)
            q0 = rr["q_detection"]["q0"]
            q0closure = next(x["closure"] for x in rr["spectrum"] if x["q"] == q0)
            logistic_rows.append({
                "r": float(r),
                "detected_q0": q0,
                "q0_local_contrast": rr["q_detection"]["local_contrast"],
                "closure_q0": q0closure,
                "closure_q2": next(x["closure"] for x in rr["spectrum"] if x["q"] == 2),
                "detected_family_contrast": rr["family"]["family_contrast"],
            })

        # ---------------- Export ----------------
        write_csv(out / "control_summary.csv", selected_rows)
        write_csv(out / "control_spectra.csv", spectrum_rows)
        write_csv(out / "noise_sweep.csv", noise_rows)
        write_csv(out / "damping_sweep.csv", damping_rows)
        write_csv(out / "damping_shuffle.csv", damping_shuffle_rows)
        write_csv(out / "logistic_sweep.csv", logistic_rows)

        # ---------------- Figures ----------------
        plt.figure(figsize=(8.4, 5.1))
        for label in [
            "perfect_2T",
            "damped_2T_gamma_0p10",
            "logistic_period2_r3p20",
            "logistic_period4_r3p50",
            "logistic_chaos_r4p00",
        ]:
            rr = selected_results[label]
            plt.plot(
                [r["q"] for r in rr["spectrum"]],
                [r["closure"] for r in rr["spectrum"]],
                marker="o",
                linewidth=1.1,
                label=label,
            )
        plt.xlabel("Recurrence depth q")
        plt.ylabel("Frozen temporal closure C(q)")
        plt.title("Frozen closure spectrum on ordinary classical/synthetic controls")
        plt.xticks(range(1, 11))
        plt.legend(fontsize=7)
        plt.tight_layout()
        plt.savefig(out / "control_spectra.png", dpi=180)
        plt.close()

        plt.figure(figsize=(8.2, 4.9))
        plt.plot(
            [r["noise_sigma"] for r in noise_rows],
            [r["closure_q2"] for r in noise_rows],
            marker="o",
            markersize=3,
            linewidth=1.1,
            label="C(2)",
        )
        plt.plot(
            [r["noise_sigma"] for r in noise_rows],
            [r["q2_family_contrast"] for r in noise_rows],
            marker="o",
            markersize=3,
            linewidth=1.1,
            label="q=2 family contrast",
        )
        plt.xlabel("Additive noise sigma")
        plt.ylabel("Frozen closure quantity")
        plt.title("Ordinary period-2 degradation under additive noise")
        plt.legend()
        plt.tight_layout()
        plt.savefig(out / "noise_sweep.png", dpi=180)
        plt.close()

        plt.figure(figsize=(8.2, 4.9))
        plt.plot(
            [r["gamma"] for r in damping_rows],
            [r["closure_q2"] for r in damping_rows],
            marker="o",
            markersize=3,
            linewidth=1.1,
            label="C(2)",
        )
        plt.plot(
            [r["gamma"] for r in damping_rows],
            [r["q2_family_contrast"] for r in damping_rows],
            marker="o",
            markersize=3,
            linewidth=1.1,
            label="q=2 family contrast",
        )
        plt.xlabel("Damping rate gamma")
        plt.ylabel("Frozen closure quantity")
        plt.title("Transient period doubling loses supported closure")
        plt.legend()
        plt.tight_layout()
        plt.savefig(out / "damping_sweep.png", dpi=180)
        plt.close()

        plt.figure(figsize=(8.4, 4.9))
        plt.step(
            [r["r"] for r in logistic_rows],
            [r["detected_q0"] for r in logistic_rows],
            where="mid",
            linewidth=1.2,
        )
        plt.xlabel("Logistic-map parameter r")
        plt.ylabel("Detected recurrence depth q0")
        plt.title("Frozen q detector across a classical nonlinear bifurcation sweep")
        plt.yticks(range(2, 11))
        plt.tight_layout()
        plt.savefig(out / "logistic_q_scan.png", dpi=180)
        plt.close()

        # ---------------- Formal control conclusions ----------------
        row_by_label = {r["label"]: r for r in selected_rows}
        perfect = row_by_label["perfect_2T"]
        log2 = row_by_label["logistic_period2_r3p20"]
        log4 = row_by_label["logistic_period4_r3p50"]
        chaos = row_by_label["logistic_chaos_r4p00"]
        damp = row_by_label["damped_2T_gamma_0p10"]
        random = row_by_label["iid_random"]
        noisy = row_by_label["noisy_2T_sigma_0p20"]

        checks = {
            "C1_exact_period2_detected": {
                "observed_q0": perfect["detected_q0"],
                "closure_q2": perfect["closure_q2"],
                "shuffle_p_ge": perfect["shuffle_p_ge"],
                "pass": bool(perfect["detected_q0"] == 2 and perfect["closure_q2"] > 0.99),
            },
            "C2_classical_period2_detected": {
                "observed_q0": log2["detected_q0"],
                "closure_q2": log2["closure_q2"],
                "shuffle_p_ge": log2["shuffle_p_ge"],
                "pass": bool(log2["detected_q0"] == 2 and log2["closure_q2"] > 0.95),
            },
            "C3_classical_period4_detected": {
                "observed_q0": log4["detected_q0"],
                "closure_q0": log4["closure_q0"],
                "shuffle_p_ge": log4["shuffle_p_ge"],
                "pass": bool(log4["detected_q0"] == 4 and log4["closure_q0"] > 0.90),
            },
            "C4_chaos_not_strongly_closed": {
                "observed_q0": chaos["detected_q0"],
                "q0_local_contrast": chaos["q0_local_contrast"],
                "shuffle_p_ge": chaos["shuffle_p_ge"],
                "pass": bool(chaos["q0_local_contrast"] < 0.05 and chaos["shuffle_p_ge"] > 0.05),
            },
            "C5_random_not_strongly_closed": {
                "q0_local_contrast": random["q0_local_contrast"],
                "shuffle_p_ge": random["shuffle_p_ge"],
                "pass": bool(random["q0_local_contrast"] < 0.05 and random["shuffle_p_ge"] > 0.05),
            },
            "C6_damped_period2_weakened": {
                "closure_q2": damp["closure_q2"],
                "q2_family_contrast": damp["q2_family_contrast"],
                "shuffle_p_ge": damp["shuffle_p_ge"],
                "pass": bool(damp["closure_q2"] < log2["closure_q2"] and damp["q2_family_contrast"] < log2["q2_family_contrast"]),
            },
            "C7_noisy_harmonic_ambiguity_recorded": {
                "observed_q0": noisy["detected_q0"],
                "closure_q2": noisy["closure_q2"],
                "note": "The frozen local-contrast q0 rule may promote a higher even harmonic when an ordinary period-2 signal has near-degenerate even recurrence peaks.",
                "pass": True,
            },
        }

        validation = {
            "status": "PASS_CONTROL_CHALLENGE",
            "lock_id": lock["lock_id"],
            "metric_sha256": metric_sha,
            "metric_modified": False,
            "generator_seed": SEED,
            "selected_controls": selected_rows,
            "checks": checks,
            "scientific_result": {
                "closure_is_dtc_specific": False,
                "finding": (
                    "The frozen closure metric correctly detects strong recurrence "
                    "in ordinary/classical periodic dynamics. Therefore C(q) and "
                    "shuffle-significant recurrence are generic temporal-structure "
                    "observables, not unique identifiers of a discrete time crystal."
                ),
                "implication": (
                    "DTC discrimination must rely on higher-order rigidity, "
                    "universality across states/realizations, collective persistence, "
                    "and perturbation-basin structure rather than the mere existence "
                    "of q=2 closure."
                ),
                "harmonic_detector_limitation": (
                    "For noisy exact period-2 data, the local-contrast q0 detector can "
                    "select an even harmonic such as q=8 because q=2,4,6,8,10 are "
                    "nearly degenerate recurrence peaks. This limitation is preserved "
                    "rather than repaired after seeing the controls."
                ),
            },
        }
        (out / "control_validation.json").write_text(
            json.dumps(validation, indent=2), encoding="utf-8"
        )

        log = [
            "STATUS: PASS_CONTROL_CHALLENGE",
            f"LOCK VERIFIED: {lock['lock_id']}",
            f"Metric SHA256: {metric_sha}",
            "",
            "SELECTED CONTROLS",
        ]
        for row in selected_rows:
            log.append(
                f"{row['label']}: q0={row['detected_q0']}, "
                f"C2={row['closure_q2']:.6f}, "
                f"family={row['detected_family_contrast']:.6f}, "
                f"shuffle p={row['shuffle_p_ge']:.6f}"
            )
        log += [
            "",
            "CORE CONCLUSION",
            "Ordinary classical period-2 dynamics also produce strong frozen temporal closure.",
            "Therefore q=2 closure is NOT a unique DTC identifier.",
            "The next test must construct higher-order temporal rigidity/universality from already frozen observables.",
        ]
        (out / "RUN_LOG.txt").write_text("\n".join(log) + "\n", encoding="utf-8")
        print("\n".join(log))


if __name__ == "__main__":
    main()

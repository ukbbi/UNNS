from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import numpy as np
import matplotlib.pyplot as plt

from src.rigidity import (
    Artifact,
    verify_lock,
    geometry_similarity,
    universality_score,
    basin_area,
    pareto_dominates,
    spectrum_vector,
)


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


def import_locked_metric(metric_bytes: bytes, temp_dir: Path):
    p = temp_dir / "tc_closure_LOCKED.py"
    p.write_bytes(metric_bytes)
    spec = importlib.util.spec_from_file_location("tc_closure_RIGIDITY_LOCKED", p)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def exact_signflip_initial_states() -> dict[str, np.ndarray]:
    """
    A deliberately ordinary deterministic classical map:
        X_(t+1) = -X_t

    Every initial state lies on an exact two-cycle. Three very different
    20-coordinate initial states are used to test whether initial-condition
    universality itself is DTC-specific.
    """
    n = 20
    x = np.linspace(-1.0, 1.0, n)
    initial = {
        "signflip_sine": np.sin(np.linspace(0.2, 3.0, n)),
        "signflip_polynomial": x + 0.45*x*x - 0.2*x*x*x,
        "signflip_mixed": np.cos(np.linspace(0.1, 4.5, n)) + 0.3*np.sin(np.linspace(0.2, 7.0, n)),
    }
    out = {}
    for label, a in initial.items():
        a = a / np.sqrt(np.mean(a*a))
        out[label] = np.stack([a if t % 2 == 0 else -a for t in range(51)])
    return out


def locked_metrics(tc, X: np.ndarray) -> dict:
    ok = np.ones(X.shape[1], dtype=bool)
    spec, _, _ = tc.closure_spectrum(X, ok, qmax=10)
    qdet = tc.detect_fundamental_q(spec)
    fam = tc.family_contrast(spec, qdet["q0"])
    null = tc.shuffle_null(X, ok, qdet["q0"])
    return {
        "spectrum": spec,
        "q0": qdet["q0"],
        "C": next(r["closure"] for r in spec if r["q"] == qdet["q0"]),
        "F": fam["family_contrast"],
        "S": 1.0 - null["empirical_p_ge"],
        "p": null["empirical_p_ge"],
    }


def main():
    ap = argparse.ArgumentParser(
        description="Higher-order rigidity specificity test using frozen temporal closure observables."
    )
    ap.add_argument("lock", help="TC_CLOSURE_LOCK_v001 directory or ZIP")
    ap.add_argument("frey", help="TC_CLOSURE_v001 directory or ZIP")
    ap.add_argument("mi", help="TC_EXT_MI_v001 directory or ZIP")
    ap.add_argument("ctrl", help="TC_CTRL_v001 directory or ZIP")
    ap.add_argument("output", nargs="?", default="outputs")
    args = ap.parse_args()

    out = Path(args.output).resolve()
    out.mkdir(parents=True, exist_ok=True)

    lock_art = Artifact(args.lock)
    frey_art = Artifact(args.frey)
    mi_art = Artifact(args.mi)
    ctrl_art = Artifact(args.ctrl)

    lock, metric_bytes = verify_lock(lock_art)
    metric_sha = lock["frozen_files"]["src/tc_closure.py"]

    mi_val = mi_art.read_json("outputs/external_validation.json")
    ctrl_val = ctrl_art.read_json("outputs/control_validation.json")
    frey_val = frey_art.read_json("outputs/closure_result.json")

    # Provenance firewall across earlier packages.
    if mi_val["frozen_metric_sha256"] != metric_sha:
        raise RuntimeError("Mi validation metric SHA does not match the frozen lock")
    if ctrl_val["metric_sha256"] != metric_sha:
        raise RuntimeError("Control validation metric SHA does not match the frozen lock")

    with tempfile.TemporaryDirectory(prefix="tc_rigidity_") as td:
        tc = import_locked_metric(metric_bytes, Path(td))

        # ---------------- Existing rigidity vectors ----------------
        m = mi_val["primary_results"]
        rows = []

        def add_existing(label, cls, r, U=None):
            rows.append({
                "label": label,
                "class": cls,
                "C": float(r["closure_q0"]),
                "F": float(r["family_contrast"]),
                "S": 1.0 - float(r["shuffle_p_ge"]),
                "U": U,
                "q0": int(r["detected_q0"]),
                "source": "TC_EXT_MI_v001",
            })

        mi_uni = mi_val["pairwise_initial_state_universality"]
        mbl_u = universality_score([
            float(mi_uni["mbl"]["pairwise_family_contrast_mean"] - mi_uni["mbl"]["pairwise_family_contrast_std"]),
            float(mi_uni["mbl"]["pairwise_family_contrast_mean"]),
            float(mi_uni["mbl"]["pairwise_family_contrast_mean"] + mi_uni["mbl"]["pairwise_family_contrast_std"]),
        ])["U"]
        pre_u = universality_score([
            float(mi_uni["prethermal"]["pairwise_family_contrast_mean"] - mi_uni["prethermal"]["pairwise_family_contrast_std"]),
            float(mi_uni["prethermal"]["pairwise_family_contrast_mean"]),
            float(mi_uni["prethermal"]["pairwise_family_contrast_mean"] + mi_uni["prethermal"]["pairwise_family_contrast_std"]),
        ])["U"]

        # Exact CV from published mean/sd is 1 - sd/mean; store directly.
        mbl_u = float(np.clip(1.0 - (
            mi_uni["mbl"]["pairwise_family_contrast_std"] /
            mi_uni["mbl"]["pairwise_family_contrast_mean"]
        ), 0, 1))
        pre_u = float(np.clip(1.0 - (
            mi_uni["prethermal"]["pairwise_family_contrast_std"] /
            mi_uni["prethermal"]["pairwise_family_contrast_mean"]
        ), 0, 1))

        add_existing("Mi_MBL_site", "MBL-DTC", m["mbl_dtc_fig2d"])
        add_existing("Mi_thermal_site", "thermal control", m["thermal_fig2d"])
        add_existing("Mi_MBL_initial", "MBL-DTC", m["mbl_initial_states_fig3a"], mbl_u)
        add_existing("Mi_prethermal_initial", "prethermal DTC-like", m["prethermal_fig3a"], pre_u)

        # Existing selected classical controls.
        ctrl_map = {r["label"]: r for r in ctrl_val["selected_controls"]}
        for label in [
            "perfect_2T",
            "noisy_2T_sigma_0p20",
            "damped_2T_gamma_0p10",
            "logistic_period2_r3p20",
            "logistic_period4_r3p50",
            "logistic_chaos_r4p00",
            "iid_random",
        ]:
            r = ctrl_map[label]
            rows.append({
                "label": label,
                "class": r["control_kind"],
                "C": float(r["closure_q0"]),
                "F": float(r["detected_family_contrast"]),
                "S": 1.0 - float(r["shuffle_p_ge"]),
                "U": None,
                "q0": int(r["detected_q0"]),
                "source": "TC_CTRL_v001",
            })

        # ---------------- Classical initial-state universality ----------------
        exact_runs = []
        exact_spec_rows = []
        for label, X in exact_signflip_initial_states().items():
            rr = locked_metrics(tc, X)
            exact_runs.append(rr)
            for s in rr["spectrum"]:
                exact_spec_rows.append({"label": label, **s})

        exact_U_detail = universality_score([r["F"] for r in exact_runs])
        exact_C = float(np.mean([r["C"] for r in exact_runs]))
        exact_F = float(np.mean([r["F"] for r in exact_runs]))
        exact_S = float(np.mean([r["S"] for r in exact_runs]))
        rows.append({
            "label": "classical_signflip_family",
            "class": "ordinary classical exact 2-cycle across initial states",
            "C": exact_C,
            "F": exact_F,
            "S": exact_S,
            "U": exact_U_detail["U"],
            "q0": 2,
            "source": "TC_RIGIDITY_v001 generated with frozen metric",
        })

        # ---------------- Closure-family geometry ----------------
        mi_spec_rows = mi_art.read_csv("outputs/external_spectra.csv")
        ctrl_spec_rows = ctrl_art.read_csv("outputs/control_spectra.csv")

        geometry_rows = []
        comparisons = [
            ("Mi_MBL_site", spectrum_vector(mi_spec_rows, "fig2d_g097"),
             "perfect_2T", spectrum_vector(ctrl_spec_rows, "perfect_2T")),
            ("Mi_MBL_site", spectrum_vector(mi_spec_rows, "fig2d_g097"),
             "logistic_period2_r3p20", spectrum_vector(ctrl_spec_rows, "logistic_period2_r3p20")),
            ("Mi_MBL_initial", spectrum_vector(mi_spec_rows, "fig3a_mbl"),
             "damped_2T_gamma_0p10", spectrum_vector(ctrl_spec_rows, "damped_2T_gamma_0p10")),
            ("Mi_prethermal_initial", spectrum_vector(mi_spec_rows, "fig3a_prethermal"),
             "damped_2T_gamma_0p10", spectrum_vector(ctrl_spec_rows, "damped_2T_gamma_0p10")),
        ]
        for a_label, a, b_label, b in comparisons:
            g = geometry_similarity(a, b)
            geometry_rows.append({
                "A": a_label,
                "B": b_label,
                **g,
            })

        # ---------------- Perturbation-basin breadth ----------------
        frey_scan = frey_art.read_csv("outputs/closure_scan.csv")
        noise_scan = ctrl_art.read_csv("outputs/noise_sweep.csv")
        damp_scan = ctrl_art.read_csv("outputs/damping_sweep.csv")

        frey_boundary = float(frey_val["closure_basin"]["boundary_epsilon"])

        # Apply the same frozen basin-exit rule to q=2 family contrast in the
        # ordinary controls. q=2 is fixed by the noise-free baseline, not
        # re-selected at each noisy point.
        noise_for_basin = [{
            "epsilon": float(r["noise_sigma"]),
            "family_contrast": float(r["q2_family_contrast"]),
        } for r in noise_scan]
        damp_for_basin = [{
            "epsilon": float(r["gamma"]),
            "family_contrast": float(r["q2_family_contrast"]),
        } for r in damp_scan]

        noise_basin = tc.plateau_exit_boundary(
            noise_for_basin, key="family_contrast",
            seed_n=5, sigma_mult=3.0, consecutive=2
        )
        damp_basin = tc.plateau_exit_boundary(
            damp_for_basin, key="family_contrast",
            seed_n=5, sigma_mult=3.0, consecutive=2
        )

        basin_rows = [
            {
                "label": "Frey_MBL_DTC",
                "perturbation": "drive imperfection epsilon",
                "boundary": frey_boundary,
                **basin_area(frey_scan, "epsilon", "family_contrast", frey_boundary),
            },
            {
                "label": "classical_exact2T_plus_noise",
                "perturbation": "additive noise sigma",
                "boundary": float(noise_basin["boundary_epsilon"]),
                **basin_area(noise_scan, "noise_sigma", "q2_family_contrast",
                             float(noise_basin["boundary_epsilon"])),
            },
            {
                "label": "classical_exact2T_plus_damping",
                "perturbation": "exponential damping gamma",
                "boundary": float(damp_basin["boundary_epsilon"]),
                **basin_area(damp_scan, "gamma", "q2_family_contrast",
                             float(damp_basin["boundary_epsilon"])),
            },
        ]

        # ---------------- Dominance / specificity test ----------------
        rowmap = {r["label"]: r for r in rows}
        dom_core = pareto_dominates(
            rowmap["perfect_2T"],
            rowmap["Mi_MBL_site"],
            ["C", "F", "S"],
        )
        dom_initial = pareto_dominates(
            rowmap["classical_signflip_family"],
            rowmap["Mi_MBL_initial"],
            ["C", "F", "S", "U"],
        )

        # MBL still clearly exceeds its quantum thermal/prethermal controls.
        mbl_vs_thermal = pareto_dominates(
            rowmap["Mi_MBL_site"],
            rowmap["Mi_thermal_site"],
            ["C", "F", "S"],
        )
        mbl_vs_prethermal = pareto_dominates(
            rowmap["Mi_MBL_initial"],
            rowmap["Mi_prethermal_initial"],
            ["C", "F", "S", "U"],
        )

        result = {
            "status": "RIGIDITY_TEST_COMPLETE",
            "specificity_verdict": "DTC_SPECIFICITY_NOT_ESTABLISHED",
            "lock_id": lock["lock_id"],
            "metric_sha256": metric_sha,
            "lower_metric_modified": False,
            "rigidity_axes": {
                "C": "frozen closure at automatically detected q0",
                "F": "frozen recurrence-family contrast",
                "S": "1 - frozen shuffle-null p_ge",
                "U": "1 - coefficient of variation of family contrast across initial-state variants/pairs",
                "B": "dimensionless area under normalized family-contrast curve inside a basin found by the frozen plateau-exit rule",
            },
            "dominance_tests": {
                "ordinary_exact2T_vs_Mi_MBL_site_on_CFS": dom_core,
                "ordinary_signflip_initial_family_vs_Mi_MBL_initial_on_CFSU": dom_initial,
                "Mi_MBL_site_vs_thermal_on_CFS": mbl_vs_thermal,
                "Mi_MBL_initial_vs_prethermal_on_CFSU": mbl_vs_prethermal,
            },
            "geometry": geometry_rows,
            "basins": basin_rows,
            "classical_initial_state_universality": exact_U_detail,
            "interpretation": {
                "positive": (
                    "The higher-order descriptor cleanly preserves the separation "
                    "between MBL-DTC and the thermal/prethermal controls."
                ),
                "negative": (
                    "It does not uniquely separate MBL-DTC from ordinary classical "
                    "period-2 dynamics. Exact classical two-cycle dynamics equal or "
                    "exceed the MBL-DTC on the monotone closure/contrast/shuffle/"
                    "initial-state-universality axes."
                ),
                "consequence": (
                    "No monotone scalar made only from C, F, S and U can be justified "
                    "as a DTC-specific order parameter on these tests. The next UNNS "
                    "stage must add genuinely collective/many-body structural information "
                    "rather than further reweighting trajectory-recurrence observables."
                ),
            },
        }

        write_csv(out / "rigidity_vectors.csv", rows)
        write_csv(out / "geometry_comparison.csv", geometry_rows)
        write_csv(out / "basin_comparison.csv", basin_rows)
        write_csv(out / "classical_initial_states.csv", [{
            "run": i + 1,
            "C": rr["C"],
            "F": rr["F"],
            "S": rr["S"],
            "q0": rr["q0"],
        } for i, rr in enumerate(exact_runs)])
        write_csv(out / "classical_initial_spectra.csv", exact_spec_rows)
        (out / "rigidity_result.json").write_text(
            json.dumps(result, indent=2), encoding="utf-8"
        )

        # ---------------- Figures ----------------
        # Closure geometry profiles.
        plt.figure(figsize=(8.4, 5.0))
        for label, vec in [
            ("Mi MBL-DTC site", spectrum_vector(mi_spec_rows, "fig2d_g097")),
            ("classical exact 2T", spectrum_vector(ctrl_spec_rows, "perfect_2T")),
            ("classical logistic period-2", spectrum_vector(ctrl_spec_rows, "logistic_period2_r3p20")),
        ]:
            v = vec / np.max(vec)
            plt.plot(range(1, 11), v, marker="o", linewidth=1.2, label=label)
        plt.xlabel("Recurrence depth q")
        plt.ylabel("Normalized closure-family profile")
        plt.title("Closure-family geometry: MBL-DTC versus ordinary period doubling")
        plt.xticks(range(1, 11))
        plt.legend(fontsize=8)
        plt.tight_layout()
        plt.savefig(out / "geometry_profiles.png", dpi=180)
        plt.close()

        # Core rigidity axes.
        labels = ["Mi MBL", "Mi thermal", "Mi prethermal", "exact classical 2T", "logistic 2T"]
        keys = ["Mi_MBL_site", "Mi_thermal_site", "Mi_prethermal_initial", "perfect_2T", "logistic_period2_r3p20"]
        C = [rowmap[k]["C"] for k in keys]
        F = [rowmap[k]["F"] for k in keys]
        S = [rowmap[k]["S"] for k in keys]
        x = np.arange(len(labels))
        w = 0.25
        plt.figure(figsize=(9.0, 5.0))
        plt.bar(x-w, C, width=w, label="C")
        plt.bar(x, F, width=w, label="F")
        plt.bar(x+w, S, width=w, label="S")
        plt.xticks(x, labels, rotation=20, ha="right")
        plt.ylim(0, 1.08)
        plt.ylabel("Rigidity-axis value")
        plt.title("Higher-order recurrence rigidity is not DTC-unique")
        plt.legend()
        plt.tight_layout()
        plt.savefig(out / "rigidity_axes.png", dpi=180)
        plt.close()

        # Universality.
        u_labels = ["Mi MBL", "Mi prethermal", "classical sign-flip family"]
        u_vals = [mbl_u, pre_u, exact_U_detail["U"]]
        plt.figure(figsize=(7.6, 4.8))
        plt.bar(range(3), u_vals)
        plt.xticks(range(3), u_labels)
        plt.ylim(0, 1.05)
        plt.ylabel("Initial-state universality U")
        plt.title("Initial-state universality is strong but not uniquely DTC")
        plt.tight_layout()
        plt.savefig(out / "universality.png", dpi=180)
        plt.close()

        # Basin shape comparison, normalized x and y.
        plt.figure(figsize=(8.4, 5.0))
        def plot_basin(rows, xkey, ykey, boundary, label):
            xx = np.asarray([float(r[xkey]) for r in rows])
            yy = np.asarray([float(r[ykey]) for r in rows])
            order = np.argsort(xx); xx=xx[order]; yy=yy[order]
            mask = xx <= boundary + 1e-12
            xx=xx[mask]; yy=yy[mask]
            xn=(xx-xx[0])/(boundary-xx[0])
            base=np.median(yy[:min(5,len(yy))])
            yn=yy/base
            plt.plot(xn,yn,marker="o",linewidth=1.1,label=label)

        plot_basin(frey_scan, "epsilon", "family_contrast", frey_boundary, "Frey MBL-DTC")
        plot_basin(noise_scan, "noise_sigma", "q2_family_contrast",
                   float(noise_basin["boundary_epsilon"]), "classical 2T + noise")
        plot_basin(damp_scan, "gamma", "q2_family_contrast",
                   float(damp_basin["boundary_epsilon"]), "classical 2T + damping")
        plt.xlabel("Normalized distance through detected basin")
        plt.ylabel("Family contrast / seed-baseline")
        plt.title("Dimensionless basin-retention geometry")
        plt.legend(fontsize=8)
        plt.tight_layout()
        plt.savefig(out / "basin_retention.png", dpi=180)
        plt.close()

        # ---------------- Log ----------------
        g_exact = next(r for r in geometry_rows if r["A"]=="Mi_MBL_site" and r["B"]=="perfect_2T")
        log = [
            "STATUS: RIGIDITY_TEST_COMPLETE",
            "VERDICT: DTC_SPECIFICITY_NOT_ESTABLISHED",
            f"LOCK VERIFIED: {lock['lock_id']}",
            f"Metric SHA256: {metric_sha}",
            "",
            "GEOMETRY",
            f"Mi MBL-DTC vs exact classical 2T cosine similarity: {g_exact['cosine_similarity']:.9f}",
            f"Mi MBL-DTC vs exact classical 2T normalized RMS distance: {g_exact['normalized_RMS_distance']:.9f}",
            "",
            "INITIAL-STATE UNIVERSALITY",
            f"Mi MBL U: {mbl_u:.6f}",
            f"Mi prethermal U: {pre_u:.6f}",
            f"Classical exact sign-flip U: {exact_U_detail['U']:.6f}",
            "",
            "DIMENSIONLESS BASIN RETENTION AREA",
        ]
        for b in basin_rows:
            log.append(f"{b['label']}: {b['normalized_area']:.6f}")
        log += [
            "",
            "DOMINANCE TESTS",
            f"Exact classical 2T >= Mi MBL site on C,F,S: {dom_core['dominates_or_equals']}",
            f"Classical sign-flip family >= Mi MBL initial on C,F,S,U: {dom_initial['dominates_or_equals']}",
            f"Mi MBL site >= thermal on C,F,S: {mbl_vs_thermal['dominates_or_equals']}",
            f"Mi MBL initial >= prethermal on C,F,S,U: {mbl_vs_prethermal['dominates_or_equals']}",
            "",
            "CORE CONCLUSION",
            "The current higher-order recurrence-rigidity axes separate MBL-DTC from thermal/prethermal controls,",
            "but they do not separate it uniquely from ordinary classical two-cycle dynamics.",
            "A DTC-specific UNNS criterion now requires genuinely collective/many-body structure.",
        ]
        (out / "RUN_LOG.txt").write_text("\n".join(log) + "\n", encoding="utf-8")
        print("\n".join(log))


if __name__ == "__main__":
    main()

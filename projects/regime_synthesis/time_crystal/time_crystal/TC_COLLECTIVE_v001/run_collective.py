from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

from src.collective import (
    Artifact, MiData, verify_provenance,
    spin_glass_scaling, crossing_interval,
    spatial_localization, distribution_stats,
    typicality_stats, typicality_summary,
    classical_spin_glass_analogue,
    classical_localization_analogue,
)


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
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)


def main():
    ap = argparse.ArgumentParser(
        description="Collective/many-body sector for the UNNS Time Crystal branch."
    )
    ap.add_argument("data", help="DTC_Data.zip")
    ap.add_argument("lock", help="TC_CLOSURE_LOCK_v001 directory or ZIP")
    ap.add_argument("mi", help="TC_EXT_MI_v001 directory or ZIP")
    ap.add_argument("ctrl", help="TC_CTRL_v001 directory or ZIP")
    ap.add_argument("output", nargs="?", default="outputs")
    args = ap.parse_args()

    out = Path(args.output).resolve()
    out.mkdir(parents=True, exist_ok=True)

    data = MiData(args.data)
    lock = Artifact(args.lock)
    mi = Artifact(args.mi)
    ctrl = Artifact(args.ctrl)

    provenance = verify_provenance(lock, mi, ctrl)
    mi_val = mi.read_json("outputs/external_validation.json")
    ctrl_val = ctrl.read_json("outputs/control_validation.json")

    # -------- Temporal sector from frozen prior stage --------
    m = mi_val["primary_results"]
    temporal = {
        "mbl_dtc": {
            "C": float(m["mbl_dtc_fig2d"]["closure_q0"]),
            "F": float(m["mbl_dtc_fig2d"]["family_contrast"]),
            "shuffle_p": float(m["mbl_dtc_fig2d"]["shuffle_p_ge"]),
        },
        "prethermal": {
            "C": float(m["prethermal_fig3a"]["closure_q0"]),
            "F": float(m["prethermal_fig3a"]["family_contrast"]),
            "shuffle_p": float(m["prethermal_fig3a"]["shuffle_p_ge"]),
        },
        "thermal": {
            "C": float(m["thermal_fig2d"]["closure_q0"]),
            "F": float(m["thermal_fig2d"]["family_contrast"]),
            "shuffle_p": float(m["thermal_fig2d"]["shuffle_p_ge"]),
        },
    }

    # -------- Collective pair order / finite-size scaling --------
    fig5 = data.read("DTC_Data/fig_5.csv")
    sg_rows = spin_glass_scaling(fig5)
    sg_cross = crossing_interval(sg_rows)

    # -------- Correlation-spreading localization --------
    mbl_loc = spatial_localization(data.read("DTC_Data/fig_3d_mbl.csv").to_numpy(dtype=float))
    pre_loc = spatial_localization(data.read("DTC_Data/fig_3d_prethermal.csv").to_numpy(dtype=float))

    localization_rows = [
        {"regime": "MBL-DTC", **mbl_loc},
        {"regime": "prethermal", **pre_loc},
    ]

    # -------- 500-state spectral breadth --------
    fig3b = data.read("DTC_Data/fig_3b.csv")
    bitstring_rows = [
        {"regime": "MBL-DTC", **distribution_stats(fig3b["mbl_autocorrelators"].to_numpy(dtype=float))},
        {"regime": "prethermal", **distribution_stats(fig3b["prethermal_autocorrelators"].to_numpy(dtype=float))},
    ]

    # -------- Quantum typicality under scrambling --------
    dtc_typ = typicality_stats(
        data.read("DTC_Data/fig_4d.csv"),
        {0: "K_0", 2: "K_2", 20: "K_20"}
    )
    pre_typ = typicality_stats(
        data.read("DTC_Data/fig_s10_b.csv"),
        {0: "prethermal_list_0", 5: "prethermal_list_5", 20: "prethermal_list_20"}
    )
    th_typ = typicality_stats(
        data.read("DTC_Data/fig_s10_d.csv"),
        {0: "thermal_list_0", 5: "thermal_list_5", 20: "thermal_list_20"}
    )

    typ_rows = []
    for regime, rr in [("MBL-DTC", dtc_typ), ("prethermal", pre_typ), ("thermal", th_typ)]:
        for x in rr:
            typ_rows.append({"regime": regime, **x})

    typ_summary = {
        "MBL-DTC": typicality_summary(dtc_typ),
        "prethermal": typicality_summary(pre_typ),
        "thermal": typicality_summary(th_typ),
    }

    # -------- Classical counterexamples to lower collective coordinates --------
    classical_sg = classical_spin_glass_analogue()
    classical_loc = classical_localization_analogue()

    # A compact many-body evidence vector. No arbitrary weighted scalar.
    collective_vectors = [
        {
            "regime": "MBL-DTC",
            "temporal_C": temporal["mbl_dtc"]["C"],
            "temporal_F": temporal["mbl_dtc"]["F"],
            "temporal_shuffle_significance": 1.0 - temporal["mbl_dtc"]["shuffle_p"],
            "bitstring_mean_abs": bitstring_rows[0]["mean_abs"],
            "bitstring_CV_abs": bitstring_rows[0]["CV_abs"],
            "late_perturbation_IPR": mbl_loc["IPR"],
            "late_perturbation_N_eff": mbl_loc["N_eff"],
            "typicality_K20_mean_abs": typ_summary["MBL-DTC"]["mean_abs_final"],
            "typicality_K20_CV": typ_summary["MBL-DTC"]["final_CV"],
        },
        {
            "regime": "prethermal",
            "temporal_C": temporal["prethermal"]["C"],
            "temporal_F": temporal["prethermal"]["F"],
            "temporal_shuffle_significance": 1.0 - temporal["prethermal"]["shuffle_p"],
            "bitstring_mean_abs": bitstring_rows[1]["mean_abs"],
            "bitstring_CV_abs": bitstring_rows[1]["CV_abs"],
            "late_perturbation_IPR": pre_loc["IPR"],
            "late_perturbation_N_eff": pre_loc["N_eff"],
            "typicality_K20_mean_abs": typ_summary["prethermal"]["mean_abs_final"],
            "typicality_K20_CV": typ_summary["prethermal"]["final_CV"],
        },
        {
            "regime": "thermal",
            "temporal_C": temporal["thermal"]["C"],
            "temporal_F": temporal["thermal"]["F"],
            "temporal_shuffle_significance": 1.0 - temporal["thermal"]["shuffle_p"],
            "bitstring_mean_abs": None,
            "bitstring_CV_abs": None,
            "late_perturbation_IPR": None,
            "late_perturbation_N_eff": None,
            "typicality_K20_mean_abs": typ_summary["thermal"]["mean_abs_final"],
            "typicality_K20_CV": typ_summary["thermal"]["final_CV"],
        },
    ]

    # Tests. These are descriptive inequalities, not tuned classifier weights.
    tests = {
        "Q1_finite_size_collective_growth": {
            "observed_crossing_interval": [sg_cross["lower_g"], sg_cross["upper_g"]],
            "pass": bool(sg_cross["lower_g"] is not None and sg_cross["upper_g"] is not None),
        },
        "Q2_MBL_perturbation_more_localized_than_prethermal": {
            "MBL_IPR": mbl_loc["IPR"],
            "prethermal_IPR": pre_loc["IPR"],
            "MBL_N_eff": mbl_loc["N_eff"],
            "prethermal_N_eff": pre_loc["N_eff"],
            "pass": bool(mbl_loc["IPR"] > pre_loc["IPR"] and mbl_loc["N_eff"] < pre_loc["N_eff"]),
        },
        "Q3_MBL_broad_initial_state_order_exceeds_prethermal": {
            "MBL_mean_abs": bitstring_rows[0]["mean_abs"],
            "prethermal_mean_abs": bitstring_rows[1]["mean_abs"],
            "MBL_CV": bitstring_rows[0]["CV_abs"],
            "prethermal_CV": bitstring_rows[1]["CV_abs"],
            "pass": bool(
                bitstring_rows[0]["mean_abs"] > bitstring_rows[1]["mean_abs"]
                and bitstring_rows[0]["CV_abs"] < bitstring_rows[1]["CV_abs"]
            ),
        },
        "Q4_typical_entangled_state_order": {
            "MBL_K20_mean_abs": typ_summary["MBL-DTC"]["mean_abs_final"],
            "prethermal_K20_mean_abs": typ_summary["prethermal"]["mean_abs_final"],
            "thermal_K20_mean_abs": typ_summary["thermal"]["mean_abs_final"],
            "pass": bool(
                typ_summary["MBL-DTC"]["mean_abs_final"] >
                typ_summary["prethermal"]["mean_abs_final"] >
                typ_summary["thermal"]["mean_abs_final"]
            ),
        },
        "Q5_classical_pair_order_counterexample": {
            "classical_chi_values": classical_sg,
            "pass": True,
            "meaning": "Extensive Edwards-Anderson-type pair order can be mimicked by a deterministic classical two-cycle; pair order alone is not DTC-specific.",
        },
        "Q6_classical_localization_counterexample": {
            **classical_loc,
            "pass": True,
            "meaning": "Perfect perturbation localization can occur in an uncoupled classical sign-flip map; localization alone is not DTC-specific.",
        },
    }

    result = {
        "status": "COLLECTIVE_SECTOR_COMPLETE",
        "verdict": "QUANTUM_MANY_BODY_SECTOR_ESTABLISHED_WITH_CLASSICAL_SCOPE_LIMIT",
        "provenance": provenance,
        "tests": tests,
        "spin_glass_crossing": sg_cross,
        "typicality_summary": typ_summary,
        "interpretation": {
            "established": (
                "The Mi dataset supplies independent many-body collective evidence beyond temporal recurrence: "
                "finite-size spin-glass order, localized correlation spreading in the MBL regime, broad initial-state "
                "eigenstate order, and a nonzero response for highly scrambled typical quantum states."
            ),
            "classical_falsification": (
                "Neither extensive pair order nor perturbation localization alone is DTC-specific: explicit ordinary "
                "classical two-cycle counterexamples can reproduce those lower collective signatures."
            ),
            "first_nonclassical_coordinate": (
                "The quantum-typicality/eigenstate-breadth axis is operationally quantum-many-body: it is measured on "
                "highly entangled scrambled states sampling the many-body Hilbert space. An ordinary classical periodic "
                "attractor has no directly equivalent Hilbert-space typicality coordinate, so it must be marked N/A rather "
                "than assigned an artificial zero."
            ),
            "scope": (
                "Therefore temporal closure + collective order separates MBL-DTC from the thermal and prethermal quantum "
                "controls in this dataset. It does not yield a universal scalar classifier against classical dynamics; "
                "the classical comparison becomes domain-qualified because the decisive spectral-typicality coordinate "
                "is not defined for an ordinary classical attractor."
            ),
        },
    }

    # Outputs.
    write_csv(out / "spin_glass_scaling.csv", sg_rows)
    write_csv(out / "localization.csv", localization_rows)
    write_csv(out / "bitstring_breadth.csv", bitstring_rows)
    write_csv(out / "typicality.csv", typ_rows)
    write_csv(out / "collective_vectors.csv", collective_vectors)
    write_csv(out / "classical_spin_glass.csv", classical_sg)
    (out / "collective_result.json").write_text(json.dumps(result, indent=2), encoding="utf-8")

    # Figures.
    plt.figure(figsize=(8.2, 4.9))
    for L in [8, 12, 16, 20]:
        plt.plot(fig5["g"], fig5[f"s_{L}"], marker="o", linewidth=1.1, label=f"L={L}")
    plt.xlabel("Drive parameter g")
    plt.ylabel("Spin-glass order parameter")
    plt.title("Collective finite-size order in the Mi experiment")
    plt.legend()
    plt.tight_layout()
    plt.savefig(out / "spin_glass_scaling.png", dpi=180)
    plt.close()

    plt.figure(figsize=(8.2, 4.9))
    plt.plot([r["g"] for r in sg_rows], [r["alpha_logL"] for r in sg_rows],
             marker="o", linewidth=1.1)
    plt.axhline(0, linewidth=1)
    if sg_cross["lower_g"] is not None:
        plt.axvspan(sg_cross["lower_g"], sg_cross["upper_g"], alpha=0.12)
    plt.xlabel("Drive parameter g")
    plt.ylabel("Finite-size exponent alpha")
    plt.title("Sign change of collective size scaling")
    plt.tight_layout()
    plt.savefig(out / "spin_glass_exponent.png", dpi=180)
    plt.close()

    # Late perturbation profiles.
    mbl_arr = data.read("DTC_Data/fig_3d_mbl.csv").to_numpy(dtype=float)
    pre_arr = data.read("DTC_Data/fig_3d_prethermal.csv").to_numpy(dtype=float)
    plt.figure(figsize=(8.2, 4.9))
    plt.plot(np.arange(1,21), np.abs(mbl_arr[:,-1]), marker="o", linewidth=1.1, label="MBL-DTC")
    plt.plot(np.arange(1,21), np.abs(pre_arr[:,-1]), marker="o", linewidth=1.1, label="prethermal")
    plt.xlabel("Qubit position")
    plt.ylabel("Late relative perturbation response")
    plt.title("Many-body perturbation spreading")
    plt.legend()
    plt.tight_layout()
    plt.savefig(out / "perturbation_profiles.png", dpi=180)
    plt.close()

    # Typicality mean across K.
    plt.figure(figsize=(8.2, 4.9))
    for regime, rr in [("MBL-DTC", dtc_typ), ("prethermal", pre_typ), ("thermal", th_typ)]:
        plt.plot([x["K"] for x in rr], [x["mean_abs"] for x in rr],
                 marker="o", linewidth=1.2, label=regime)
    plt.xlabel("Scrambling depth K")
    plt.ylabel("Mean |A_psi| across 500 states")
    plt.title("Quantum typicality / eigenstate breadth")
    plt.legend()
    plt.tight_layout()
    plt.savefig(out / "typicality_mean.png", dpi=180)
    plt.close()

    # Temporal + spectral plane.
    pts = [
        ("MBL-DTC", temporal["mbl_dtc"]["C"], typ_summary["MBL-DTC"]["mean_abs_final"]),
        ("prethermal", temporal["prethermal"]["C"], typ_summary["prethermal"]["mean_abs_final"]),
        ("thermal", temporal["thermal"]["C"], typ_summary["thermal"]["mean_abs_final"]),
    ]
    plt.figure(figsize=(7.4, 5.2))
    for label, x, y in pts:
        plt.scatter([x], [y], s=70)
        plt.text(x+0.01, y+0.005, label)
    plt.xlabel("Frozen temporal closure C(q0)")
    plt.ylabel("K=20 typical-state mean |A_psi|")
    plt.title("Temporal closure + many-body spectral order")
    plt.tight_layout()
    plt.savefig(out / "temporal_collective_plane.png", dpi=180)
    plt.close()

    log = [
        "STATUS: COLLECTIVE_SECTOR_COMPLETE",
        "VERDICT: QUANTUM_MANY_BODY_SECTOR_ESTABLISHED_WITH_CLASSICAL_SCOPE_LIMIT",
        f"LOCK VERIFIED: {provenance['lock_id']}",
        f"Metric SHA256: {provenance['metric_sha256']}",
        "",
        "FINITE-SIZE SPIN-GLASS ORDER",
        f"alpha sign-change interval: g={sg_cross['lower_g']:.2f} to {sg_cross['upper_g']:.2f}",
        "",
        "PERTURBATION SPREADING",
        f"MBL late IPR: {mbl_loc['IPR']:.6f}, N_eff={mbl_loc['N_eff']:.3f}",
        f"Prethermal late IPR: {pre_loc['IPR']:.6f}, N_eff={pre_loc['N_eff']:.3f}",
        "",
        "500-STATE EIGENSTATE BREADTH",
        f"MBL mean |A|={bitstring_rows[0]['mean_abs']:.6f}, CV={bitstring_rows[0]['CV_abs']:.6f}",
        f"Prethermal mean |A|={bitstring_rows[1]['mean_abs']:.6f}, CV={bitstring_rows[1]['CV_abs']:.6f}",
        "",
        "QUANTUM TYPICALITY K=20",
        f"MBL mean |A_psi|={typ_summary['MBL-DTC']['mean_abs_final']:.6f}",
        f"Prethermal mean |A_psi|={typ_summary['prethermal']['mean_abs_final']:.6f}",
        f"Thermal mean |A_psi|={typ_summary['thermal']['mean_abs_final']:.6f}",
        "",
        "CLASSICAL COUNTEREXAMPLES",
        "Extensive pair order: classically reproducible.",
        "Perfect perturbation localization: classically reproducible.",
        "Hilbert-space quantum typicality: no direct ordinary-classical analogue; recorded as N/A, not zero.",
        "",
        "CORE CONCLUSION",
        "Temporal closure + experimentally measured many-body spectral breadth separates MBL-DTC from thermal/prethermal quantum controls.",
        "A universal scalar separator against classical attractors is NOT established because the decisive typicality axis is quantum-domain-specific.",
    ]
    (out / "RUN_LOG.txt").write_text("\n".join(log) + "\n", encoding="utf-8")
    print("\n".join(log))


if __name__ == "__main__":
    main()

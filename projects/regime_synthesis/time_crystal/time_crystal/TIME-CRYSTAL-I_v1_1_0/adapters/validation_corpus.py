from __future__ import annotations

from .artifact import Artifact


def sector(status: str, **evidence):
    return {"status": status, **evidence}


def build_validation_corpus(
    phys_path,
    closure_path,
    mi_path,
    ctrl_path,
    rigidity_path,
    collective_path,
):
    phys = Artifact(phys_path)
    closure = Artifact(closure_path)
    mi = Artifact(mi_path)
    ctrl = Artifact(ctrl_path)
    rigidity = Artifact(rigidity_path)
    collective = Artifact(collective_path)

    phys_v = phys.read_json("outputs/physics_validation.json")
    clos_v = closure.read_json("outputs/closure_result.json")
    clos_scan = closure.read_csv("outputs/closure_scan.csv")
    mi_v = mi.read_json("outputs/external_validation.json")
    ctrl_v = ctrl.read_json("outputs/control_validation.json")
    rig_v = rigidity.read_json("outputs/rigidity_result.json")
    coll_v = collective.read_json("outputs/collective_result.json")

    # Frozen dependency cross-checks.
    metric_sha = clos_v["firewall"].get("physics_gate_status_checked")
    lock_sha = mi_v["frozen_metric_sha256"]
    if ctrl_v["metric_sha256"] != lock_sha:
        raise RuntimeError("Control and Mi stages do not share the frozen closure metric")
    if rig_v["metric_sha256"] != lock_sha:
        raise RuntimeError("Rigidity stage does not share the frozen closure metric")
    if coll_v["provenance"]["metric_sha256"] != lock_sha:
        raise RuntimeError("Collective stage does not share the frozen closure metric")

    # Frey representative low-perturbation point.
    frey_eps05 = next(r for r in clos_scan if abs(float(r["epsilon"]) - 0.05) < 1e-12)
    frey = {
        "id": "frey57_mbl_dtc",
        "label": "Frey–Rachel 57-qubit DTC",
        "domain": "quantum_many_body",
        "expected_physics_class": "MBL-DTC",
        "sectors": {
            "temporal": sector(
                "SUPPORTED",
                q0=int(clos_v["fundamental_recurrence"]["q0"]),
                closure=float(clos_v["shuffle_null"]["observed"]),
                family_contrast=float(frey_eps05["family_contrast"]),
                shuffle_p=float(clos_v["shuffle_null"]["empirical_p_ge"]),
                basis="frozen TC_CLOSURE_v001 low-perturbation recurrence",
            ),
            "rigidity": sector(
                "SUPPORTED",
                basin_exit=float(clos_v["closure_basin"]["boundary_epsilon"]),
                physical_transition_reference=float(
                    closure.read_json("outputs/posthoc_comparison.json")["physical_reference_epsilon_c"]
                ),
                basis="closure basin plus independent physics gate",
            ),
            "collective": sector(
                "NOT_TESTED",
                basis="the Frey branch was not processed through TC_COLLECTIVE_v001",
            ),
            "spectral": sector(
                "NOT_TESTED",
                basis="no frozen many-body typicality/eigenstate-breadth sector in this branch",
            ),
        },
        "provenance": [
            "TC_PHYS_v001",
            "TC_CLOSURE_v001",
        ],
    }

    p = mi_v["primary_results"]
    u = mi_v["pairwise_initial_state_universality"]
    tests = coll_v["tests"]
    typicality = coll_v["typicality_summary"]

    mi_mbl = {
        "id": "mi20_mbl_dtc",
        "label": "Mi et al. 20-qubit MBL-DTC",
        "domain": "quantum_many_body",
        "expected_physics_class": "MBL-DTC",
        "sectors": {
            "temporal": sector(
                "SUPPORTED",
                q0=int(p["mbl_dtc_fig2d"]["detected_q0"]),
                closure=float(p["mbl_dtc_fig2d"]["closure_q0"]),
                family_contrast=float(p["mbl_dtc_fig2d"]["family_contrast"]),
                shuffle_p=float(p["mbl_dtc_fig2d"]["shuffle_p_ge"]),
                basis="independent frozen-metric external validation",
            ),
            "rigidity": sector(
                "SUPPORTED",
                initial_state_pairs_significant=int(
                    u["mbl"]["significant_shuffle_pairs_p_lt_0_05"]
                ),
                initial_state_pair_count=int(u["mbl"]["pair_count"]),
                universality=float(
                    1.0 - u["mbl"]["pairwise_family_contrast_std"]
                    / u["mbl"]["pairwise_family_contrast_mean"]
                ),
                basis="3/3 initial-state pair stability plus frozen rigidity analysis",
            ),
            "collective": sector(
                "SUPPORTED",
                finite_size_collective_growth=bool(tests["Q1_finite_size_collective_growth"]["pass"]),
                localized_spreading=bool(
                    tests["Q2_MBL_perturbation_more_localized_than_prethermal"]["pass"]
                ),
                broad_initial_state_order=bool(
                    tests["Q3_MBL_broad_initial_state_order_exceeds_prethermal"]["pass"]
                ),
                basis="finite-size spin-glass order + perturbation localization + 500-state breadth",
            ),
            "spectral": sector(
                "SUPPORTED",
                typicality_K20_mean_abs=float(
                    typicality["MBL-DTC"]["mean_abs_final"]
                ),
                typicality_retention=float(
                    typicality["MBL-DTC"]["mean_retention"]
                ),
                basis="highly scrambled 500-state quantum-typicality sector",
            ),
        },
        "provenance": [
            "TC_EXT_MI_v001",
            "TC_RIGIDITY_v001",
            "TC_COLLECTIVE_v001",
        ],
    }

    mi_pre = {
        "id": "mi20_prethermal",
        "label": "Mi et al. prethermal DTC-like control",
        "domain": "quantum_many_body",
        "expected_physics_class": "prethermal DTC-like",
        "sectors": {
            "temporal": sector(
                "SUPPORTED",
                q0=int(p["prethermal_fig3a"]["detected_q0"]),
                closure=float(p["prethermal_fig3a"]["closure_q0"]),
                family_contrast=float(p["prethermal_fig3a"]["family_contrast"]),
                shuffle_p=float(p["prethermal_fig3a"]["shuffle_p_ge"]),
                basis="DTC-like q=2 recurrence exists but is weaker and less universal",
            ),
            "rigidity": sector(
                "NOT_SUPPORTED",
                initial_state_pairs_significant=int(
                    u["prethermal"]["significant_shuffle_pairs_p_lt_0_05"]
                ),
                initial_state_pair_count=int(u["prethermal"]["pair_count"]),
                universality=float(
                    1.0 - u["prethermal"]["pairwise_family_contrast_std"]
                    / u["prethermal"]["pairwise_family_contrast_mean"]
                ),
                basis="only 1/3 initial-state pairs significant in frozen external validation",
            ),
            "collective": sector(
                "PARTIAL",
                localized_spreading=False,
                broad_initial_state_order=False,
                basis="many-body dynamics present, but MBL collective signatures fail against MBL-DTC",
            ),
            "spectral": sector(
                "SUPPORTED",
                typicality_K20_mean_abs=float(
                    typicality["prethermal"]["mean_abs_final"]
                ),
                typicality_retention=float(
                    typicality["prethermal"]["mean_retention"]
                ),
                basis="nonzero typical-state response, but not sufficient to overcome failed rigidity/collective gates",
            ),
        },
        "provenance": [
            "TC_EXT_MI_v001",
            "TC_RIGIDITY_v001",
            "TC_COLLECTIVE_v001",
        ],
    }

    mi_thermal = {
        "id": "mi20_thermal",
        "label": "Mi et al. thermal control",
        "domain": "quantum_many_body",
        "expected_physics_class": "thermal",
        "sectors": {
            "temporal": sector(
                "NOT_SUPPORTED",
                q0=int(p["thermal_fig2d"]["detected_q0"]),
                closure=float(p["thermal_fig2d"]["closure_q0"]),
                family_contrast=float(p["thermal_fig2d"]["family_contrast"]),
                shuffle_p=float(p["thermal_fig2d"]["shuffle_p_ge"]),
                basis="transient q=2 signature is not temporally significant under frozen shuffle null",
            ),
            "rigidity": sector("NOT_SUPPORTED", basis="thermal depolarization"),
            "collective": sector("NOT_SUPPORTED", basis="thermal quantum control"),
            "spectral": sector(
                "NOT_SUPPORTED",
                typicality_K20_mean_abs=float(
                    typicality["thermal"]["mean_abs_final"]
                ),
                typicality_retention=float(
                    typicality["thermal"]["mean_retention"]
                ),
                basis="typical-state response collapses at high scrambling depth",
            ),
        },
        "provenance": [
            "TC_EXT_MI_v001",
            "TC_COLLECTIVE_v001",
        ],
    }

    cmap = {r["label"]: r for r in ctrl_v["selected_controls"]}

    exact = cmap["perfect_2T"]
    exact_classical = {
        "id": "classical_exact_2T",
        "label": "Exact classical two-cycle",
        "domain": "classical",
        "expected_physics_class": "ordinary period-2",
        "sectors": {
            "temporal": sector(
                "SUPPORTED",
                q0=int(exact["detected_q0"]),
                closure=float(exact["closure_q0"]),
                family_contrast=float(exact["detected_family_contrast"]),
                shuffle_p=float(exact["shuffle_p_ge"]),
                basis="frozen classical control challenge",
            ),
            "rigidity": sector(
                "SUPPORTED",
                universality=float(
                    rig_v["classical_initial_state_universality"]["U"]
                ),
                basis="exact sign-flip family plus broad classical noise basin",
            ),
            "collective": sector(
                "N/A",
                basis="quantum collective gate is not imposed on a classical-domain record",
            ),
            "spectral": sector(
                "N/A",
                basis="Hilbert-space quantum typicality has no direct ordinary-classical analogue",
            ),
        },
        "provenance": ["TC_CTRL_v001", "TC_RIGIDITY_v001"],
    }

    logistic2 = cmap["logistic_period2_r3p20"]
    classical_log2 = {
        "id": "classical_logistic_2T",
        "label": "Classical logistic-map period-2 attractor",
        "domain": "classical",
        "expected_physics_class": "ordinary nonlinear period-2",
        "sectors": {
            "temporal": sector(
                "SUPPORTED",
                q0=int(logistic2["detected_q0"]),
                closure=float(logistic2["closure_q0"]),
                family_contrast=float(logistic2["detected_family_contrast"]),
                shuffle_p=float(logistic2["shuffle_p_ge"]),
                basis="frozen ordinary-period-doubling challenge",
            ),
            "rigidity": sector(
                "NOT_TESTED",
                basis="no independent multi-initial-state/basin chamber test frozen for this specific logistic record",
            ),
            "collective": sector("N/A", basis="classical domain"),
            "spectral": sector("N/A", basis="classical domain"),
        },
        "provenance": ["TC_CTRL_v001"],
    }

    logistic4 = cmap["logistic_period4_r3p50"]
    classical_log4 = {
        "id": "classical_logistic_4T",
        "label": "Classical logistic-map period-4 attractor",
        "domain": "classical",
        "expected_physics_class": "ordinary nonlinear period-4",
        "sectors": {
            "temporal": sector(
                "SUPPORTED",
                q0=int(logistic4["detected_q0"]),
                closure=float(logistic4["closure_q0"]),
                family_contrast=float(logistic4["detected_family_contrast"]),
                shuffle_p=float(logistic4["shuffle_p_ge"]),
                basis="q detector generalization sanity control",
            ),
            "rigidity": sector("NOT_TESTED", basis="not required for recurrence-depth sanity control"),
            "collective": sector("N/A", basis="classical domain"),
            "spectral": sector("N/A", basis="classical domain"),
        },
        "provenance": ["TC_CTRL_v001"],
    }

    damped = cmap["damped_2T_gamma_0p10"]
    classical_damped = {
        "id": "classical_damped_2T",
        "label": "Damped transient period-2 control",
        "domain": "classical",
        "expected_physics_class": "transient period-2",
        "sectors": {
            "temporal": sector(
                "SUPPORTED",
                q0=int(damped["detected_q0"]),
                closure=float(damped["closure_q0"]),
                family_contrast=float(damped["detected_family_contrast"]),
                shuffle_p=float(damped["shuffle_p_ge"]),
                basis="period-2 recurrence remains visible but supported closure is weak",
            ),
            "rigidity": sector("NOT_SUPPORTED", basis="support collapses under damping"),
            "collective": sector("N/A", basis="classical domain"),
            "spectral": sector("N/A", basis="classical domain"),
        },
        "provenance": ["TC_CTRL_v001"],
    }

    chaos = cmap["logistic_chaos_r4p00"]
    classical_chaos = {
        "id": "classical_chaos",
        "label": "Classical logistic-map chaotic control",
        "domain": "classical",
        "expected_physics_class": "chaotic",
        "sectors": {
            "temporal": sector(
                "NOT_SUPPORTED",
                q0=int(chaos["detected_q0"]),
                closure=float(chaos["closure_q0"]),
                family_contrast=float(chaos["detected_family_contrast"]),
                shuffle_p=float(chaos["shuffle_p_ge"]),
                basis="tiny closure contrast and null-consistent temporal ordering",
            ),
            "rigidity": sector("NOT_SUPPORTED", basis="chaotic control"),
            "collective": sector("N/A", basis="classical domain"),
            "spectral": sector("N/A", basis="classical domain"),
        },
        "provenance": ["TC_CTRL_v001"],
    }

    random = cmap["iid_random"]
    classical_random = {
        "id": "iid_random",
        "label": "IID random negative control",
        "domain": "generic",
        "expected_physics_class": "random",
        "sectors": {
            "temporal": sector(
                "NOT_SUPPORTED",
                q0=int(random["detected_q0"]),
                closure=float(random["closure_q0"]),
                family_contrast=float(random["detected_family_contrast"]),
                shuffle_p=float(random["shuffle_p_ge"]),
                basis="null-consistent random negative control",
            ),
            "rigidity": sector("NOT_SUPPORTED", basis="random control"),
            "collective": sector("N/A", basis="not applicable"),
            "spectral": sector("N/A", basis="not applicable"),
        },
        "provenance": ["TC_CTRL_v001"],
    }

    return [
        frey,
        mi_mbl,
        mi_pre,
        mi_thermal,
        exact_classical,
        classical_log2,
        classical_log4,
        classical_damped,
        classical_chaos,
        classical_random,
    ], {
        "frozen_closure_metric_sha256": lock_sha,
        "physics_gate_status": phys_v["status"],
        "rigidity_verdict": rig_v["specificity_verdict"],
        "collective_verdict": coll_v["verdict"],
    }

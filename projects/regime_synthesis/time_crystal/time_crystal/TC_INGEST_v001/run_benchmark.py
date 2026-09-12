from __future__ import annotations
import argparse, csv, json
from pathlib import Path
from statistics import median
import numpy as np
import matplotlib.pyplot as plt
from tc_ingest import (
    parse_meta, load_dat, target_autocorrelation, reference_autocorrelation,
    half_frequency_per_qubit, staggered, state_distance
)

SPECIAL_MARKERS = ("POL", "NEEL", "NoDIS", "RND_RefDis", "PolND_RefDis")


def row_for(path: Path):
    meta = parse_meta(path)
    arr = load_dat(path)
    ac = target_autocorrelation(arr)
    ref = reference_autocorrelation(arr)
    hi = half_frequency_per_qubit(ac)
    avg = ac.mean(axis=1)
    st = staggered(ac).mean(axis=1)
    return {
        **meta.to_dict(),
        "hf_mean": float(np.mean(hi)),
        "hf_var": float(np.var(hi)),
        "staggered_early_1_10": float(np.mean(st[1:11])),
        "staggered_late_20_40": float(np.mean(st[20:41])),
        "reference_staggered_late_20_40": float(np.mean(staggered(ref).mean(axis=1)[20:41])),
        "D1_raw": state_distance(ac, 1),
        "D2_raw": state_distance(ac, 2),
        "D2_over_D1_raw": state_distance(ac, 2) / max(state_distance(ac, 1), 1e-12),
        "trace": avg,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("data_dir")
    ap.add_argument("output_dir")
    args = ap.parse_args()
    data_dir = Path(args.data_dir); out = Path(args.output_dir); out.mkdir(parents=True, exist_ok=True)

    rows = [row_for(p) for p in sorted(data_dir.glob("*.dat"))]
    scalar_fields = [k for k in rows[0].keys() if k != "trace"]
    with open(out / "benchmark.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=scalar_fields); w.writeheader()
        for r in rows: w.writerow({k:r[k] for k in scalar_fields})

    regular = [r for r in rows if not any(m in r["filename"] for m in SPECIAL_MARKERS)]
    grouped = {}
    for r in regular: grouped.setdefault(r["epsilon"], []).append(r)
    phase = []
    for eps in sorted(grouped):
        g=grouped[eps]
        phase.append({
            "epsilon": eps,
            "n_files": len(g),
            "hf_mean_median": median([x["hf_mean"] for x in g]),
            "hf_var_median": median([x["hf_var"] for x in g]),
            "staggered_late_median": median([x["staggered_late_20_40"] for x in g]),
            "D2_over_D1_median": median([x["D2_over_D1_raw"] for x in g]),
        })
    with open(out / "phase_scan.csv", "w", newline="", encoding="utf-8") as f:
        w=csv.DictWriter(f, fieldnames=list(phase[0].keys())); w.writeheader(); w.writerows(phase)

    def choose(exact_name=None, eps=None, contains=()):
        if exact_name:
            for r in rows:
                if r["filename"]==exact_name: return r
        cand=[r for r in rows if (eps is None or abs(r["epsilon"]-eps)<1e-12) and all(x in r["filename"] for x in contains)]
        return cand[0] if cand else None

    dtc = choose("NewFloq_REF_Bro57_Eps005_T50_5IT_16Sep.dat")
    thermal = choose("NewFloq_REF_Man57_Eps05_T50_5IT_5Jul.dat")
    pol = choose("NewFloq_REF_Bro57_Eps005_T50_5IT_30Aug_POL.dat")
    nodis = choose("NewFloq_REF_Bro57_Eps005_T50_5IT_30Aug_NoDIS.dat")

    reps=[("DTC_proxy_eps005",dtc),("thermal_proxy_eps05",thermal),("polarized_eps005",pol),("no_disorder_eps005",nodis)]
    with open(out / "representative_traces.csv", "w", newline="", encoding="utf-8") as f:
        w=csv.writer(f); w.writerow(["timestep"]+[x[0] for x in reps if x[1]])
        for t in range(51):
            w.writerow([t]+[float(r["trace"][t]) for _,r in reps if r])

    # Physics sanity gate: only raw/unmitigated distinction, not an exact reproduction of published Fig. 3.
    gate={"status":"INCOMPLETE","checks":{},"scope":"raw binary-data sanity checks; no claim of exact paper error-mitigation reproduction"}
    if dtc and thermal:
        ratio=dtc["hf_mean"]/max(thermal["hf_mean"],1e-12)
        gate["checks"]["DTC_vs_thermal_half_frequency_ratio"]={"value":ratio,"pass":bool(ratio>5.0)}
        gate["checks"]["DTC_late_staggered_gt_thermal"]={
            "dtc":dtc["staggered_late_20_40"],"thermal":thermal["staggered_late_20_40"],
            "pass":bool(dtc["staggered_late_20_40"] > thermal["staggered_late_20_40"] + 0.03)
        }
    if all(v.get("pass",False) for v in gate["checks"].values()) and gate["checks"]:
        gate["status"]="PASS_RAW_SANITY"
    (out/"physics_gate.json").write_text(json.dumps(gate,indent=2),encoding="utf-8")

    # Representative trace figure.
    plt.figure(figsize=(8,4.8))
    for label,r in reps[:2]:
        if r: plt.plot(np.arange(51), r["trace"], marker='o', markersize=2, linewidth=1, label=label)
    plt.axhline(0, linewidth=0.8)
    plt.xlabel("Floquet timestep")
    plt.ylabel("Mean local autocorrelation (raw)")
    plt.title("Raw DTC-like vs thermal representative traces")
    plt.legend()
    plt.tight_layout(); plt.savefig(out/"fig2_proxy.png",dpi=160); plt.close()

    # Phase scan raw proxy figure.
    plt.figure(figsize=(7.5,4.6))
    plt.plot([x["epsilon"] for x in phase],[x["hf_mean_median"] for x in phase],marker='o',markersize=3)
    plt.xlabel("epsilon")
    plt.ylabel("Median raw half-frequency amplitude")
    plt.title("Raw epsilon scan (not paper-mitigated)")
    plt.tight_layout(); plt.savefig(out/"phase_proxy.png",dpi=160); plt.close()

    print(json.dumps(gate,indent=2))

if __name__ == "__main__": main()

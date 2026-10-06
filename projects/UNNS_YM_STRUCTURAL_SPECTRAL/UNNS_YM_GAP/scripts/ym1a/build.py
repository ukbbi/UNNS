from pathlib import Path
import csv, json, math

ROOT = Path(__file__).resolve().parents[2]
MASS = ROOT / "data" / "derived" / "at20" / "at_mass.csv"
LAT = ROOT / "data" / "derived" / "at20" / "at_lat.csv"
CONT = ROOT / "data" / "derived" / "at20" / "at_cont.csv"
OUT = ROOT / "ladders"
RUN = ROOT / "output" / "ym1a_build.json"

# Frozen coordinate order. These are the only channel/state pairs present at all 8 beta values.
COORDS = [
    ("c1", "A1++", 0, "A1++ ground (0++ mass-gap state)"),
    ("c2", "A1++", 1, "A1++ first excitation"),
    ("c3", "E++", 0, "E++ ground"),
    ("c4", "T2++", 0, "T2++ ground"),
    ("c5", "A1-+", 0, "A1-+ ground (0-+ candidate)"),
]

def read_csv(path):
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))

def write_csv(path, rows, fields):
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)

def f(x):
    return float(x)

def ratio_err_indep(m, dm, s, ds):
    # Diagnostic only. m and s arise from the same ensembles and may be correlated.
    # No covariance was supplied in the extracted corpus.
    return math.sqrt((dm/s)**2 + ((m*ds)/(s*s))**2)

def main():
    mass = read_csv(MASS)
    lat = read_csv(LAT)
    cont = read_csv(CONT)

    lat_by_e = {r["ensemble_id"]: r for r in lat}
    mass_by_key = {
        (r["ensemble_id"], r["channel"], int(r["state_index"])): r
        for r in mass
    }

    # Refinement order is increasing beta / decreasing a*sqrt(sigma).
    levels = sorted(lat, key=lambda r: float(r["beta"]))

    long_rows = []
    wide_rows = []
    gap_rows = []

    for i, lr in enumerate(levels, start=1):
        e = lr["ensemble_id"]
        s = f(lr["a_sqrt_sigma"])
        ds = f(lr["a_sqrt_sigma_err"])
        wide = {
            "level": i,
            "ensemble_id": e,
            "beta": lr["beta"],
            "lattice": lr["lattice"],
            "a_sqrt_sigma": lr["a_sqrt_sigma"],
            "a_sqrt_sigma_err": lr["a_sqrt_sigma_err"],
            "a2_sigma": f"{s*s:.12g}",
        }

        coord1 = None
        for cid, ch, si, label in COORDS:
            mr = mass_by_key[(e, ch, si)]
            m = f(mr["value"])
            dm = f(mr["uncertainty"])
            ratio = m / s
            re = ratio_err_indep(m, dm, s, ds)

            row = {
                "level": i,
                "ensemble_id": e,
                "beta": lr["beta"],
                "lattice": lr["lattice"],
                "a_sqrt_sigma": lr["a_sqrt_sigma"],
                "a_sqrt_sigma_err": lr["a_sqrt_sigma_err"],
                "coord_id": cid,
                "channel": ch,
                "state_index": si,
                "label": label,
                "aM": mr["value"],
                "aM_err": mr["uncertainty"],
                "M_over_sqrt_sigma": f"{ratio:.10g}",
                "ratio_err_indep": f"{re:.10g}",
                "record_id": mr["record_id"],
                "source_table": mr["source_table"],
                "note_ids": mr["note_ids"],
            }
            long_rows.append(row)
            wide[f"{cid}_M_over_sqrt_sigma"] = f"{ratio:.10g}"
            wide[f"{cid}_ratio_err_indep"] = f"{re:.10g}"
            if cid == "c1":
                coord1 = mr

        gm = f(lr["am_gap"])
        dgm = f(lr["am_gap_err"])
        gr = gm / s
        gre = ratio_err_indep(gm, dgm, s, ds)
        delta = gm - f(coord1["value"])
        gap_rows.append({
            "level": i,
            "ensemble_id": e,
            "beta": lr["beta"],
            "lattice": lr["lattice"],
            "a_sqrt_sigma": lr["a_sqrt_sigma"],
            "a_sqrt_sigma_err": lr["a_sqrt_sigma_err"],
            "gap_aM_table1": lr["am_gap"],
            "gap_aM_err_table1": lr["am_gap_err"],
            "gap_M_over_sqrt_sigma": f"{gr:.10g}",
            "ratio_err_indep": f"{gre:.10g}",
            "A1pp_ground_aM_table7_13": coord1["value"],
            "table1_minus_spectrum_aM": f"{delta:.10g}",
            "note_ids": lr["note_ids"],
        })
        wide_rows.append(wide)

    # Published continuum references: not treated as a ninth measured refinement level.
    cont_rows = []
    cont_by_key = {(r["channel"], int(r["state_index"])): r for r in cont}
    for cid, ch, si, label in COORDS:
        r = cont_by_key[(ch, si)]
        cont_rows.append({
            "coord_id": cid,
            "channel": ch,
            "state_index": si,
            "label": label,
            "M_over_sqrt_sigma_continuum": r["value"],
            "uncertainty": r["uncertainty"],
            "poor_fit": r["poor_fit"],
            "record_id": r["record_id"],
            "source_table": r["source_table"],
        })

    OUT.mkdir(parents=True, exist_ok=True)

    long_fields = [
        "level","ensemble_id","beta","lattice","a_sqrt_sigma","a_sqrt_sigma_err",
        "coord_id","channel","state_index","label","aM","aM_err",
        "M_over_sqrt_sigma","ratio_err_indep","record_id","source_table","note_ids"
    ]
    write_csv(OUT / "ym1a_long.csv", long_rows, long_fields)

    wide_fields = [
        "level","ensemble_id","beta","lattice","a_sqrt_sigma","a_sqrt_sigma_err","a2_sigma"
    ]
    for cid, *_ in COORDS:
        wide_fields += [f"{cid}_M_over_sqrt_sigma", f"{cid}_ratio_err_indep"]
    write_csv(OUT / "ym1a_refinement.csv", wide_rows, wide_fields)

    gap_fields = [
        "level","ensemble_id","beta","lattice","a_sqrt_sigma","a_sqrt_sigma_err",
        "gap_aM_table1","gap_aM_err_table1","gap_M_over_sqrt_sigma","ratio_err_indep",
        "A1pp_ground_aM_table7_13","table1_minus_spectrum_aM","note_ids"
    ]
    write_csv(OUT / "ym1a_gap.csv", gap_rows, gap_fields)

    cont_fields = [
        "coord_id","channel","state_index","label","M_over_sqrt_sigma_continuum",
        "uncertainty","poor_fit","record_id","source_table"
    ]
    write_csv(OUT / "ym1a_continuum.csv", cont_rows, cont_fields)

    # Verification / build record
    checks = {}
    checks["eight_levels"] = len(wide_rows) == 8
    checks["five_coordinates_each"] = len(long_rows) == 40
    checks["strict_refinement"] = all(
        float(wide_rows[i]["a_sqrt_sigma"]) > float(wide_rows[i+1]["a_sqrt_sigma"])
        for i in range(len(wide_rows)-1)
    )
    checks["positive_ratios"] = all(float(r["M_over_sqrt_sigma"]) > 0 for r in long_rows)
    checks["five_continuum_refs"] = len(cont_rows) == 5
    checks["gap_table_consistency"] = max(abs(float(r["table1_minus_spectrum_aM"])) for r in gap_rows) <= 0.0001000001

    summary = {
        "object": "YM1A refinement ladder",
        "version": "1.0",
        "coordinate_order": [
            {"coord_id": c, "channel": ch, "state_index": si, "label": label}
            for c, ch, si, label in COORDS
        ],
        "levels": 8,
        "coordinates_per_level": 5,
        "normalization": "M/sqrt(sigma) = (aM)/(a*sqrt(sigma))",
        "uncertainty_note": (
            "ratio_err_indep assumes independence only as a diagnostic. "
            "Mass and string-tension estimates may be correlated; no covariance is available here."
        ),
        "continuum_is_reference_not_level": True,
        "checks": checks,
        "passed": all(checks.values()),
        "gap_coarse": float(gap_rows[0]["gap_M_over_sqrt_sigma"]),
        "gap_fine": float(gap_rows[-1]["gap_M_over_sqrt_sigma"]),
        "gap_continuum_published": 3.405,
    }
    RUN.parent.mkdir(parents=True, exist_ok=True)
    RUN.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))

if __name__ == "__main__":
    main()

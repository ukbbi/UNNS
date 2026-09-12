#!/usr/bin/env python3
"""
Inspect Baker flux-tube rows marked REVIEW_SEPARATELY.

Run from the pack root. Expected inputs:
  reports/baker_flux_profile_qc_table.csv
  data/03_core_flux_tube_profiles/baker2024_extended_flux_profiles_long.csv

Outputs:
  reports/05_baker_review_separately_rows.md
  reports/baker_review_separately_decisions.csv
  reports/fig_baker_review_profiles_overlay.png
  reports/fig_baker_review_snr.png
  reports/fig_baker_review_width_flags.png
"""
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

ROOT = Path.cwd()
REPORTS = ROOT / "reports"
DATA = ROOT / "data" / "03_core_flux_tube_profiles"

qc_path = REPORTS / "baker_flux_profile_qc_table.csv"
long_path = DATA / "baker2024_extended_flux_profiles_long.csv"

if not qc_path.exists():
    raise FileNotFoundError(f"Missing {qc_path}")
if not long_path.exists():
    raise FileNotFoundError(f"Missing {long_path}")

qc = pd.read_csv(qc_path)
long = pd.read_csv(long_path)
review = qc[qc["qc_decision"] == "REVIEW_SEPARATELY"].copy()

def get_profile(src, d):
    return long[
        (long["source_file"] == src) &
        (np.isclose(long["source_separation_fm"].astype(float), float(d), atol=1e-6))
    ].copy().sort_values("x_t_fm")

records = []
for _, row in review.iterrows():
    sdf = get_profile(row.source_file, row.source_separation_fm)
    if len(sdf) == 0:
        continue

    center = sdf.iloc[(sdf.x_t_fm.abs()).argmin()]
    peak = sdf.loc[sdf.field_value_GeV2.idxmax()]
    edge = pd.concat([sdf.head(4), sdf.tail(4)])

    peak_snr = abs(peak.field_value_GeV2) / peak.field_error_GeV2 if peak.field_error_GeV2 else np.nan
    center_snr = abs(center.field_value_GeV2) / center.field_error_GeV2 if center.field_error_GeV2 else np.nan
    edge_floor_ratio = edge.field_value_GeV2.abs().mean() / abs(center.field_value_GeV2) if center.field_value_GeV2 != 0 else np.nan
    boundary_peak = abs(peak.x_t_fm) > 0.8 * max(abs(sdf.x_t_fm.min()), abs(sdf.x_t_fm.max()))
    normalized = "normalized" in str(sdf.series_comment.iloc[0]).lower()
    qualitative = "ANALISI_QUALITATIVA_STRING-BREAKING" in str(sdf.series_comment.iloc[0])
    scaling = "ANALISI_SCALING_QCD" in str(sdf.series_comment.iloc[0])

    d = float(row.source_separation_fm)
    src = row.source_file
    decision = "REVIEW_REQUIRED"
    rationale = "not classified by current rule."

    if src == "Ex_NP_d1.0fm_scaling_normfact.agr" and abs(d - 1.033) < 1e-6:
        decision = "EXCLUDE_FROM_TREND_KEEP_AS_OUTLIER_NOTE"
        rationale = "ordinary NP/scaling file, but profile has wide FWHM, high edge floor, and low peak significance; do not interpret as route broadening."
    elif src == "beta7.158dist13.agr":
        decision = "KEEP_SEPARATE_QUALITATIVE_STRING_BREAKING"
        rationale = "clean paper-defined string-breaking profile; single source convention distinct from scaling_normfact profiles."
    elif src == "beta6.3942dist789.agr" and d in [1.064, 1.216]:
        decision = "KEEP_SEPARATE_QUALITATIVE_STRING_BREAKING"
        rationale = "paper-defined qualitative string-breaking profile with central peak; separate from trusted scaling profiles."
    elif src == "QCD_large_distances.agr" and d == 1.216:
        decision = "KEEP_SEPARATE_LARGE_DISTANCE_CONTROL"
        rationale = "large-distance normalized profile with central peak, but separate source convention and larger errors."
    elif src == "QCD_large_distances.agr" and d in [1.235, 1.267]:
        decision = "NORMALIZE_LATER_QUALITATIVE_ONLY"
        rationale = "large-distance normalized profile but low signal-to-noise and unstable width; not usable in current trend."
    elif d == 1.368:
        decision = "EXCLUDE_FROM_INTERPRETATION_FOR_NOW"
        rationale = "maximum occurs at boundary with very large errors; FWHM estimate is a parsing/noise artifact."

    records.append({
        "source_file": src,
        "component": row.component,
        "source_separation_fm": d,
        "target": sdf.target.iloc[0],
        "n_points": len(sdf),
        "peak_field_GeV2": row.peak_field_GeV2,
        "peak_error_GeV2": float(peak.field_error_GeV2),
        "peak_snr": peak_snr,
        "peak_x_fm": float(peak.x_t_fm),
        "center_field_GeV2": float(center.field_value_GeV2),
        "center_error_GeV2": float(center.field_error_GeV2),
        "center_snr": center_snr,
        "fwhm_estimate_fm": row.fwhm_estimate_fm,
        "area_trapz_GeV2_fm": row.area_trapz_GeV2_fm,
        "edge_abs_mean_GeV2": edge.field_value_GeV2.abs().mean(),
        "edge_floor_ratio": edge_floor_ratio,
        "boundary_peak_flag": boundary_peak,
        "normalized_flag": normalized,
        "qualitative_string_breaking_flag": qualitative,
        "scaling_qcd_flag": scaling,
        "series_legend": str(sdf.series_legend.iloc[0]),
        "series_comment": str(sdf.series_comment.iloc[0]),
        "review_decision": decision,
        "review_rationale": rationale,
    })

dec = pd.DataFrame(records)
REPORTS.mkdir(exist_ok=True)
dec.to_csv(REPORTS / "baker_review_separately_decisions.csv", index=False)

# Figures
fig, ax = plt.subplots(figsize=(12, 7))
for _, rec in dec.iterrows():
    sdf = get_profile(rec.source_file, rec.source_separation_fm)
    label = f"{rec.source_file.replace('.agr','')} d={rec.source_separation_fm:.3g} {rec.review_decision[:12]}"
    linestyle = "-" if "KEEP" in rec.review_decision else "--" if "NORMALIZE" in rec.review_decision else ":"
    ax.errorbar(sdf.x_t_fm, sdf.field_value_GeV2, yerr=sdf.field_error_GeV2, marker="o", ms=3, lw=1, alpha=0.65, label=label, linestyle=linestyle)
ax.set_title("Reviewed Baker flux-tube profiles (not in trusted trend)")
ax.set_xlabel("transverse distance x_t [fm]")
ax.set_ylabel("field value [GeV^2]")
ax.grid(True, alpha=0.3)
ax.legend(fontsize=7)
fig.tight_layout()
fig.savefig(REPORTS / "fig_baker_review_profiles_overlay.png", dpi=160)
plt.close(fig)

fig, ax = plt.subplots(figsize=(10, 6))
x = np.arange(len(dec))
ax.bar(x - 0.2, dec.center_snr, width=0.4, label="center SNR")
ax.bar(x + 0.2, dec.peak_snr, width=0.4, label="peak SNR")
ax.axhline(2, color="black", linestyle="--", linewidth=1, label="SNR=2 guide")
ax.set_xticks(x)
ax.set_xticklabels([f"{r.source_file.split('.')[0]}\n{r.source_separation_fm:.3g}" for _, r in dec.iterrows()], rotation=45, ha="right", fontsize=8)
ax.set_ylabel("field / error")
ax.set_title("Signal-to-noise guide for REVIEW_SEPARATELY rows")
ax.grid(True, axis="y", alpha=0.3)
ax.legend()
fig.tight_layout()
fig.savefig(REPORTS / "fig_baker_review_snr.png", dpi=160)
plt.close(fig)

fig, ax = plt.subplots(figsize=(10, 6))
colors = ["tab:red" if "EXCLUDE" in d else "tab:orange" if "NORMALIZE" in d else "tab:blue" for d in dec.review_decision]
ax.bar(x, dec.fwhm_estimate_fm, color=colors)
ax.axhline(1.5, color="black", linestyle="--", linewidth=1, label="QC wide threshold 1.5 fm")
ax.set_xticks(x)
ax.set_xticklabels([f"{r.source_file.split('.')[0]}\n{r.source_separation_fm:.3g}" for _, r in dec.iterrows()], rotation=45, ha="right", fontsize=8)
ax.set_ylabel("FWHM estimate [fm]")
ax.set_title("Width estimates for reviewed rows")
ax.grid(True, axis="y", alpha=0.3)
ax.legend()
fig.tight_layout()
fig.savefig(REPORTS / "fig_baker_review_width_flags.png", dpi=160)
plt.close(fig)

# Compact report
table = "| source file | component | d [fm] | n | peak | peak SNR | FWHM [fm] | decision |\n|---|---|---:|---:|---:|---:|---:|---|\n"
for _, r in dec.iterrows():
    table += f"| `{r.source_file}` | {r.component} | {r.source_separation_fm:.3f} | {int(r.n_points)} | {r.peak_field_GeV2:.6g} | {r.peak_snr:.2f} | {r.fwhm_estimate_fm:.3f} | `{r.review_decision}` |\n"

report = f"""# Baker REVIEW_SEPARATELY Row Inspection

This report inspects the rows previously marked `REVIEW_SEPARATELY` by the Baker flux-tube QC pass.

## Decisions

{table}

## Practical decision

Use only `ACCEPT_FOR_TREND` rows for the main flux-tube trend. Keep qualitative string-breaking and large-distance rows in separate sections. Do not use the excluded/outlier rows as route-broadening evidence.

## Files produced

- `baker_review_separately_decisions.csv`
- `fig_baker_review_profiles_overlay.png`
- `fig_baker_review_snr.png`
- `fig_baker_review_width_flags.png`
"""
(REPORTS / "05_baker_review_separately_rows.md").write_text(report, encoding="utf-8")

print("BAKER REVIEW-SEPARATELY INSPECTION COMPLETE")
print(dec["review_decision"].value_counts().to_string())
print("Report:", REPORTS / "05_baker_review_separately_rows.md")

#!/usr/bin/env python3
"""
MC_GRAMMAR_v001 frozen verdict evaluator.

This file does not recompute the representation or null engine. It evaluates a
prospective candidate record after the frozen `rep_study_v002.py` and
`grammar_dev_v001.py` pipelines have produced the required metrics.

Input JSON schema:
{
  "domain_valid": true,
  "ratio_qualified_v001": true,
  "P_phase_label_p_upper": 0.01,
  "J_frac": 0.2,
  "M_frac": 0.18,
  "M_fourier_p_upper": 0.02,
  "M_robustness": {
      "ORIGIN_SHIFT": 0.17,
      "CLOCK_EXCHANGE": 0.18,
      "AFFINE_STATE": 0.18,
      "DOWNSAMPLE_5": 0.15,
      "PREFIX_0.75": 0.16,
      "NOISE_0.02SD": 0.18
  },
  "collective_annotation": "COLLECTIVE_NOT_ASSESSED"
}

No value in this evaluator may be changed without creating a new grammar version.
"""
import argparse, json
from pathlib import Path

P_GATE = 0.10
M_GATE = 0.12
M_NULL_GATE = 0.10

ROBUSTNESS_VARIANTS = [
    "ORIGIN_SHIFT",
    "CLOCK_EXCHANGE",
    "AFFINE_STATE",
    "DOWNSAMPLE_5",
    "PREFIX_0.75",
    "NOISE_0.02SD",
]

ALLOWED_COLLECTIVE = {
    "COLLECTIVE_NOT_ASSESSED",
    "COLLECTIVE_EVIDENCE_UNAVAILABLE",
    "COLLECTIVE_EVIDENCE_AVAILABLE_FOR_DOMAIN_SPECIFIC_REVIEW",
}

def evaluate(rec):
    flags = []

    if not bool(rec.get("domain_valid", False)):
        return {
            "temporal_state":"OUTSIDE_CHART_DOMAIN",
            "failure_flags":["OUTSIDE_CHART_DOMAIN"],
            "J_frac":rec.get("J_frac"),
            "collective_annotation":rec.get("collective_annotation","COLLECTIVE_NOT_ASSESSED"),
        }

    if not bool(rec.get("ratio_qualified_v001", False)):
        return {
            "temporal_state":"OUTSIDE_EMPIRICALLY_QUALIFIED_RATIO_DOMAIN",
            "failure_flags":["OUTSIDE_EMPIRICALLY_QUALIFIED_RATIO_DOMAIN"],
            "J_frac":rec.get("J_frac"),
            "collective_annotation":rec.get("collective_annotation","COLLECTIVE_NOT_ASSESSED"),
        }

    p = float(rec["P_phase_label_p_upper"])
    j = float(rec["J_frac"])
    m = float(rec["M_frac"])
    mp = float(rec["M_fourier_p_upper"])
    robust = rec["M_robustness"]

    missing = [v for v in ROBUSTNESS_VARIANTS if v not in robust]
    if missing:
        raise ValueError("Missing frozen robustness variants: " + ", ".join(missing))

    if p > P_GATE:
        flags.append("SOURCE_UNANCHORED")
    if m < M_GATE:
        flags.append("MIXED_ORGANIZATION_WEAK")
    if mp > M_NULL_GATE:
        flags.append("MIXED_ORGANIZATION_SPECTRAL_NULL")
    if any(float(robust[v]) < M_GATE for v in ROBUSTNESS_VARIANTS):
        flags.append("MIXED_ORGANIZATION_UNSTABLE")

    precedence = [
        "SOURCE_UNANCHORED",
        "MIXED_ORGANIZATION_WEAK",
        "MIXED_ORGANIZATION_SPECTRAL_NULL",
        "MIXED_ORGANIZATION_UNSTABLE",
    ]
    state = "TEMPORAL_CORE_SUPPORTED"
    for x in precedence:
        if x in flags:
            state = x
            break

    coll = rec.get("collective_annotation","COLLECTIVE_NOT_ASSESSED")
    if coll not in ALLOWED_COLLECTIVE:
        raise ValueError("Unknown collective annotation: " + str(coll))

    return {
        "temporal_state":state,
        "failure_flags":flags,
        "P_phase_label_p_upper":p,
        "J_frac":j,
        "M_frac":m,
        "M_fourier_p_upper":mp,
        "M_robustness":{v:float(robust[v]) for v in ROBUSTNESS_VARIANTS},
        "collective_annotation":coll,
    }

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("record_json")
    ap.add_argument("--output")
    args=ap.parse_args()

    rec=json.loads(Path(args.record_json).read_text())
    out=evaluate(rec)
    text=json.dumps(out,indent=2)
    if args.output:
        Path(args.output).write_text(text+"\n")
    print(text)

if __name__=="__main__":
    main()

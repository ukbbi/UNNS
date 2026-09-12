#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_phase3_transition_corpus.py

Charge Boundary Routing I
Phase 3 — Closure-Preserving Transitions

Purpose
-------
Build the Phase 3 seed corpus for allowed particle transitions.

Phase 3 moves from static boundary classification and bridge geometry to
dynamic closure-preserving transitions. The central question is:

    Do allowed particle transitions preserve the charge-boundary invariant
    while routing identity between different structural regimes?

This script writes:

    data/canonical/phase3_closure_preserving_transitions.csv
    data/derived/phase3_transition_summary.json

Run from the project root:

    python scripts/build_phase3_transition_corpus.py

Project root expected:

    charge_boundary_routing_i/
"""

from __future__ import annotations

import csv
import json
from collections import Counter, defaultdict
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Sequence


# ---------------------------------------------------------------------------
# Phase 1 canonical layer codes
# ---------------------------------------------------------------------------

LAYER_A = "A"  # primitive external integer / neutral charge closures
LAYER_B = "B"  # confined fractional internal charge coordinates
LAYER_C = "C"  # composite integer / neutral charge closures
LAYER_D = "D"  # boundary absences / empirical constraints

LAYER_LABELS = {
    LAYER_A: "primitive_external_closure",
    LAYER_B: "confined_fractional_coordinate",
    LAYER_C: "composite_closure",
    LAYER_D: "boundary_absence_or_constraint",
}


# ---------------------------------------------------------------------------
# Object registry
# ---------------------------------------------------------------------------
# These object records are intentionally minimal and local to Phase 3.
# They encode only what the transition corpus needs:
# object symbol, external charge, Phase 1 layer, route class, and closure class.
#
# UNNS = Unbounded Nested Number Sequences.

OBJECTS: Dict[str, Dict[str, object]] = {
    # Composite closures
    "neutron": {
        "symbol": "n",
        "Q_over_e": 0.0,
        "layer": LAYER_C,
        "route_class": "COMPOSITE_NEUTRAL_ROUTE",
        "closure_class": "COMPOSITE_NEUTRAL_CLOSURE",
        "category": "baryon",
    },
    "proton": {
        "symbol": "p",
        "Q_over_e": 1.0,
        "layer": LAYER_C,
        "route_class": "COMPOSITE_INTEGER_ROUTE",
        "closure_class": "COMPOSITE_INTEGER_CLOSURE",
        "category": "baryon",
    },
    "pi_plus": {
        "symbol": "pi+",
        "Q_over_e": 1.0,
        "layer": LAYER_C,
        "route_class": "COMPOSITE_INTEGER_ROUTE",
        "closure_class": "COMPOSITE_INTEGER_CLOSURE",
        "category": "meson",
    },
    "pi_zero": {
        "symbol": "pi0",
        "Q_over_e": 0.0,
        "layer": LAYER_C,
        "route_class": "COMPOSITE_NEUTRAL_ROUTE",
        "closure_class": "COMPOSITE_NEUTRAL_CLOSURE",
        "category": "meson",
    },
    "k_plus": {
        "symbol": "K+",
        "Q_over_e": 1.0,
        "layer": LAYER_C,
        "route_class": "COMPOSITE_INTEGER_ROUTE",
        "closure_class": "COMPOSITE_INTEGER_CLOSURE",
        "category": "meson",
    },

    # Primitive external closures
    "electron": {
        "symbol": "e-",
        "Q_over_e": -1.0,
        "layer": LAYER_A,
        "route_class": "FREE_INTEGER_ROUTE",
        "closure_class": "FREE_INTEGER_CLOSURE",
        "category": "lepton",
    },
    "positron": {
        "symbol": "e+",
        "Q_over_e": 1.0,
        "layer": LAYER_A,
        "route_class": "FREE_INTEGER_ROUTE",
        "closure_class": "FREE_INTEGER_CLOSURE",
        "category": "lepton",
    },
    "muon_minus": {
        "symbol": "mu-",
        "Q_over_e": -1.0,
        "layer": LAYER_A,
        "route_class": "FREE_INTEGER_ROUTE",
        "closure_class": "FREE_INTEGER_CLOSURE",
        "category": "lepton",
    },
    "muon_plus": {
        "symbol": "mu+",
        "Q_over_e": 1.0,
        "layer": LAYER_A,
        "route_class": "FREE_INTEGER_ROUTE",
        "closure_class": "FREE_INTEGER_CLOSURE",
        "category": "lepton",
    },
    "electron_neutrino": {
        "symbol": "nu_e",
        "Q_over_e": 0.0,
        "layer": LAYER_A,
        "route_class": "FREE_NEUTRAL_ROUTE",
        "closure_class": "FREE_NEUTRAL_CLOSURE",
        "category": "lepton",
    },
    "electron_antineutrino": {
        "symbol": "anti_nu_e",
        "Q_over_e": 0.0,
        "layer": LAYER_A,
        "route_class": "FREE_NEUTRAL_ROUTE",
        "closure_class": "FREE_NEUTRAL_CLOSURE",
        "category": "lepton",
    },
    "muon_neutrino": {
        "symbol": "nu_mu",
        "Q_over_e": 0.0,
        "layer": LAYER_A,
        "route_class": "FREE_NEUTRAL_ROUTE",
        "closure_class": "FREE_NEUTRAL_CLOSURE",
        "category": "lepton",
    },
    "muon_antineutrino": {
        "symbol": "anti_nu_mu",
        "Q_over_e": 0.0,
        "layer": LAYER_A,
        "route_class": "FREE_NEUTRAL_ROUTE",
        "closure_class": "FREE_NEUTRAL_CLOSURE",
        "category": "lepton",
    },
    "w_minus": {
        "symbol": "W-",
        "Q_over_e": -1.0,
        "layer": LAYER_A,
        "route_class": "FREE_INTEGER_ROUTE",
        "closure_class": "FREE_INTEGER_CLOSURE",
        "category": "gauge_boson",
    },
    "w_plus": {
        "symbol": "W+",
        "Q_over_e": 1.0,
        "layer": LAYER_A,
        "route_class": "FREE_INTEGER_ROUTE",
        "closure_class": "FREE_INTEGER_CLOSURE",
        "category": "gauge_boson",
    },
    "photon": {
        "symbol": "gamma",
        "Q_over_e": 0.0,
        "layer": LAYER_A,
        "route_class": "FREE_NEUTRAL_ROUTE",
        "closure_class": "FREE_NEUTRAL_CLOSURE",
        "category": "gauge_boson",
    },
}


@dataclass(frozen=True)
class TransitionSeed:
    transition_id: str
    transition_name: str
    initial_objects: Sequence[str]
    final_objects: Sequence[str]
    transition_class: str
    source_file: str
    source_note: str
    notes: str


# ---------------------------------------------------------------------------
# Phase 3 seed transitions
# ---------------------------------------------------------------------------
# Keep the seed intentionally small and canonical. Additional reactions can be
# added after this first seed is tested through the ladders and chambers.

TRANSITIONS: List[TransitionSeed] = [
    TransitionSeed(
        transition_id="T001",
        transition_name="neutron_beta_decay",
        initial_objects=["neutron"],
        final_objects=["proton", "electron", "electron_antineutrino"],
        transition_class="COMPOSITE_TO_COMPOSITE_PLUS_EXTERNALS",
        source_file="rpp2026-sum-baryons.pdf; rpp2026-sum-leptons.pdf",
        source_note="Seed transition: n -> p + e- + anti_nu_e.",
        notes="Neutral composite closure routes into charged composite closure plus external charged and neutral leptonic closures.",
    ),
    TransitionSeed(
        transition_id="T002",
        transition_name="positive_pion_muonic_decay",
        initial_objects=["pi_plus"],
        final_objects=["muon_plus", "muon_neutrino"],
        transition_class="COMPOSITE_TO_EXTERNALS",
        source_file="rpp2026-sum-mesons.pdf; rpp2026-sum-leptons.pdf",
        source_note="Seed transition: pi+ -> mu+ + nu_mu.",
        notes="Positive composite meson closure routes into positive external lepton plus neutral external lepton.",
    ),
    TransitionSeed(
        transition_id="T003",
        transition_name="negative_muon_decay",
        initial_objects=["muon_minus"],
        final_objects=["electron", "electron_antineutrino", "muon_neutrino"],
        transition_class="LEPTONIC_EXTERNAL_DECAY",
        source_file="rpp2026-sum-leptons.pdf",
        source_note="Seed transition: mu- -> e- + anti_nu_e + nu_mu.",
        notes="Negative external lepton closure routes into lower-mass negative external lepton plus neutral external leptonic closures.",
    ),
    TransitionSeed(
        transition_id="T004",
        transition_name="w_minus_leptonic_decay",
        initial_objects=["w_minus"],
        final_objects=["electron", "electron_antineutrino"],
        transition_class="EXTERNAL_TO_EXTERNALS",
        source_file="rpp2026-sum-gauge-higgs-bosons.pdf; rpp2026-sum-leptons.pdf",
        source_note="Seed transition: W- -> e- + anti_nu_e.",
        notes="Charged gauge-boson external closure routes into charged lepton plus neutral lepton closure.",
    ),
    TransitionSeed(
        transition_id="T005",
        transition_name="w_plus_leptonic_decay",
        initial_objects=["w_plus"],
        final_objects=["positron", "electron_neutrino"],
        transition_class="EXTERNAL_TO_EXTERNALS",
        source_file="rpp2026-sum-gauge-higgs-bosons.pdf; rpp2026-sum-leptons.pdf",
        source_note="Seed transition: W+ -> e+ + nu_e.",
        notes="Positive gauge-boson external closure routes into positive lepton plus neutral lepton closure.",
    ),
    TransitionSeed(
        transition_id="T006",
        transition_name="neutral_pion_two_photon_decay",
        initial_objects=["pi_zero"],
        final_objects=["photon", "photon"],
        transition_class="NEUTRAL_COMPOSITE_TO_RADIATION",
        source_file="rpp2026-sum-mesons.pdf; rpp2026-sum-gauge-higgs-bosons.pdf",
        source_note="Seed transition: pi0 -> gamma + gamma.",
        notes="Neutral composite meson closure routes into two neutral external radiation closures.",
    ),
    TransitionSeed(
        transition_id="T007",
        transition_name="positive_kaon_muonic_decay",
        initial_objects=["k_plus"],
        final_objects=["muon_plus", "muon_neutrino"],
        transition_class="COMPOSITE_TO_EXTERNALS",
        source_file="rpp2026-sum-mesons.pdf; rpp2026-sum-leptons.pdf",
        source_note="Seed transition: K+ -> mu+ + nu_mu.",
        notes="Positive strange meson closure routes into positive external lepton plus neutral external lepton; included to compare same final route form with pion decay.",
    ),
]


FIELDNAMES = [
    "transition_id",
    "transition_name",
    "initial_objects",
    "final_objects",
    "initial_symbols",
    "final_symbols",
    "initial_Q_sum",
    "final_Q_sum",
    "charge_balance_error",
    "charge_conserved",
    "initial_layers",
    "final_layers",
    "layer_transition",
    "initial_route_classes",
    "final_route_classes",
    "route_transition",
    "initial_closure_classes",
    "final_closure_classes",
    "closure_transition",
    "initial_categories",
    "final_categories",
    "initial_multiplicity",
    "final_multiplicity",
    "charged_initial_count",
    "charged_final_count",
    "neutral_initial_count",
    "neutral_final_count",
    "charged_multiplicity_delta",
    "neutral_multiplicity_delta",
    "composite_initial_count",
    "composite_final_count",
    "external_initial_count",
    "external_final_count",
    "composite_count_delta",
    "externalization_delta",
    "boundary_preservation_code",
    "boundary_route_preserved",
    "transition_class",
    "source_file",
    "source_note",
    "notes",
]


def project_root_from_script() -> Path:
    """Return the project root when this script is run from scripts/."""
    return Path(__file__).resolve().parents[1]


def join_values(values: Sequence[object]) -> str:
    return ";".join(str(v) for v in values)


def object_records(object_ids: Sequence[str]) -> List[Dict[str, object]]:
    missing = [obj for obj in object_ids if obj not in OBJECTS]
    if missing:
        raise KeyError(f"Unknown object id(s): {missing}")
    return [OBJECTS[obj] for obj in object_ids]


def charge_sum(records: Sequence[Dict[str, object]]) -> float:
    return round(sum(float(r["Q_over_e"]) for r in records), 12)


def count_charged(records: Sequence[Dict[str, object]]) -> int:
    return sum(1 for r in records if abs(float(r["Q_over_e"])) > 1e-12)


def count_neutral(records: Sequence[Dict[str, object]]) -> int:
    return sum(1 for r in records if abs(float(r["Q_over_e"])) <= 1e-12)


def count_layer(records: Sequence[Dict[str, object]], layer: str) -> int:
    return sum(1 for r in records if r["layer"] == layer)


def transition_code(initial_values: Sequence[str], final_values: Sequence[str]) -> str:
    return f"{join_values(initial_values)}->{join_values(final_values)}"


def build_row(seed: TransitionSeed) -> Dict[str, object]:
    initial = object_records(seed.initial_objects)
    final = object_records(seed.final_objects)

    initial_q = charge_sum(initial)
    final_q = charge_sum(final)
    charge_balance_error = round(final_q - initial_q, 12)

    initial_layers = [str(r["layer"]) for r in initial]
    final_layers = [str(r["layer"]) for r in final]

    initial_routes = [str(r["route_class"]) for r in initial]
    final_routes = [str(r["route_class"]) for r in final]

    initial_closures = [str(r["closure_class"]) for r in initial]
    final_closures = [str(r["closure_class"]) for r in final]

    initial_categories = [str(r["category"]) for r in initial]
    final_categories = [str(r["category"]) for r in final]

    charged_initial = count_charged(initial)
    charged_final = count_charged(final)
    neutral_initial = count_neutral(initial)
    neutral_final = count_neutral(final)

    composite_initial = count_layer(initial, LAYER_C)
    composite_final = count_layer(final, LAYER_C)
    external_initial = count_layer(initial, LAYER_A)
    external_final = count_layer(final, LAYER_A)

    # Boundary preservation is seeded as 1 for allowed charge-conserving
    # transitions. Later Phase 3 expansions can add forbidden/constrained
    # transitions with code 0 or -1.
    boundary_route_preserved = abs(charge_balance_error) <= 1e-12
    boundary_preservation_code = 1 if boundary_route_preserved else 0

    return {
        "transition_id": seed.transition_id,
        "transition_name": seed.transition_name,
        "initial_objects": join_values(seed.initial_objects),
        "final_objects": join_values(seed.final_objects),
        "initial_symbols": join_values([r["symbol"] for r in initial]),
        "final_symbols": join_values([r["symbol"] for r in final]),
        "initial_Q_sum": initial_q,
        "final_Q_sum": final_q,
        "charge_balance_error": charge_balance_error,
        "charge_conserved": str(boundary_route_preserved).upper(),
        "initial_layers": join_values(initial_layers),
        "final_layers": join_values(final_layers),
        "layer_transition": transition_code(initial_layers, final_layers),
        "initial_route_classes": join_values(initial_routes),
        "final_route_classes": join_values(final_routes),
        "route_transition": transition_code(initial_routes, final_routes),
        "initial_closure_classes": join_values(initial_closures),
        "final_closure_classes": join_values(final_closures),
        "closure_transition": transition_code(initial_closures, final_closures),
        "initial_categories": join_values(initial_categories),
        "final_categories": join_values(final_categories),
        "initial_multiplicity": len(initial),
        "final_multiplicity": len(final),
        "charged_initial_count": charged_initial,
        "charged_final_count": charged_final,
        "neutral_initial_count": neutral_initial,
        "neutral_final_count": neutral_final,
        "charged_multiplicity_delta": charged_final - charged_initial,
        "neutral_multiplicity_delta": neutral_final - neutral_initial,
        "composite_initial_count": composite_initial,
        "composite_final_count": composite_final,
        "external_initial_count": external_initial,
        "external_final_count": external_final,
        "composite_count_delta": composite_final - composite_initial,
        "externalization_delta": external_final - external_initial,
        "boundary_preservation_code": boundary_preservation_code,
        "boundary_route_preserved": str(boundary_route_preserved).upper(),
        "transition_class": seed.transition_class,
        "source_file": seed.source_file,
        "source_note": seed.source_note,
        "notes": seed.notes,
    }


def write_csv(path: Path, rows: Sequence[Dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def build_summary(rows: Sequence[Dict[str, object]]) -> Dict[str, object]:
    transition_classes = Counter(str(row["transition_class"]) for row in rows)
    layer_transitions = Counter(str(row["layer_transition"]) for row in rows)
    charge_errors = [float(row["charge_balance_error"]) for row in rows]
    conserved_count = sum(1 for row in rows if str(row["charge_conserved"]) == "TRUE")

    route_transition_counts = Counter(str(row["route_transition"]) for row in rows)
    closure_transition_counts = Counter(str(row["closure_transition"]) for row in rows)

    by_transition_class = defaultdict(list)
    for row in rows:
        by_transition_class[str(row["transition_class"])].append(str(row["transition_id"]))

    return {
        "program": "UNNS Substrate Program",
        "project": "Charge Boundary Routing I",
        "phase": "Phase 3 — Closure-Preserving Transitions",
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "row_count": len(rows),
        "charge_conserved_count": conserved_count,
        "charge_nonconserved_count": len(rows) - conserved_count,
        "max_abs_charge_balance_error": max(abs(x) for x in charge_errors) if charge_errors else None,
        "layer_labels": LAYER_LABELS,
        "transition_classes": dict(sorted(transition_classes.items())),
        "layer_transitions": dict(sorted(layer_transitions.items())),
        "route_transition_count": len(route_transition_counts),
        "closure_transition_count": len(closure_transition_counts),
        "transition_ids_by_class": {
            key: sorted(value) for key, value in sorted(by_transition_class.items())
        },
        "output_files": {
            "canonical_csv": "data/canonical/phase3_closure_preserving_transitions.csv",
            "summary_json": "data/derived/phase3_transition_summary.json",
        },
        "notes": [
            "This is a seed corpus, not a complete particle-decay database.",
            "The seed is designed to test charge-boundary preservation across different route and closure regimes.",
            "Phase 2C same-charge route control remains reserved as a separate validation/control corpus.",
        ],
    }


def main() -> int:
    root = project_root_from_script()

    canonical_csv = root / "data" / "canonical" / "phase3_closure_preserving_transitions.csv"
    summary_json = root / "data" / "derived" / "phase3_transition_summary.json"

    # Prepare Phase 3 folders now, so the next ladder builder has a clean target.
    phase3_dirs = [
        root / "data" / "canonical",
        root / "data" / "derived",
        root / "ladders" / "phase3_transitions",
        root / "ladders" / "phase3_transitions" / "one_column",
        root / "ladders" / "phase3_transitions" / "diagnostics",
        root / "results" / "struc_perc_i" / "phase3_transitions",
        root / "results" / "struc_i" / "phase3_transitions",
        root / "outputs" / "reports" / "phase3_transitions",
    ]
    for directory in phase3_dirs:
        directory.mkdir(parents=True, exist_ok=True)

    rows = [build_row(seed) for seed in TRANSITIONS]

    write_csv(canonical_csv, rows)

    summary = build_summary(rows)
    summary_json.parent.mkdir(parents=True, exist_ok=True)
    summary_json.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")

    print("Phase 3 transition seed corpus built.")
    print(f"Rows: {len(rows)}")
    print(f"Wrote: {canonical_csv.relative_to(root)}")
    print(f"Wrote: {summary_json.relative_to(root)}")
    print("")
    print("Next step:")
    print("  build_phase3_transition_ladders.py")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

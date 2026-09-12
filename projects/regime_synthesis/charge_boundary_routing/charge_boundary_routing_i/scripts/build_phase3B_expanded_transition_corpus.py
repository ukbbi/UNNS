#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_phase3B_expanded_transition_corpus.py

Charge Boundary Routing I
Phase 3B — Expanded Allowed Transition Corpus

Purpose
-------
Build a larger allowed-transition corpus to test whether the Phase 3 seed result
is robust beyond the first seven transitions.

Phase 3 seed result:
    route_transition_code, closure_transition_code, transition_class_code,
    initial_total_charge, and final_total_charge reached weak persistence.

Phase 3B question:
    Do route_transition_code and closure_transition_code remain weakly
    persistent when the transition corpus grows beyond the 7-transition seed?

This script writes:

    data/canonical/phase3B_expanded_allowed_transition_corpus.csv
    data/derived/phase3B_expanded_allowed_transition_summary.json

It also prepares:

    ladders/phase3B_expanded_transitions/
    ladders/phase3B_expanded_transitions/one_column/
    ladders/phase3B_expanded_transitions/diagnostics/
    results/struc_perc_i/phase3B_expanded_transitions/
    results/struc_i/phase3B_expanded_transitions/
    outputs/reports/phase3B_expanded_transitions/

Run from project root:

    python scripts/build_phase3B_expanded_transition_corpus.py
"""

from __future__ import annotations

import csv
import json
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Sequence


# ---------------------------------------------------------------------------
# Phase layer codes
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
# This registry is intentionally local and audit-friendly. It captures only
# the fields needed for charge-boundary transition encoding.
#
# UNNS = Unbounded Nested Number Sequences.

OBJECTS: Dict[str, Dict[str, object]] = {
    # -----------------------------------------------------------------------
    # Primitive external closures: leptons and gauge/radiation objects
    # -----------------------------------------------------------------------
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
    "tau_minus": {
        "symbol": "tau-",
        "Q_over_e": -1.0,
        "layer": LAYER_A,
        "route_class": "FREE_INTEGER_ROUTE",
        "closure_class": "FREE_INTEGER_CLOSURE",
        "category": "lepton",
    },
    "tau_plus": {
        "symbol": "tau+",
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
    "tau_neutrino": {
        "symbol": "nu_tau",
        "Q_over_e": 0.0,
        "layer": LAYER_A,
        "route_class": "FREE_NEUTRAL_ROUTE",
        "closure_class": "FREE_NEUTRAL_CLOSURE",
        "category": "lepton",
    },
    "tau_antineutrino": {
        "symbol": "anti_nu_tau",
        "Q_over_e": 0.0,
        "layer": LAYER_A,
        "route_class": "FREE_NEUTRAL_ROUTE",
        "closure_class": "FREE_NEUTRAL_CLOSURE",
        "category": "lepton",
    },
    "photon": {
        "symbol": "gamma",
        "Q_over_e": 0.0,
        "layer": LAYER_A,
        "route_class": "FREE_NEUTRAL_ROUTE",
        "closure_class": "FREE_NEUTRAL_CLOSURE",
        "category": "gauge_boson",
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
    "z_boson": {
        "symbol": "Z",
        "Q_over_e": 0.0,
        "layer": LAYER_A,
        "route_class": "FREE_NEUTRAL_ROUTE",
        "closure_class": "FREE_NEUTRAL_CLOSURE",
        "category": "gauge_boson",
    },

    # -----------------------------------------------------------------------
    # Composite closures: baryons
    # -----------------------------------------------------------------------
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
    "lambda_zero": {
        "symbol": "Lambda0",
        "Q_over_e": 0.0,
        "layer": LAYER_C,
        "route_class": "COMPOSITE_NEUTRAL_ROUTE",
        "closure_class": "COMPOSITE_NEUTRAL_CLOSURE",
        "category": "baryon",
    },
    "sigma_plus": {
        "symbol": "Sigma+",
        "Q_over_e": 1.0,
        "layer": LAYER_C,
        "route_class": "COMPOSITE_INTEGER_ROUTE",
        "closure_class": "COMPOSITE_INTEGER_CLOSURE",
        "category": "baryon",
    },
    "sigma_zero": {
        "symbol": "Sigma0",
        "Q_over_e": 0.0,
        "layer": LAYER_C,
        "route_class": "COMPOSITE_NEUTRAL_ROUTE",
        "closure_class": "COMPOSITE_NEUTRAL_CLOSURE",
        "category": "baryon",
    },
    "sigma_minus": {
        "symbol": "Sigma-",
        "Q_over_e": -1.0,
        "layer": LAYER_C,
        "route_class": "COMPOSITE_INTEGER_ROUTE",
        "closure_class": "COMPOSITE_INTEGER_CLOSURE",
        "category": "baryon",
    },
    "xi_zero": {
        "symbol": "Xi0",
        "Q_over_e": 0.0,
        "layer": LAYER_C,
        "route_class": "COMPOSITE_NEUTRAL_ROUTE",
        "closure_class": "COMPOSITE_NEUTRAL_CLOSURE",
        "category": "baryon",
    },
    "xi_minus": {
        "symbol": "Xi-",
        "Q_over_e": -1.0,
        "layer": LAYER_C,
        "route_class": "COMPOSITE_INTEGER_ROUTE",
        "closure_class": "COMPOSITE_INTEGER_CLOSURE",
        "category": "baryon",
    },
    "omega_minus": {
        "symbol": "Omega-",
        "Q_over_e": -1.0,
        "layer": LAYER_C,
        "route_class": "COMPOSITE_INTEGER_ROUTE",
        "closure_class": "COMPOSITE_INTEGER_CLOSURE",
        "category": "baryon",
    },
    "delta_plus_plus": {
        "symbol": "Delta++",
        "Q_over_e": 2.0,
        "layer": LAYER_C,
        "route_class": "COMPOSITE_INTEGER_ROUTE",
        "closure_class": "COMPOSITE_INTEGER_CLOSURE",
        "category": "baryon",
    },
    "delta_plus": {
        "symbol": "Delta+",
        "Q_over_e": 1.0,
        "layer": LAYER_C,
        "route_class": "COMPOSITE_INTEGER_ROUTE",
        "closure_class": "COMPOSITE_INTEGER_CLOSURE",
        "category": "baryon",
    },
    "delta_zero": {
        "symbol": "Delta0",
        "Q_over_e": 0.0,
        "layer": LAYER_C,
        "route_class": "COMPOSITE_NEUTRAL_ROUTE",
        "closure_class": "COMPOSITE_NEUTRAL_CLOSURE",
        "category": "baryon",
    },
    "delta_minus": {
        "symbol": "Delta-",
        "Q_over_e": -1.0,
        "layer": LAYER_C,
        "route_class": "COMPOSITE_INTEGER_ROUTE",
        "closure_class": "COMPOSITE_INTEGER_CLOSURE",
        "category": "baryon",
    },

    # -----------------------------------------------------------------------
    # Composite closures: mesons
    # -----------------------------------------------------------------------
    "pi_plus": {
        "symbol": "pi+",
        "Q_over_e": 1.0,
        "layer": LAYER_C,
        "route_class": "COMPOSITE_INTEGER_ROUTE",
        "closure_class": "COMPOSITE_INTEGER_CLOSURE",
        "category": "meson",
    },
    "pi_minus": {
        "symbol": "pi-",
        "Q_over_e": -1.0,
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
    "k_minus": {
        "symbol": "K-",
        "Q_over_e": -1.0,
        "layer": LAYER_C,
        "route_class": "COMPOSITE_INTEGER_ROUTE",
        "closure_class": "COMPOSITE_INTEGER_CLOSURE",
        "category": "meson",
    },
    "k_zero": {
        "symbol": "K0",
        "Q_over_e": 0.0,
        "layer": LAYER_C,
        "route_class": "COMPOSITE_NEUTRAL_ROUTE",
        "closure_class": "COMPOSITE_NEUTRAL_CLOSURE",
        "category": "meson",
    },
    "k_zero_bar": {
        "symbol": "anti_K0",
        "Q_over_e": 0.0,
        "layer": LAYER_C,
        "route_class": "COMPOSITE_NEUTRAL_ROUTE",
        "closure_class": "COMPOSITE_NEUTRAL_CLOSURE",
        "category": "meson",
    },
    "eta": {
        "symbol": "eta",
        "Q_over_e": 0.0,
        "layer": LAYER_C,
        "route_class": "COMPOSITE_NEUTRAL_ROUTE",
        "closure_class": "COMPOSITE_NEUTRAL_CLOSURE",
        "category": "meson",
    },
    "eta_prime": {
        "symbol": "eta_prime",
        "Q_over_e": 0.0,
        "layer": LAYER_C,
        "route_class": "COMPOSITE_NEUTRAL_ROUTE",
        "closure_class": "COMPOSITE_NEUTRAL_CLOSURE",
        "category": "meson",
    },
    "rho_plus": {
        "symbol": "rho+",
        "Q_over_e": 1.0,
        "layer": LAYER_C,
        "route_class": "COMPOSITE_INTEGER_ROUTE",
        "closure_class": "COMPOSITE_INTEGER_CLOSURE",
        "category": "meson",
    },
    "rho_zero": {
        "symbol": "rho0",
        "Q_over_e": 0.0,
        "layer": LAYER_C,
        "route_class": "COMPOSITE_NEUTRAL_ROUTE",
        "closure_class": "COMPOSITE_NEUTRAL_CLOSURE",
        "category": "meson",
    },
    "rho_minus": {
        "symbol": "rho-",
        "Q_over_e": -1.0,
        "layer": LAYER_C,
        "route_class": "COMPOSITE_INTEGER_ROUTE",
        "closure_class": "COMPOSITE_INTEGER_CLOSURE",
        "category": "meson",
    },
    "omega_meson": {
        "symbol": "omega",
        "Q_over_e": 0.0,
        "layer": LAYER_C,
        "route_class": "COMPOSITE_NEUTRAL_ROUTE",
        "closure_class": "COMPOSITE_NEUTRAL_CLOSURE",
        "category": "meson",
    },
    "phi_meson": {
        "symbol": "phi",
        "Q_over_e": 0.0,
        "layer": LAYER_C,
        "route_class": "COMPOSITE_NEUTRAL_ROUTE",
        "closure_class": "COMPOSITE_NEUTRAL_CLOSURE",
        "category": "meson",
    },
}


@dataclass(frozen=True)
class TransitionSeed:
    transition_id: str
    transition_name: str
    initial_objects: Sequence[str]
    final_objects: Sequence[str]
    transition_class: str
    transition_family: str
    source_file: str
    source_note: str
    notes: str


# ---------------------------------------------------------------------------
# Expanded allowed-transition corpus
# ---------------------------------------------------------------------------
# Includes the original Phase 3 seven-transition seed plus a larger controlled
# expansion. This makes Phase 3B a robustness test rather than a disconnected
# corpus.

TRANSITIONS: List[TransitionSeed] = [
    # -----------------------------------------------------------------------
    # Original Phase 3 seed retained for continuity
    # -----------------------------------------------------------------------
    TransitionSeed(
        "T001", "neutron_beta_decay",
        ["neutron"], ["proton", "electron", "electron_antineutrino"],
        "COMPOSITE_TO_COMPOSITE_PLUS_EXTERNALS", "seed_continuity",
        "rpp2026-sum-baryons.pdf; rpp2026-sum-leptons.pdf",
        "n -> p + e- + anti_nu_e.",
        "Original Phase 3 seed transition retained for continuity."
    ),
    TransitionSeed(
        "T002", "positive_pion_muonic_decay",
        ["pi_plus"], ["muon_plus", "muon_neutrino"],
        "COMPOSITE_TO_EXTERNALS", "seed_continuity",
        "rpp2026-sum-mesons.pdf; rpp2026-sum-leptons.pdf",
        "pi+ -> mu+ + nu_mu.",
        "Original Phase 3 seed transition retained for continuity."
    ),
    TransitionSeed(
        "T003", "negative_muon_decay",
        ["muon_minus"], ["electron", "electron_antineutrino", "muon_neutrino"],
        "LEPTONIC_EXTERNAL_DECAY", "seed_continuity",
        "rpp2026-sum-leptons.pdf",
        "mu- -> e- + anti_nu_e + nu_mu.",
        "Original Phase 3 seed transition retained for continuity."
    ),
    TransitionSeed(
        "T004", "w_minus_leptonic_decay",
        ["w_minus"], ["electron", "electron_antineutrino"],
        "EXTERNAL_TO_EXTERNALS", "seed_continuity",
        "rpp2026-sum-gauge-higgs-bosons.pdf; rpp2026-sum-leptons.pdf",
        "W- -> e- + anti_nu_e.",
        "Original Phase 3 seed transition retained for continuity."
    ),
    TransitionSeed(
        "T005", "w_plus_leptonic_decay",
        ["w_plus"], ["positron", "electron_neutrino"],
        "EXTERNAL_TO_EXTERNALS", "seed_continuity",
        "rpp2026-sum-gauge-higgs-bosons.pdf; rpp2026-sum-leptons.pdf",
        "W+ -> e+ + nu_e.",
        "Original Phase 3 seed transition retained for continuity."
    ),
    TransitionSeed(
        "T006", "neutral_pion_two_photon_decay",
        ["pi_zero"], ["photon", "photon"],
        "NEUTRAL_COMPOSITE_TO_RADIATION", "seed_continuity",
        "rpp2026-sum-mesons.pdf; rpp2026-sum-gauge-higgs-bosons.pdf",
        "pi0 -> gamma + gamma.",
        "Original Phase 3 seed transition retained for continuity."
    ),
    TransitionSeed(
        "T007", "positive_kaon_muonic_decay",
        ["k_plus"], ["muon_plus", "muon_neutrino"],
        "COMPOSITE_TO_EXTERNALS", "seed_continuity",
        "rpp2026-sum-mesons.pdf; rpp2026-sum-leptons.pdf",
        "K+ -> mu+ + nu_mu.",
        "Original Phase 3 seed transition retained for continuity."
    ),

    # -----------------------------------------------------------------------
    # Additional charged meson decays
    # -----------------------------------------------------------------------
    TransitionSeed(
        "T008", "negative_pion_muonic_decay",
        ["pi_minus"], ["muon_minus", "muon_antineutrino"],
        "COMPOSITE_TO_EXTERNALS", "charged_meson_decay",
        "rpp2026-sum-mesons.pdf; rpp2026-sum-leptons.pdf",
        "pi- -> mu- + anti_nu_mu.",
        "Charge-conjugate counterpart of positive pion muonic decay."
    ),
    TransitionSeed(
        "T009", "positive_pion_electronic_decay",
        ["pi_plus"], ["positron", "electron_neutrino"],
        "COMPOSITE_TO_EXTERNALS", "charged_meson_decay",
        "rpp2026-sum-mesons.pdf; rpp2026-sum-leptons.pdf",
        "pi+ -> e+ + nu_e.",
        "Leptonic charged pion electronic channel."
    ),
    TransitionSeed(
        "T010", "negative_pion_electronic_decay",
        ["pi_minus"], ["electron", "electron_antineutrino"],
        "COMPOSITE_TO_EXTERNALS", "charged_meson_decay",
        "rpp2026-sum-mesons.pdf; rpp2026-sum-leptons.pdf",
        "pi- -> e- + anti_nu_e.",
        "Charge-conjugate electronic pion channel."
    ),
    TransitionSeed(
        "T011", "negative_kaon_muonic_decay",
        ["k_minus"], ["muon_minus", "muon_antineutrino"],
        "COMPOSITE_TO_EXTERNALS", "charged_meson_decay",
        "rpp2026-sum-mesons.pdf; rpp2026-sum-leptons.pdf",
        "K- -> mu- + anti_nu_mu.",
        "Charge-conjugate counterpart of positive kaon muonic decay."
    ),
    TransitionSeed(
        "T012", "positive_kaon_pionic_decay",
        ["k_plus"], ["pi_plus", "pi_zero"],
        "COMPOSITE_TO_COMPOSITES", "charged_meson_decay",
        "rpp2026-sum-mesons.pdf",
        "K+ -> pi+ + pi0.",
        "Charged kaon routes into charged and neutral composite meson closures."
    ),
    TransitionSeed(
        "T013", "negative_kaon_pionic_decay",
        ["k_minus"], ["pi_minus", "pi_zero"],
        "COMPOSITE_TO_COMPOSITES", "charged_meson_decay",
        "rpp2026-sum-mesons.pdf",
        "K- -> pi- + pi0.",
        "Charge-conjugate composite meson channel."
    ),

    # -----------------------------------------------------------------------
    # Additional neutral meson decays
    # -----------------------------------------------------------------------
    TransitionSeed(
        "T014", "eta_two_photon_decay",
        ["eta"], ["photon", "photon"],
        "NEUTRAL_COMPOSITE_TO_RADIATION", "neutral_meson_decay",
        "rpp2026-sum-mesons.pdf; rpp2026-sum-gauge-higgs-bosons.pdf",
        "eta -> gamma + gamma.",
        "Neutral composite meson routes into two neutral external radiation closures."
    ),
    TransitionSeed(
        "T015", "eta_three_pion_decay",
        ["eta"], ["pi_plus", "pi_minus", "pi_zero"],
        "NEUTRAL_COMPOSITE_TO_COMPOSITES", "neutral_meson_decay",
        "rpp2026-sum-mesons.pdf",
        "eta -> pi+ + pi- + pi0.",
        "Neutral composite meson routes into charged-pair plus neutral composite closures."
    ),
    TransitionSeed(
        "T016", "rho_zero_two_pion_decay",
        ["rho_zero"], ["pi_plus", "pi_minus"],
        "NEUTRAL_COMPOSITE_TO_COMPOSITES", "neutral_meson_decay",
        "rpp2026-sum-mesons.pdf",
        "rho0 -> pi+ + pi-.",
        "Neutral vector meson routes into charged composite pair."
    ),
    TransitionSeed(
        "T017", "rho_plus_pion_decay",
        ["rho_plus"], ["pi_plus", "pi_zero"],
        "COMPOSITE_TO_COMPOSITES", "neutral_or_charged_vector_meson_decay",
        "rpp2026-sum-mesons.pdf",
        "rho+ -> pi+ + pi0.",
        "Charged vector meson routes into charged and neutral composite mesons."
    ),
    TransitionSeed(
        "T018", "rho_minus_pion_decay",
        ["rho_minus"], ["pi_minus", "pi_zero"],
        "COMPOSITE_TO_COMPOSITES", "neutral_or_charged_vector_meson_decay",
        "rpp2026-sum-mesons.pdf",
        "rho- -> pi- + pi0.",
        "Charge-conjugate vector meson composite channel."
    ),
    TransitionSeed(
        "T019", "omega_three_pion_decay",
        ["omega_meson"], ["pi_plus", "pi_minus", "pi_zero"],
        "NEUTRAL_COMPOSITE_TO_COMPOSITES", "neutral_meson_decay",
        "rpp2026-sum-mesons.pdf",
        "omega -> pi+ + pi- + pi0.",
        "Neutral composite vector meson routes into three composite pions."
    ),
    TransitionSeed(
        "T020", "phi_kaon_pair_decay",
        ["phi_meson"], ["k_plus", "k_minus"],
        "NEUTRAL_COMPOSITE_TO_COMPOSITES", "neutral_meson_decay",
        "rpp2026-sum-mesons.pdf",
        "phi -> K+ + K-.",
        "Neutral composite vector meson routes into charged kaon pair."
    ),

    # -----------------------------------------------------------------------
    # Baryon decays
    # -----------------------------------------------------------------------
    TransitionSeed(
        "T021", "lambda_to_proton_pion_minus",
        ["lambda_zero"], ["proton", "pi_minus"],
        "COMPOSITE_TO_COMPOSITES", "baryon_decay",
        "rpp2026-sum-baryons.pdf; rpp2026-sum-mesons.pdf",
        "Lambda0 -> p + pi-.",
        "Neutral baryon routes into charged baryon plus oppositely charged meson."
    ),
    TransitionSeed(
        "T022", "lambda_to_neutron_pion_zero",
        ["lambda_zero"], ["neutron", "pi_zero"],
        "COMPOSITE_TO_COMPOSITES", "baryon_decay",
        "rpp2026-sum-baryons.pdf; rpp2026-sum-mesons.pdf",
        "Lambda0 -> n + pi0.",
        "Neutral baryon routes into neutral baryon plus neutral meson."
    ),
    TransitionSeed(
        "T023", "sigma_plus_to_proton_pion_zero",
        ["sigma_plus"], ["proton", "pi_zero"],
        "COMPOSITE_TO_COMPOSITES", "baryon_decay",
        "rpp2026-sum-baryons.pdf; rpp2026-sum-mesons.pdf",
        "Sigma+ -> p + pi0.",
        "Charged baryon routes into charged baryon plus neutral meson."
    ),
    TransitionSeed(
        "T024", "sigma_plus_to_neutron_pion_plus",
        ["sigma_plus"], ["neutron", "pi_plus"],
        "COMPOSITE_TO_COMPOSITES", "baryon_decay",
        "rpp2026-sum-baryons.pdf; rpp2026-sum-mesons.pdf",
        "Sigma+ -> n + pi+.",
        "Charged baryon routes into neutral baryon plus charged meson."
    ),
    TransitionSeed(
        "T025", "sigma_minus_to_neutron_pion_minus",
        ["sigma_minus"], ["neutron", "pi_minus"],
        "COMPOSITE_TO_COMPOSITES", "baryon_decay",
        "rpp2026-sum-baryons.pdf; rpp2026-sum-mesons.pdf",
        "Sigma- -> n + pi-.",
        "Negative baryon routes into neutral baryon plus negative meson."
    ),
    TransitionSeed(
        "T026", "xi_minus_to_lambda_pion_minus",
        ["xi_minus"], ["lambda_zero", "pi_minus"],
        "COMPOSITE_TO_COMPOSITES", "baryon_decay",
        "rpp2026-sum-baryons.pdf; rpp2026-sum-mesons.pdf",
        "Xi- -> Lambda0 + pi-.",
        "Negative cascade baryon routes into neutral baryon plus negative meson."
    ),
    TransitionSeed(
        "T027", "xi_zero_to_lambda_pion_zero",
        ["xi_zero"], ["lambda_zero", "pi_zero"],
        "COMPOSITE_TO_COMPOSITES", "baryon_decay",
        "rpp2026-sum-baryons.pdf; rpp2026-sum-mesons.pdf",
        "Xi0 -> Lambda0 + pi0.",
        "Neutral cascade baryon routes into neutral baryon plus neutral meson."
    ),
    TransitionSeed(
        "T028", "omega_minus_to_lambda_kaon_minus",
        ["omega_minus"], ["lambda_zero", "k_minus"],
        "COMPOSITE_TO_COMPOSITES", "baryon_decay",
        "rpp2026-sum-baryons.pdf; rpp2026-sum-mesons.pdf",
        "Omega- -> Lambda0 + K-.",
        "Negative omega baryon routes into neutral baryon plus negative kaon."
    ),
    TransitionSeed(
        "T029", "delta_plus_plus_to_proton_pion_plus",
        ["delta_plus_plus"], ["proton", "pi_plus"],
        "COMPOSITE_TO_COMPOSITES", "baryon_resonance_decay",
        "rpp2026-sum-baryons.pdf; rpp2026-sum-mesons.pdf",
        "Delta++ -> p + pi+.",
        "Doubly charged baryon resonance routes into two positive composite closures."
    ),
    TransitionSeed(
        "T030", "delta_minus_to_neutron_pion_minus",
        ["delta_minus"], ["neutron", "pi_minus"],
        "COMPOSITE_TO_COMPOSITES", "baryon_resonance_decay",
        "rpp2026-sum-baryons.pdf; rpp2026-sum-mesons.pdf",
        "Delta- -> n + pi-.",
        "Negative baryon resonance routes into neutral baryon plus negative pion."
    ),

    # -----------------------------------------------------------------------
    # W / Z mediated external channels
    # -----------------------------------------------------------------------
    TransitionSeed(
        "T031", "w_minus_muonic_decay",
        ["w_minus"], ["muon_minus", "muon_antineutrino"],
        "EXTERNAL_TO_EXTERNALS", "w_z_mediated_channel",
        "rpp2026-sum-gauge-higgs-bosons.pdf; rpp2026-sum-leptons.pdf",
        "W- -> mu- + anti_nu_mu.",
        "External charged gauge closure routes into muon channel."
    ),
    TransitionSeed(
        "T032", "w_plus_muonic_decay",
        ["w_plus"], ["muon_plus", "muon_neutrino"],
        "EXTERNAL_TO_EXTERNALS", "w_z_mediated_channel",
        "rpp2026-sum-gauge-higgs-bosons.pdf; rpp2026-sum-leptons.pdf",
        "W+ -> mu+ + nu_mu.",
        "Charge-conjugate W muon channel."
    ),
    TransitionSeed(
        "T033", "w_minus_tauonic_decay",
        ["w_minus"], ["tau_minus", "tau_antineutrino"],
        "EXTERNAL_TO_EXTERNALS", "w_z_mediated_channel",
        "rpp2026-sum-gauge-higgs-bosons.pdf; rpp2026-sum-leptons.pdf",
        "W- -> tau- + anti_nu_tau.",
        "External charged gauge closure routes into tau channel."
    ),
    TransitionSeed(
        "T034", "w_plus_tauonic_decay",
        ["w_plus"], ["tau_plus", "tau_neutrino"],
        "EXTERNAL_TO_EXTERNALS", "w_z_mediated_channel",
        "rpp2026-sum-gauge-higgs-bosons.pdf; rpp2026-sum-leptons.pdf",
        "W+ -> tau+ + nu_tau.",
        "Charge-conjugate W tau channel."
    ),
    TransitionSeed(
        "T035", "z_to_electron_pair",
        ["z_boson"], ["electron", "positron"],
        "NEUTRAL_EXTERNAL_TO_EXTERNALS", "w_z_mediated_channel",
        "rpp2026-sum-gauge-higgs-bosons.pdf; rpp2026-sum-leptons.pdf",
        "Z -> e- + e+.",
        "Neutral gauge closure routes into opposite-charge external lepton pair."
    ),
    TransitionSeed(
        "T036", "z_to_muon_pair",
        ["z_boson"], ["muon_minus", "muon_plus"],
        "NEUTRAL_EXTERNAL_TO_EXTERNALS", "w_z_mediated_channel",
        "rpp2026-sum-gauge-higgs-bosons.pdf; rpp2026-sum-leptons.pdf",
        "Z -> mu- + mu+.",
        "Neutral gauge closure routes into opposite-charge muon pair."
    ),

    # -----------------------------------------------------------------------
    # Radiative decays
    # -----------------------------------------------------------------------
    TransitionSeed(
        "T037", "sigma_zero_radiative_decay",
        ["sigma_zero"], ["lambda_zero", "photon"],
        "COMPOSITE_TO_COMPOSITE_PLUS_RADIATION", "radiative_decay",
        "rpp2026-sum-baryons.pdf; rpp2026-sum-gauge-higgs-bosons.pdf",
        "Sigma0 -> Lambda0 + gamma.",
        "Neutral baryon closure routes into neutral baryon plus radiation closure."
    ),
    TransitionSeed(
        "T038", "eta_prime_radiative_decay",
        ["eta_prime"], ["rho_zero", "photon"],
        "NEUTRAL_COMPOSITE_TO_COMPOSITE_PLUS_RADIATION", "radiative_decay",
        "rpp2026-sum-mesons.pdf; rpp2026-sum-gauge-higgs-bosons.pdf",
        "eta_prime -> rho0 + gamma.",
        "Neutral meson routes into neutral vector meson plus radiation closure."
    ),
]


FIELDNAMES = [
    "transition_id",
    "transition_name",
    "phase",
    "batch",
    "transition_family",
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
    "category_transition",
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

    boundary_route_preserved = abs(charge_balance_error) <= 1e-12
    boundary_preservation_code = 1 if boundary_route_preserved else 0

    return {
        "transition_id": seed.transition_id,
        "transition_name": seed.transition_name,
        "phase": "Phase 3B",
        "batch": "expanded_allowed_transition_corpus",
        "transition_family": seed.transition_family,
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
        "category_transition": transition_code(initial_categories, final_categories),
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
    charge_errors = [float(row["charge_balance_error"]) for row in rows]
    transition_family_counts = Counter(str(row["transition_family"]) for row in rows)
    transition_class_counts = Counter(str(row["transition_class"]) for row in rows)
    layer_transition_counts = Counter(str(row["layer_transition"]) for row in rows)
    route_transition_counts = Counter(str(row["route_transition"]) for row in rows)
    closure_transition_counts = Counter(str(row["closure_transition"]) for row in rows)
    category_transition_counts = Counter(str(row["category_transition"]) for row in rows)

    ids_by_family = defaultdict(list)
    for row in rows:
        ids_by_family[str(row["transition_family"])].append(str(row["transition_id"]))

    return {
        "program": "UNNS Substrate Program",
        "project": "Charge Boundary Routing I",
        "phase": "Phase 3B — Expanded Allowed Transition Corpus",
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "row_count": len(rows),
        "seed_continuity_rows": transition_family_counts.get("seed_continuity", 0),
        "new_expansion_rows": len(rows) - transition_family_counts.get("seed_continuity", 0),
        "charge_conserved_count": sum(1 for row in rows if str(row["charge_conserved"]) == "TRUE"),
        "charge_nonconserved_count": sum(1 for row in rows if str(row["charge_conserved"]) != "TRUE"),
        "max_abs_charge_balance_error": max(abs(x) for x in charge_errors) if charge_errors else None,
        "layer_labels": LAYER_LABELS,
        "transition_family_counts": dict(sorted(transition_family_counts.items())),
        "transition_class_counts": dict(sorted(transition_class_counts.items())),
        "layer_transition_count": len(layer_transition_counts),
        "route_transition_count": len(route_transition_counts),
        "closure_transition_count": len(closure_transition_counts),
        "category_transition_count": len(category_transition_counts),
        "transition_ids_by_family": {
            key: sorted(value) for key, value in sorted(ids_by_family.items())
        },
        "output_files": {
            "canonical_csv": "data/canonical/phase3B_expanded_allowed_transition_corpus.csv",
            "summary_json": "data/derived/phase3B_expanded_allowed_transition_summary.json",
        },
        "notes": [
            "Phase 3B includes the original seven Phase 3 seed transitions plus 31 expanded allowed transitions.",
            "This is a controlled robustness corpus, not a complete particle-decay database.",
            "All rows are intended as allowed charge-preserving transitions.",
            "Phase 2C same-charge route control remains separate.",
        ],
    }


def main() -> int:
    root = project_root_from_script()

    canonical_csv = root / "data" / "canonical" / "phase3B_expanded_allowed_transition_corpus.csv"
    summary_json = root / "data" / "derived" / "phase3B_expanded_allowed_transition_summary.json"

    phase3b_dirs = [
        root / "data" / "canonical",
        root / "data" / "derived",
        root / "ladders" / "phase3B_expanded_transitions",
        root / "ladders" / "phase3B_expanded_transitions" / "one_column",
        root / "ladders" / "phase3B_expanded_transitions" / "diagnostics",
        root / "results" / "struc_perc_i" / "phase3B_expanded_transitions",
        root / "results" / "struc_i" / "phase3B_expanded_transitions",
        root / "outputs" / "reports" / "phase3B_expanded_transitions",
    ]
    for directory in phase3b_dirs:
        directory.mkdir(parents=True, exist_ok=True)

    rows = [build_row(seed) for seed in TRANSITIONS]

    # Hard validation: every expanded-transition row must conserve charge.
    bad_rows = [
        row for row in rows
        if abs(float(row["charge_balance_error"])) > 1e-12
    ]
    if bad_rows:
        ids = [row["transition_id"] for row in bad_rows]
        raise ValueError(f"Charge balance failed for transition id(s): {ids}")

    write_csv(canonical_csv, rows)

    summary = build_summary(rows)
    summary_json.parent.mkdir(parents=True, exist_ok=True)
    summary_json.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")

    print("Phase 3B expanded allowed-transition corpus built.")
    print(f"Rows: {len(rows)}")
    print(f"Seed continuity rows: {summary['seed_continuity_rows']}")
    print(f"New expansion rows: {summary['new_expansion_rows']}")
    print(f"Wrote: {canonical_csv.relative_to(root)}")
    print(f"Wrote: {summary_json.relative_to(root)}")
    print("")
    print("Next step:")
    print("  build_phase3B_expanded_transition_ladders.py")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

UNNS Visual Engine

Substrate Instrument — Operator Laboratory

This folder contains the UNNS Visual Engine, a research-grade interactive instrument for exploring operator-driven recursion in the UNNS Substrate (Unbounded Nested Number Sequences).

The engine is designed as an exploration tool, not a predictive or empirical model.

Contents
unns_visual_engine/
├─ visual_engine_enhanced.html   # Main interactive engine
├─ visual_engine_guide.html      # Standalone user & methodology guide
└─ README.md                     # This file

What This Tool Is

The UNNS Visual Engine is a substrate-level laboratory that allows users to:

Construct recursive structures using UNNS Operators (Φ, Ψ, τ, XII)

Observe invariant diagnostics instead of raw numerical output

Explore τ-flow evolution (temporal recursion)

Visualize collapse, stability, and phase transitions

Export structured JSON logs for analysis or publication

It is intended for:

Conceptual exploration

Structural diagnostics

Demonstration of UNNS principles

Lab-style experimentation

What This Tool Is Not

❌ Not a physics simulator

❌ Not a probabilistic model

❌ Not a numerical predictor

❌ Not an ML system in the statistical sense

All results are UNNS-internal structural diagnostics.

Main Files
visual_engine_enhanced.html

The core interactive instrument.

Features include:

Operator stack control (Φ → Ψ → τ → XII)

Multiple projections:

2D Abstract

τ-Geometry 3D

Collapse View

τ-Flow (true temporal evolution)

Invariant diagnostics:

τ-stability

survival ratio

coherence

commutativity

resonance

Structure classification

Operator trace

JSON export (single run or τ-flow history)

This file is self-contained (HTML + CSS + JS).

visual_engine_guide.html

A standalone guide module, opened from the engine via a button in a separate window/tab.

The guide explains:

Conceptual purpose of the engine

Meaning of each operator

Interpretation of invariants

τ-Flow evolution and phases

Collapse semantics

How to read classifications and diagnostics

How to use exported JSON

The guide is designed to be readable without the engine running.

τ-Flow Evolution (Phase-F)

The engine supports true τ-flow, meaning:

The state evolves over time

Operators are reapplied iteratively

τ acts as a dynamic field

Structure (nodes, edges, topology) can change

Collapse can occur mid-evolution

Evolution is visualized via:

Animated τ-geometry

Structural change in the graph

A multi-invariant evolution timeline

Export Format

The engine can export JSON containing:

Seed and parameters

Operator stack

Invariant diagnostics

Structure classification

τ-flow history (if active)

Phase and event markers

Exports are intended for:

Reproducibility

Comparison between regimes

Chamber logs

External analysis

Ontology vs Exploration

This tool belongs to the exploration layer of the UNNS Substrate.

Ontological definitions (what UNNS is) live elsewhere

This engine explores what happens when operators act

No claims of physical reality are implied

Usage

Open visual_engine_enhanced.html in a modern browser

Adjust Seed (M), Parameter (N), and Node Count

Enable/disable operators

Choose a projection

Optionally start τ-Flow

Inspect invariants and classification

Open the Guide for interpretation

Export JSON if needed

Status

Stable — active development

The engine is considered a UNNS Phase-F exploration instrument.
Further refinements may include:

Local τ-fields

Evolution replay / scrubbing

Additional operator variants

License / Attribution

This tool is part of the UNNS Substrate project.
README — A–B–C ORIENTATION-SENSITIVE BRIDGE

PURPOSE

This stage compares the three cosmological trajectories using signed path
information rather than sorted scalar geometry.

Datasets:

A — classical Friedmann contraction toward the small-a boundary
B — effective LQC contraction, finite bounce, and expansion
C — Planck-anchored Lambda-CDM expansion

SCRIPT

ABC_bridge/tools/
build_orientation_sensitive_abc_bridge.py

OUTPUTS

ABC_bridge/outputs/
ABC_orientation_sensitive_bridge.csv
ABC_orientation_sensitive_bridge_summary.csv
ABC_orientation_sensitive_bridge_manifest.txt

PRIMARY BRIDGE QUANTITIES

- signed Delta ln(a)
- signed H flow
- signed density flow
- signed curvature flow
- signed provisional-margin flow
- margin-flow direction
- distance to boundary or turning surface
- branch identity
- route phase
- rho/rho_c for Dataset B
- x_bounce_distance for Dataset B

RUN

Open a terminal in:

ABC_bridge/tools/

Run:

python build_orientation_sensitive_abc_bridge.py

EXPECTED ROUTING PATTERN

Dataset A:
terminal boundary approach

Dataset B:
approach to a finite turning surface, route reversal, and recession

Dataset C:
expansion away from the early boundary regime

IMPORTANT LIMIT

boundary_margin_candidate remains provisional.

The bridge restores orientation and route topology, but it does not yet freeze
the final shared A/B/C boundary-distance coordinate.

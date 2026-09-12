README — A–B–C ORIENTATION-SENSITIVE BRIDGE V1.1

PURPOSE

Bridge v1.1 replaces heterogeneous surface-distance fields with a shared
dimensionless route coordinate and adds normalized signed-flow summaries.

SHARED ROUTE COORDINATE

The coordinate is based on cumulative absolute logarithmic scale-factor change:

cumulative |Delta ln(a)|

A:
-1 at the outer contraction endpoint
0 at the terminal small-a endpoint

B:
-1 at the outer contraction endpoint
0 at the exact bounce
+1 at the outer expansion endpoint

C:
0 at the early small-a endpoint
+1 at the late expansion endpoint

NORMALIZED SIGNED FLOWS

Each channel is scaled by its dataset-specific Q90 absolute interval magnitude:

normalized = raw / (Q90(|raw|) + |raw|)

The result remains signed and lies within [-1,1].

Channels:

- signed Delta ln(a)
- signed H flow
- signed density flow
- signed curvature flow
- signed provisional-margin flow

SCRIPT

ABC_bridge/tools/
build_orientation_sensitive_abc_bridge_v1_1.py

RUN

python build_orientation_sensitive_abc_bridge_v1_1.py

OUTPUTS

ABC_bridge/outputs/
ABC_orientation_sensitive_bridge_v1_1.csv
ABC_orientation_sensitive_bridge_summary_v1_1.csv
ABC_orientation_sensitive_bridge_manifest_v1_1.txt

INTERPRETIVE LIMIT

The route coordinate is a shared path-intrinsic coordinate. It is not yet a
physical metric distance on the admissibility manifold.

The provisional margin remains diagnostic.

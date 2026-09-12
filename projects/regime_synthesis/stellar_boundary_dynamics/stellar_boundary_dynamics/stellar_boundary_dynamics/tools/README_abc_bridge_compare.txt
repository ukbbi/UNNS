README_abc_bridge_compare.txt
STELLAR_BOUNDARY_DYNAMICS_I
A-B-C Tri-Domain Bridge Comparator

SCRIPT:
tools/abc_bridge_compare.py

PURPOSE:
Compare all three normalization-reviewed v2 vector domains:

A = pre-supernova radial profiles
B = post-collapse light curves
C = post-collapse spectral line evolution

INPUTS:
ABC_bridge/inputs/A_5D_VECTOR_SUMMARY_v2.csv
ABC_bridge/inputs/B_5D_VECTOR_SUMMARY_v2.csv
ABC_bridge/inputs/C_5D_VECTOR_SUMMARY_v2.csv

OUTPUTS:
ABC_bridge/comparisons/ABC_DOMAIN_CENTROID_COMPARISON.csv
ABC_bridge/comparisons/ABC_PAIRWISE_DOMAIN_DISTANCE.csv
ABC_bridge/comparisons/ABC_OBJECT_CHAIN_ALIGNMENT.csv
ABC_bridge/comparisons/ABC_TRANSITION_CHAIN_TEST.csv

ABC_bridge/summaries/ABC_BRIDGE_SUMMARY.csv
ABC_bridge/summaries/ABC_BRIDGE_INTERPRETATION.txt

RECOMMENDED RUN:
Open PowerShell in:

stellar_boundary_dynamics/

Then run:

python tools/abc_bridge_compare.py ABC_bridge/inputs/A_5D_VECTOR_SUMMARY_v2.csv ABC_bridge/inputs/B_5D_VECTOR_SUMMARY_v2.csv ABC_bridge/inputs/C_5D_VECTOR_SUMMARY_v2.csv ABC_bridge

RUN FROM INSIDE ABC_bridge:
python ../tools/abc_bridge_compare.py inputs/A_5D_VECTOR_SUMMARY_v2.csv inputs/B_5D_VECTOR_SUMMARY_v2.csv inputs/C_5D_VECTOR_SUMMARY_v2.csv .

FEATURES COMPARED:
mean_GR
var_GR
anisotropic_persistence_bounded
admissibility_persistence
collapse_onset_radius
kappa_connect_reference
tail_dominance_reference

TESTS:
A-B centroid distance
B-C centroid distance
A-C centroid distance
BC_minus_AB branching strength
SN1993J contact chain:
  A2_20M -> B_SN1993J -> C1_SN1993J

SN2012aw anomaly chain:
  nearest A -> B_SN2012aw -> C2_SN2012aw

INTERPRETATION TARGET:
Decide whether the tri-domain system is better described as:

1. A -> B -> C transition chain
2. A -> B with C branching away
3. linked admissible clusters

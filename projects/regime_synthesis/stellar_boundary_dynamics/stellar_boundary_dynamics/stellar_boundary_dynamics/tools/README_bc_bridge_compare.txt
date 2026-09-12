README_bc_bridge_compare.txt
STELLAR_BOUNDARY_DYNAMICS_I
B–C Bridge Comparator

SCRIPT:
tools/bc_bridge_compare.py

PURPOSE:
Compare Phase B normalization-reviewed v2 vectors against Phase C
normalization-reviewed v2 vectors.

INPUTS:
BC_bridge/inputs/B_5D_VECTOR_SUMMARY_v2.csv
BC_bridge/inputs/C_5D_VECTOR_SUMMARY_v2.csv

OUTPUTS:
BC_bridge/comparisons/BC_VECTOR_PAIRWISE_COMPARISON.csv
BC_bridge/comparisons/BC_DOMAIN_CENTROID_COMPARISON.csv
BC_bridge/comparisons/BC_OBJECT_ALIGNMENT.csv

BC_bridge/summaries/BC_BRIDGE_SUMMARY.csv
BC_bridge/summaries/BC_BRIDGE_INTERPRETATION.txt

RECOMMENDED RUN:
Open PowerShell in:

stellar_boundary_dynamics/

Then run:

python tools/bc_bridge_compare.py BC_bridge/inputs/B_5D_VECTOR_SUMMARY_v2.csv BC_bridge/inputs/C_5D_VECTOR_SUMMARY_v2.csv BC_bridge

RUN FROM INSIDE BC_bridge:
python ../tools/bc_bridge_compare.py inputs/B_5D_VECTOR_SUMMARY_v2.csv inputs/C_5D_VECTOR_SUMMARY_v2.csv .

FEATURES COMPARED:
mean_GR
var_GR
anisotropic_persistence_bounded
admissibility_persistence
collapse_onset_radius
kappa_connect_reference
tail_dominance_reference

METHOD:
The script performs min-max normalization across B+C vectors, then computes:

pairwise B-C Euclidean distance
pairwise B-C Manhattan distance
pairwise cosine similarity
B-domain centroid
C-domain centroid
centroid distance
object-matched alignment for SN1993J and SN2012aw

SPECIAL TESTS:
B_SN1993J ↔ C1_SN1993J
B_SN2012aw ↔ C2_SN2012aw

INTERPRETATION:
This is a structural bridge between two post-collapse observable channels:

B = brightness-response trajectories
C = spectral line-evolution trajectories

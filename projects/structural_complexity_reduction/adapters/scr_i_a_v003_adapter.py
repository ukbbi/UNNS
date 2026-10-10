"""SCR-I-A v003 adapter.

The candidate generator and G1→G4 representation remain exactly the v002/P4 encoding.
v003 changes only the preservation unit from candidate identity to independently clustered target-basin geometry.
"""
from src.scr_i_v003.mechanism import generate_pool
from src.scr_i_v003.gates import evaluate_gates
from src.scr_i_v003.target_oracle import evaluate as evaluate_target
from src.scr_i_v003.basins import cluster_target_basins, preservation
__all__=['generate_pool','evaluate_gates','evaluate_target','cluster_target_basins','preservation']

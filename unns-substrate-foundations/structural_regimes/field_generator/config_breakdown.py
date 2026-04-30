import os
import numpy as np

# α, μ grids
ALPHA_GRID = np.arange(1.0, 4.01, 0.25)
MU_GRID = np.array([1.0])

# STRUC-PERC settings
K_POINTS = 17
K_MIN    = 0.01
K_MAX    = 1.0

# Paths
ENGINE_PATH = "./struc_perc_i_v2_4_0.html"
OUTPUT_DIR  = "./output"

# Dataset (auto-discovery)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data", "base_ladders")

if not os.path.exists(DATA_DIR):
    raise FileNotFoundError(f"Missing folder: {DATA_DIR}")

#  FIX: support BOTH .txt and .csv
files = [
    f for f in os.listdir(DATA_DIR)
    if f.endswith(".txt") or f.endswith(".csv")
]

#  FIX: dynamic mapping (no extension assumptions)
BASE_LADDERS = {
    os.path.splitext(f)[0]: os.path.join(DATA_DIR, f)
    for f in files
}

#  FIX: updated error message
if not BASE_LADDERS:
    raise RuntimeError("No ladder files (.txt or .csv) found in data/base_ladders")
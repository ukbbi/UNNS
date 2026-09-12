import numpy as np
import pandas as pd
import os
import json
import webbrowser
from datetime import datetime

# ==========================================
# CONFIG
# ==========================================

LADDER_FILE = "ladder_energy.txt"
OUTPUT_DIR = "fracture_real_output"

STRUC_PERC_INPUT_DIR = "struc_perc_batch_inputs"

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(STRUC_PERC_INPUT_DIR, exist_ok=True)

# ==========================================
# 1. LOAD LADDER
# ==========================================

ladder = np.loadtxt(LADDER_FILE)

print(f"[INFO] Loaded ladder ({len(ladder)} points)")

# ==========================================
# 2. FRACTURE DETECTION
# ==========================================

gaps = np.diff(ladder)
fracture_idx = np.argmax(np.abs(gaps))
fracture_gap = gaps[fracture_idx]

print("\n=== FRACTURE DETECTION ===")
print(f"Index: {fracture_idx}")
print(f"Gap: {fracture_gap}")

pd.DataFrame({
    "index": np.arange(len(gaps)),
    "gap": gaps
}).to_csv(f"{OUTPUT_DIR}/gaps.csv", index=False)

# ==========================================
# 3. GAP REMOVAL
# ==========================================

ladder_removed = np.delete(ladder, fracture_idx + 1)

np.savetxt(f"{OUTPUT_DIR}/ladder_removed.txt", ladder_removed)

print("[INFO] Saved ladder_removed.txt")

# ==========================================
# 4. SLIDING WINDOWS → REAL STRUC_PERC INPUTS
# ==========================================

WINDOW = max(6, len(ladder)//5)

print("\n=== GENERATING REAL WINDOWS ===")

window_files = []

for i in range(len(ladder) - WINDOW):
    segment = ladder[i:i+WINDOW]

    fname = f"{STRUC_PERC_INPUT_DIR}/window_{i:03d}.txt"
    np.savetxt(fname, segment)

    window_files.append(fname)

print(f"[INFO] Generated {len(window_files)} ladder segments")

# ==========================================
# 5. MASTER BATCH FILE
# ==========================================

batch_list_file = f"{STRUC_PERC_INPUT_DIR}/ALL_WINDOWS.txt"

with open(batch_list_file, "w") as f:
    for wf in window_files:
        f.write(wf + "\n")

print(f"[INFO] Batch file created: {batch_list_file}")

# ==========================================
# 6. SUMMARY
# ==========================================

summary = {
    "ladder_size": int(len(ladder)),
    "fracture_index": int(fracture_idx),
    "fracture_gap": float(fracture_gap),
    "window_size": int(WINDOW),
    "num_windows": int(len(window_files)),
    "timestamp": datetime.now().isoformat()
}

with open(f"{OUTPUT_DIR}/summary.json", "w") as f:
    json.dump(summary, f, indent=4)

print("\n=== READY FOR REAL κ ANALYSIS ===")

print("\nNEXT STEP:")
print("1. Open STRUC_PERC")
print("2. Go to BATCH MODE")
print("3. Drop ALL files from:")
print(f"   {STRUC_PERC_INPUT_DIR}")
print("4. Click RUN BATCH")
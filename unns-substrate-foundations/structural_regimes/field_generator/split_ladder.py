# split_ladder.py

import os
import csv

SRC_DIR = "data/base_ladders"

def load_values(path):
    values = []
    with open(path) as f:
        reader = csv.reader(f)
        for row in reader:
            for v in row:
                try:
                    values.append(float(v))
                except:
                    pass
    return sorted(values)

def save(path, values):
    with open(path, "w") as f:
        f.write("value\n")
        for v in values:
            f.write(f"{v}\n")

for fname in os.listdir(SRC_DIR):
    if not fname.endswith(".csv"):
        continue

    full_path = os.path.join(SRC_DIR, fname)
    values = load_values(full_path)

    if len(values) < 10:
        continue  # skip tiny ladders

    # 🔥 split point
    mid = len(values) // 2

    low = values[:mid]
    high = values[mid:]

    base = fname.replace(".csv", "")

    save(os.path.join(SRC_DIR, base + "_low.csv"), low)
    save(os.path.join(SRC_DIR, base + "_high.csv"), high)

    # 🔥 stride variants
    save(os.path.join(SRC_DIR, base + "_stride2.csv"), values[::2])
    save(os.path.join(SRC_DIR, base + "_stride3.csv"), values[::3])

    print(f"Processed: {fname}")

print("DONE")
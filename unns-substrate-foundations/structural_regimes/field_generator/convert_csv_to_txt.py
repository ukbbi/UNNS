import os
import csv

INPUT_DIR = "data/base_ladders"
OUTPUT_DIR = "data/base_ladders_txt"

os.makedirs(OUTPUT_DIR, exist_ok=True)

def convert_file(filepath):
    values = []

    with open(filepath, "r") as f:
        reader = csv.reader(f)
        for row in reader:
            for v in row:
                if v.strip() != "":
                    values.append(float(v))

    # sort is optional but recommended for ladders
    values = sorted(values)

    # write as space-separated txt
    out_name = os.path.basename(filepath).replace(".csv", ".txt")
    out_path = os.path.join(OUTPUT_DIR, out_name)

    with open(out_path, "w") as f:
        f.write(" ".join(str(v) for v in values))

    print(f"✔ Converted: {out_name}")


for file in os.listdir(INPUT_DIR):
    if file.endswith(".csv"):
        convert_file(os.path.join(INPUT_DIR, file))
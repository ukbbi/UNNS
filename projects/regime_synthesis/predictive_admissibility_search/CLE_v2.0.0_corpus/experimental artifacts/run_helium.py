from cle import CLEvaluator
from cle.adapters.csv_adapter import CsvAdapter

import json
import csv
import os

# ---------------------------------------------------
# OUTPUT DIRECTORY
# ---------------------------------------------------

output_dir = "CLE_OUTPUT/helium"

os.makedirs(output_dir, exist_ok=True)

# ---------------------------------------------------
# LOAD ENCODING FAMILY
# ---------------------------------------------------

adapter = CsvAdapter()

family = [

    # ------------------------------------------------
    # QM-I FAMILY
    # ------------------------------------------------

    adapter.load(
        "CLE_PILOT_I/helium/qmi/helium_spectrum_QM1.csv",
        column=0,
        has_header=True,
        encoding_id="qmi_spectrum",
        system_id="helium",
        domain="atomic",
    ),

    adapter.load(
        "CLE_PILOT_I/helium/qmi/helium_gap_structure_QM1.csv",
        column=0,
        has_header=True,
        encoding_id="qmi_gap",
        system_id="helium",
        domain="atomic",
    ),

    adapter.load(
        "CLE_PILOT_I/helium/qmi/helium_QM1_preprocessed.csv",
        column=0,
        has_header=True,
        encoding_id="qmi_preprocessed",
        system_id="helium",
        domain="atomic",
    ),

    # ------------------------------------------------
    # ZEEMAN FAMILY
    # ------------------------------------------------

    adapter.load(
        "CLE_PILOT_I/helium/zeeman/helium_zeeman_ladder.csv",
        column=0,
        has_header=True,
        encoding_id="zeeman",
        system_id="helium",
        domain="atomic",
    ),

    adapter.load(
        "CLE_PILOT_I/helium/zeeman/helium_singlet_zeeman_ladder.csv",
        column=0,
        has_header=True,
        encoding_id="zeeman_singlet",
        system_id="helium",
        domain="atomic",
    ),

    adapter.load(
        "CLE_PILOT_I/helium/zeeman/helium_triplet_zeeman_ladder.csv",
        column=0,
        has_header=True,
        encoding_id="zeeman_triplet",
        system_id="helium",
        domain="atomic",
    ),
]

# ---------------------------------------------------
# RUN CLE
# ---------------------------------------------------

ev = CLEvaluator(verbose=True)

result = ev.evaluate(family)

# ---------------------------------------------------
# PRINT RESULTS
# ---------------------------------------------------

print("\n===================================")
print("HELIUM CLT STRESS TEST RESULTS")
print("===================================\n")

print("Canonical encoding:")
print(result.canonical_encoding_id)

print("\nRankings:\n")

for r in result.results:

    print(
        f"Rank {r.rank:>2} | "
        f"{r.encoding_id:<20} | "
        f"C(L)={r.c_score:.4f}"
    )

# ---------------------------------------------------
# JSON EXPORT
# ---------------------------------------------------

json_data = {
    "canonical_encoding": result.canonical_encoding_id,
    "results": []
}

for r in result.results:

    json_data["results"].append({
        "rank": r.rank,
        "encoding_id": r.encoding_id,
        "c_score": r.c_score,
    })

json_path = f"{output_dir}/helium_results.json"

with open(json_path, "w", encoding="utf-8") as f:
    json.dump(json_data, f, indent=2)

# ---------------------------------------------------
# CSV EXPORT
# ---------------------------------------------------

csv_path = f"{output_dir}/helium_results.csv"

with open(csv_path, "w", newline="", encoding="utf-8") as f:

    writer = csv.writer(f)

    writer.writerow([
        "rank",
        "encoding_id",
        "c_score"
    ])

    for r in result.results:

        writer.writerow([
            r.rank,
            r.encoding_id,
            r.c_score
        ])

# ---------------------------------------------------
# DONE
# ---------------------------------------------------

print("\nExports written:")
print(json_path)
print(csv_path)

print("\nDone.")
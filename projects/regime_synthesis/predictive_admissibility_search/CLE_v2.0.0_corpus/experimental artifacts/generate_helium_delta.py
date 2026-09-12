import pandas as pd
from pathlib import Path

# ---------------------------------------------------
# INPUT FILES
# ---------------------------------------------------

files = {

    "delta_qmi_spectrum.csv":
        "CLE_PILOT_I/helium/qmi/helium_spectrum_QM1.csv",

    "delta_qmi_gap.csv":
        "CLE_PILOT_I/helium/qmi/helium_gap_structure_QM1.csv",

    "delta_qmi_preprocessed.csv":
        "CLE_PILOT_I/helium/qmi/helium_QM1_preprocessed.csv",

    "delta_zeeman.csv":
        "CLE_PILOT_I/helium/zeeman/helium_zeeman_ladder.csv",

    "delta_zeeman_singlet.csv":
        "CLE_PILOT_I/helium/zeeman/helium_singlet_zeeman_ladder.csv",

    "delta_zeeman_triplet.csv":
        "CLE_PILOT_I/helium/zeeman/helium_triplet_zeeman_ladder.csv",
}

# ---------------------------------------------------
# OUTPUT DIRECTORY
# ---------------------------------------------------

output_dir = Path("CLE_PILOT_I/helium/delta")
output_dir.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------
# GENERATE DELTA LADDERS
# ---------------------------------------------------

for output_name, source_path in files.items():

    print(f"\nProcessing: {source_path}")

    df = pd.read_csv(source_path)

    # ---------------------------------------------------
    # USE FIRST NUMERIC COLUMN
    # ---------------------------------------------------

    series = df.select_dtypes(include="number").iloc[:, 0]

    # ---------------------------------------------------
    # CUMULATIVE Δ-LIFT
    # ---------------------------------------------------

    raw_delta = series.diff().dropna()

    # preserve ordering / topology
    delta = raw_delta.cumsum()

    # ---------------------------------------------------
    # EXPORT
    # ---------------------------------------------------

    out_df = pd.DataFrame({
        "delta": delta
    })

    output_path = output_dir / output_name

    out_df.to_csv(output_path, index=False)

    print(f"Saved: {output_path}")

print("\nDone.")
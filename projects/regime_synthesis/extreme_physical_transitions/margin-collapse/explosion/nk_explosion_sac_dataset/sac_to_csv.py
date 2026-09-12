from obspy import read
import pandas as pd
import sys
import os
import glob

# ------------------------------------------------------------
# Usage
# ------------------------------------------------------------
#
# Single file:
# python sac_to_csv.py file.SAC
#
# Whole folder:
# python sac_to_csv.py folder_name
#
# ------------------------------------------------------------

if len(sys.argv) < 2:
    print("Usage:")
    print("  python sac_to_csv.py <file.SAC>")
    print("  python sac_to_csv.py <folder>")
    sys.exit(1)

target = sys.argv[1]

# ------------------------------------------------------------
# SINGLE FILE MODE
# ------------------------------------------------------------

if os.path.isfile(target):

    files = [target]

# ------------------------------------------------------------
# DIRECTORY MODE
# ------------------------------------------------------------

elif os.path.isdir(target):

    files = glob.glob(os.path.join(target, "*.SAC"))
    files += glob.glob(os.path.join(target, "*.sac"))

    if len(files) == 0:
        print("No SAC files found in folder:", target)
        sys.exit(1)

else:
    print("Path not found:", target)
    sys.exit(1)

# ------------------------------------------------------------
# PROCESS LOOP
# ------------------------------------------------------------

print(f"Found {len(files)} SAC files")

success = 0
failed = 0

for file in files:

    try:

        st = read(file)
        tr = st[0]

        time = tr.times()
        amp = tr.data.astype(float)

        df = pd.DataFrame({
            "time": time,
            "amplitude": amp
        })

        out = os.path.splitext(file)[0] + ".csv"

        df.to_csv(out, index=False)

        print("Saved:", out)

        success += 1

    except Exception as e:

        print("FAILED:", file)
        print("Reason:", e)

        failed += 1

# ------------------------------------------------------------
# SUMMARY
# ------------------------------------------------------------

print("\nDONE")
print("Successful:", success)
print("Failed:", failed)
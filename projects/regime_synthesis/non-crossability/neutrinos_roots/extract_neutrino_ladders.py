import uproot
import numpy as np
import os

# ============================================================
# OUTPUT FOLDERS
# ============================================================

os.makedirs("raw", exist_ok=True)

# ============================================================
# NORMALIZATION
# ============================================================

def normalize(x):

    x = np.asarray(x, dtype=float)

    x = x[np.isfinite(x)]

    if len(x) == 0:
        return x

    xmin = np.min(x)
    xmax = np.max(x)

    if xmax - xmin == 0:
        return x

    return (x - xmin) / (xmax - xmin)

# ============================================================
# SAVE LADDER
# ============================================================

def save_ladder(name, data):

    data = np.sort(normalize(data))

    path = os.path.join("raw", name)

    np.savetxt(path, data)

    print(f"[SAVED] {path}  ({len(data)} values)")

# ============================================================
# ENERGY SPECTRUM
# ============================================================

print("\n=== ENERGY SPECTRUM ===")

f = uproot.open("EnerySpectrum.root")

tree = f["tree"]

for branch in tree.keys():

    print("Extracting:", branch)

    arr = tree[branch].array(library="np")

    save_ladder(
        f"L_{branch}.txt",
        arr
    )

# ============================================================
# EVENT TOPOLOGY
# ============================================================

print("\n=== EVENT TOPOLOGY ===")

f = uproot.open("evt.root")

for tree_name in f.keys():

    tree = f[tree_name]

    print("\nTREE:", tree_name)

    for branch in tree.keys():

        print("Extracting:", branch)

        arr = tree[branch].array(library="np")

        save_ladder(
            f"L_{tree_name}_{branch}.txt",
            arr
        )

# ============================================================
# FIB GEOMETRY
# ============================================================

print("\n=== FIB GEOMETRY ===")

f = uproot.open("Fib_CDPMT.root")

tree = f["tree"]

for branch in tree.keys():

    print("Extracting:", branch)

    arr = tree[branch].array(library="np")

    save_ladder(
        f"L_Fib_{branch}.txt",
        arr
    )

# ============================================================
# VARIABLE SPACE
# ============================================================

print("\n=== VARIABLE SPACE ===")

f = uproot.open("variable.root")

for tree_name in f.keys():

    obj = f[tree_name]

    if not hasattr(obj, "keys"):
        continue

    print("\nTREE:", tree_name)

    for branch in obj.keys():

        print("Extracting:", branch)

        try:

            arr = obj[branch].array(library="np")

            save_ladder(
                f"L_{tree_name}_{branch}.txt",
                arr
            )

        except Exception as e:

            print("Skipped:", branch, e)

# ============================================================
# TMVA
# ============================================================

print("\n=== TMVA ===")

f = uproot.open("TMVA_performance.root")

for tree_name in f.keys():

    obj = f[tree_name]

    if not hasattr(obj, "keys"):
        continue

    print("\nTREE:", tree_name)

    for branch in obj.keys():

        print("Extracting:", branch)

        try:

            values = obj[branch].values()

            save_ladder(
                f"L_TMVA_{branch}.txt",
                values
            )

        except Exception:

            try:

                arr = obj[branch].array(library="np")

                save_ladder(
                    f"L_TMVA_{branch}.txt",
                    arr
                )

            except Exception as e:

                print("Skipped:", branch, e)

# ============================================================
# DEEP LEARNING
# ============================================================

print("\n=== DEEP LEARNING ===")

f = uproot.open("deepL_performance.root")

for tree_name in f.keys():

    obj = f[tree_name]

    if not hasattr(obj, "keys"):
        continue

    print("\nTREE:", tree_name)

    for branch in obj.keys():

        print("Extracting:", branch)

        try:

            values = obj[branch].values()

            save_ladder(
                f"L_deepL_{branch}.txt",
                values
            )

        except Exception:

            try:

                arr = obj[branch].array(library="np")

                save_ladder(
                    f"L_deepL_{branch}.txt",
                    arr
                )

            except Exception as e:

                print("Skipped:", branch, e)

print("\nDONE.")
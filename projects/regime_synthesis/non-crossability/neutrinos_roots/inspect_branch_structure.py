import uproot
import glob

root_files = glob.glob("*.root")

for fname in root_files:

    print("\n" + "=" * 70)
    print("FILE:", fname)

    try:
        f = uproot.open(fname)

        print("\nOBJECTS:")

        for k in f.keys():
            print(" ", k)

        for k in f.keys():

            obj = f[k]

            if hasattr(obj, "keys"):

                print("\nTREE:", k)
                print("BRANCHES:\n")

                for branch in obj.keys():
                    print(" ", branch)

    except Exception as e:
        print("ERROR:", e)
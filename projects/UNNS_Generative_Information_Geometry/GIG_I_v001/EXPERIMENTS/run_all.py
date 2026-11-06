"""Run E1-E4 and write RESULTS/results.json  (python run_all.py);  python run_all.py --extended  writes RESULTS/results_extended.json (E4 only)."""
import json, sys, time, os, platform
import _path
import E1_72, E2_growth, E3_content, E4_topology


def main():
    ext = "--extended" in sys.argv
    t0 = time.time()
    out = {"release": "GIG_I_v001", "python": platform.python_version(), "deterministic": True}
    if ext:
        out["E4_extended"] = E4_topology.run(extended=True)
        name = "results_extended.json"
    else:
        out["E1"] = E1_72.run()
        out["E2"] = E2_growth.run(7)
        out["E3"] = E3_content.run()
        out["E4"] = E4_topology.run(False)
        name = "results.json"
    out["seconds"] = round(time.time() - t0, 1)
    os.makedirs(_path.RESULTS, exist_ok=True)
    with open(os.path.join(_path.RESULTS, name), "w") as f:
        json.dump(out, f, indent=1, default=str, sort_keys=True)
    print("wrote", name, "in", out["seconds"], "s")


if __name__ == "__main__":
    main()

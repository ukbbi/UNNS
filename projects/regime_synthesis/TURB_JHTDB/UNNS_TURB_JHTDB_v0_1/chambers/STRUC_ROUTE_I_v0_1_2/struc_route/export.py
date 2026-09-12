from __future__ import annotations
from pathlib import Path
import json
import zipfile
import pandas as pd

def write_json(path: Path, obj):
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

def export_ladders(run_dir: Path, nodes: pd.DataFrame, squares: pd.DataFrame):
    ladder_dir = run_dir / "_ladders"
    ladder_dir.mkdir(exist_ok=True)

    candidates = [
        ("scale_persistence", "scale_persistence"),
        ("time_persistence", "time_persistence"),
        ("scale_entropy", "scale_entropy"),
        ("time_entropy", "time_entropy"),
        ("scale_branching", "scale_branching"),
        ("time_branching", "time_branching"),
        ("scale_merging", "scale_merging"),
        ("time_merging", "time_merging"),
        ("scale_conservation", "scale_conservation"),
        ("time_conservation", "time_conservation"),
    ]
    written = []
    for filename, col in candidates:
        if col not in nodes.columns:
            continue
        vals = pd.to_numeric(nodes[col], errors="coerce").dropna().sort_values()
        if len(vals) < 3:
            continue
        p = ladder_dir / f"{filename}.csv"
        pd.DataFrame({"value": vals.to_numpy()}).to_csv(p, index=False)
        written.append(p)

    if len(squares) and "mean_defect" in squares.columns:
        vals = pd.to_numeric(squares["mean_defect"], errors="coerce").dropna().sort_values()
        if len(vals) >= 3:
            p = ladder_dir / "stitch_defect.csv"
            pd.DataFrame({"value": vals.to_numpy()}).to_csv(p, index=False)
            written.append(p)

    readme = ladder_dir / "README.txt"
    readme.write_text(
        "STRUC-ROUTE-I chamber-array descendants.\n"
        "Each CSV is a scalar route-derived sequence sorted ascending for later\n"
        "explicit adaptation to canonical STRUC-I / STRUC-PERC-I.\n"
        "These files are derived views, not the primary route graph.\n",
        encoding="utf-8"
    )
    written.append(readme)

    zpath = run_dir / "LADDERS.zip"
    with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED) as zf:
        for p in written:
            zf.write(p, p.name)

    for p in written:
        p.unlink(missing_ok=True)
    ladder_dir.rmdir()
    return zpath

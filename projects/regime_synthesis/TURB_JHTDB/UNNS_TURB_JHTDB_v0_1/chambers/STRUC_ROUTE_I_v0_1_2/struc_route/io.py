from __future__ import annotations
from pathlib import Path
import json
import pandas as pd

OBJECT_REQUIRED = [
    "node_id", "time_idx", "time_value", "scale_idx", "scale_value",
    "object_id", "size"
]
REL_REQUIRED = ["src_id", "dst_id", "axis"]

def _read_table(path: Path) -> pd.DataFrame:
    suf = path.suffix.lower()
    if suf == ".csv":
        return pd.read_csv(path)
    if suf in (".parquet", ".pq"):
        return pd.read_parquet(path)
    raise ValueError(f"Unsupported table format: {path}")

def _find_one(folder: Path, stem: str, optional=False):
    candidates = []
    for ext in (".parquet", ".pq", ".csv"):
        p = folder / f"{stem}{ext}"
        if p.exists():
            candidates.append(p)
    if len(candidates) > 1:
        raise ValueError(f"Multiple {stem} tables found: {candidates}")
    if not candidates:
        if optional:
            return None
        raise FileNotFoundError(f"Missing {stem}.csv/parquet in {folder}")
    return candidates[0]

def load_project(folder: str | Path):
    folder = Path(folder)
    manifest_path = folder / "manifest.json"
    if not manifest_path.exists():
        raise FileNotFoundError(f"Missing manifest.json in {folder}")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    objects_path = _find_one(folder, "objects")
    relations_path = _find_one(folder, "relations")
    families_path = _find_one(folder, "families", optional=True)

    objects = _read_table(objects_path)
    relations = _read_table(relations_path)
    families = _read_table(families_path) if families_path else None

    return manifest, objects, relations, families, {
        "manifest": str(manifest_path),
        "objects": str(objects_path),
        "relations": str(relations_path),
        "families": str(families_path) if families_path else None,
    }

def normalize_and_validate(manifest, objects, relations, families=None):
    objects = objects.copy()
    relations = relations.copy()

    missing = [c for c in OBJECT_REQUIRED if c not in objects.columns]
    if missing:
        raise ValueError(f"objects table missing required columns: {missing}")
    missing = [c for c in REL_REQUIRED if c not in relations.columns]
    if missing:
        raise ValueError(f"relations table missing required columns: {missing}")

    objects["node_id"] = objects["node_id"].astype(str)
    objects["object_id"] = objects["object_id"].astype(str)
    relations["src_id"] = relations["src_id"].astype(str)
    relations["dst_id"] = relations["dst_id"].astype(str)
    relations["axis"] = relations["axis"].astype(str).str.lower().str.strip()

    for c in ("time_idx", "scale_idx"):
        objects[c] = pd.to_numeric(objects[c], errors="raise").astype(int)
    for c in ("time_value", "scale_value", "size"):
        objects[c] = pd.to_numeric(objects[c], errors="raise")

    if objects["node_id"].duplicated().any():
        dup = objects.loc[objects["node_id"].duplicated(), "node_id"].head().tolist()
        raise ValueError(f"Duplicate node_id values: {dup}")

    bad_axes = sorted(set(relations["axis"]) - {"scale", "time"})
    if bad_axes:
        raise ValueError(f"Invalid relation axis values: {bad_axes}")

    node_ids = set(objects["node_id"])
    missing_src = sorted(set(relations["src_id"]) - node_ids)
    missing_dst = sorted(set(relations["dst_id"]) - node_ids)
    if missing_src or missing_dst:
        raise ValueError(
            f"Relations reference missing nodes. src examples={missing_src[:5]}, "
            f"dst examples={missing_dst[:5]}"
        )

    if families is not None:
        families = families.copy()
        if "node_id" not in families.columns or "family_id" not in families.columns:
            raise ValueError("families table requires node_id,family_id")
        families["node_id"] = families["node_id"].astype(str)
        fam_map = families.drop_duplicates("node_id").set_index("node_id")["family_id"]
        objects["family_id"] = objects["node_id"].map(fam_map).fillna(
            objects["family_id"] if "family_id" in objects.columns else pd.NA
        )

    idx = objects.set_index("node_id")
    strict = bool(manifest.get("strict_adjacent", True))
    bad = []
    for i, e in relations.iterrows():
        a = idx.loc[e["src_id"]]
        b = idx.loc[e["dst_id"]]
        if e["axis"] == "scale":
            ok = (b["scale_idx"] - a["scale_idx"] == 1) and (b["time_idx"] == a["time_idx"])
        else:
            ok = (b["time_idx"] - a["time_idx"] == 1) and (b["scale_idx"] == a["scale_idx"])
        if not ok:
            bad.append(int(i))
    if bad and strict:
        raise ValueError(
            f"{len(bad)} relations violate adjacent-forward layer rules; "
            f"row examples={bad[:10]}"
        )
    if bad:
        relations = relations.drop(index=bad).copy()

    return objects.reset_index(drop=True), relations.reset_index(drop=True), families

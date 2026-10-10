from __future__ import annotations
import json
from pathlib import Path
from typing import Iterable, Mapping

from scr_iii.engine_common import scr_iii_root, project_root, sha256_file, safe_write_json, stable_int

ENGINE_VERSION_V002 = "SCR_III_ENGINE_v002"
PREREG_V002 = "SCR_III_PREREG_v002"
Q_LEVELS_V002 = (0.0, 0.1, 0.2, 0.3, 0.4)
SIGMA_LEVELS_V002 = (0.8, 0.9)
PRIMARY_DEPTHS_V002 = (14, 16, 18)
AUDIT_DEPTH_V002 = 14
MAX_ATTEMPTS_V002 = 64
N_DOSE_MIN_V002 = 6
N_ACC_MIN_V002 = 21


def prereg_root_v002() -> Path:
    return scr_iii_root() / PREREG_V002


def output_root_v002() -> Path:
    return scr_iii_root() / "output" / "v002"


def load_seeds_v002() -> dict:
    return json.loads((prereg_root_v002() / "SEEDS_v002.json").read_text(encoding="utf-8"))


def load_config_v002() -> dict:
    return json.loads((prereg_root_v002() / "config" / "prereg_v002.json").read_text(encoding="utf-8"))


def dose_delivered_family(rows: Iterable[Mapping]) -> bool:
    vals = []
    for r in rows:
        c = r.get("coverage_C")
        if c is not None:
            vals.append(float(c))
    return bool(vals) and max(vals) > 0.0


def accepted_seed_order(primary: Mapping, depth: int) -> list[int]:
    """Return accepted family seeds in frozen primary seed order."""
    seeds = load_seeds_v002()["primary"][f"depth_{int(depth)}"]
    accepted = set()
    for r in primary.get("main_cells", []):
        if int(r["depth"]) == int(depth):
            accepted.add(int(r["seed"]))
    return [int(s) for s in seeds if int(s) in accepted]

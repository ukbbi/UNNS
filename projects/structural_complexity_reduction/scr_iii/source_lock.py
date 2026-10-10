from __future__ import annotations
import json
from pathlib import Path
from scr_iii.engine_common import project_root, scr_iii_root, sha256_file


def verify_source_lock():
    cfg=json.loads((scr_iii_root()/"SCR_III_PREREG_v001"/"config"/"prereg_v001.json").read_text(encoding="utf-8"))
    scrii=project_root()/"scr_ii"
    rows=[]; ok=True
    for rel,expected in {**cfg["source_lock"],**cfg.get("implementation_dependency_lock",{})}.items():
        p=scrii/rel
        actual=sha256_file(p) if p.exists() else None
        match=actual==expected
        rows.append({"file":rel,"expected":expected,"actual":actual,"match":match})
        ok=ok and match
    return {"pass":ok,"files":rows}


def verify_design_freeze():
    """Verify the ratified top-level design bundle against SHA256SUMS_SCR_III_v001.txt."""
    root = project_root()
    manifest = root / "SHA256SUMS_SCR_III_v001.txt"
    if not manifest.exists():
        return {"pass": False, "reason": "missing SHA256SUMS_SCR_III_v001.txt", "files": []}
    mapping = {
        "SCR_III_COUPLING_SPEC_v001.md": root / "SCR_III_COUPLING_SPEC_v001.md",
        "SCR_III_STRUCTURE_v001.md": root / "SCR_III_STRUCTURE_v001.md",
        "SCR_III_PREREG_v001.md": scr_iii_root() / "SCR_III_PREREG_v001" / "SCR_III_PREREG_v001.md",
        "SEEDS_v001.json": scr_iii_root() / "SCR_III_PREREG_v001" / "SEEDS_v001.json",
    }
    rows=[]; ok=True
    for line in manifest.read_text(encoding="utf-8").splitlines():
        if not line.strip(): continue
        expected,name=line.split(None,1); name=name.strip(); p=mapping.get(name)
        actual=sha256_file(p) if p and p.exists() else None
        match=actual==expected
        rows.append({"file":name,"expected":expected,"actual":actual,"match":match})
        ok = ok and match
    return {"pass":ok,"files":rows}

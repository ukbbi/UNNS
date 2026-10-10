from __future__ import annotations
import sys
from pathlib import Path


def project_root() -> Path:
    return Path(__file__).resolve().parents[1]


def scr_ii_root() -> Path:
    return project_root() / "scr_ii"


def install_scr_ii_path() -> Path:
    root = scr_ii_root()
    if not root.is_dir():
        raise RuntimeError(f"Missing frozen scr_ii directory: {root}")
    s = str(root)
    if s not in sys.path:
        sys.path.insert(0, s)
    return root

from __future__ import annotations
import csv, io, json, zipfile, hashlib
from pathlib import Path
import numpy as np

class Bundle:
    def __init__(self, path):
        self.path = Path(path).resolve()
        if not self.path.exists():
            raise FileNotFoundError(self.path)
        self.is_zip = self.path.is_file() and self.path.suffix.lower() == ".zip"

    def _find(self, suffix):
        if self.is_zip:
            with zipfile.ZipFile(self.path, "r") as zf:
                names = [n for n in zf.namelist() if n.replace("\\","/").endswith(suffix)]
            if len(names) != 1:
                return None
            return names[0]
        p = self.path / suffix
        if p.exists():
            return p
        matches = [m for m in self.path.rglob(Path(suffix).name)
                   if str(m).replace("\\","/").endswith(suffix)]
        return matches[0] if len(matches) == 1 else None

    def exists(self, suffix):
        return self._find(suffix) is not None

    def read_bytes(self, suffix):
        found = self._find(suffix)
        if found is None:
            raise FileNotFoundError(suffix)
        if self.is_zip:
            with zipfile.ZipFile(self.path, "r") as zf:
                return zf.read(found)
        return Path(found).read_bytes()

    def read_json(self, suffix):
        return json.loads(self.read_bytes(suffix).decode("utf-8-sig"))

    def read_csv(self, suffix):
        text = self.read_bytes(suffix).decode("utf-8-sig")
        return list(csv.DictReader(io.StringIO(text)))

    def evidence_hash(self):
        h = hashlib.sha256()
        if self.is_zip:
            with zipfile.ZipFile(self.path, "r") as zf:
                names = sorted(n for n in zf.namelist() if not n.endswith("/"))
                for n in names:
                    logical = n.replace("\\","/")
                    if logical.endswith("ground_truth.json"):
                        continue
                    data = zf.read(n)
                    h.update(logical.encode("utf-8")); h.update(b"\0")
                    h.update(hashlib.sha256(data).digest())
        else:
            files = sorted(p for p in self.path.rglob("*") if p.is_file())
            for p in files:
                logical = str(p.relative_to(self.path)).replace("\\","/")
                if logical.endswith("ground_truth.json"):
                    continue
                data = p.read_bytes()
                h.update(logical.encode("utf-8")); h.update(b"\0")
                h.update(hashlib.sha256(data).digest())
        return h.hexdigest()

def matrix_csv(rows):
    if not rows:
        raise ValueError("empty CSV")
    cols = list(rows[0].keys())
    if len(cols) < 2:
        raise ValueError("trajectory CSV needs time plus at least one coordinate")
    tcol = cols[0]
    data_cols = cols[1:]
    t = np.asarray([float(r[tcol]) for r in rows], dtype=float)
    X = np.asarray([[float(r[c]) for c in data_cols] for r in rows], dtype=float)
    return t, X, data_cols

def long_values(rows, group_key, value_key):
    groups = {}
    for r in rows:
        g = float(r[group_key])
        groups.setdefault(g, []).append(float(r[value_key]))
    return {g: np.asarray(v, dtype=float) for g,v in groups.items()}

def status_entry(status, basis, metrics=None, missing=None, reasons=None):
    return {
        "status": status,
        "basis": basis,
        "metrics": metrics or {},
        "missing": missing or [],
        "reasons": reasons or [],
    }

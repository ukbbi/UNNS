from __future__ import annotations

import csv
import io
import json
import zipfile
from pathlib import Path


class Artifact:
    def __init__(self, path: str | Path):
        self.path = Path(path).resolve()
        if not self.path.exists():
            raise FileNotFoundError(self.path)
        self.is_zip = self.path.is_file() and self.path.suffix.lower() == ".zip"

    def _member(self, suffix: str) -> str:
        with zipfile.ZipFile(self.path, "r") as zf:
            names = [n for n in zf.namelist() if n.endswith(suffix)]
        if len(names) != 1:
            raise FileNotFoundError(
                f"{self.path}: expected one member ending {suffix}, found {len(names)}"
            )
        return names[0]

    def read_bytes(self, suffix: str) -> bytes:
        if self.is_zip:
            with zipfile.ZipFile(self.path, "r") as zf:
                return zf.read(self._member(suffix))
        p = self.path / suffix
        if not p.exists():
            matches = [
                m for m in self.path.rglob(Path(suffix).name)
                if str(m).replace("\\", "/").endswith(suffix)
            ]
            if len(matches) != 1:
                raise FileNotFoundError(p)
            p = matches[0]
        return p.read_bytes()

    def read_json(self, suffix: str) -> dict:
        return json.loads(self.read_bytes(suffix).decode("utf-8"))

    def read_csv(self, suffix: str) -> list[dict]:
        return list(csv.DictReader(io.StringIO(
            self.read_bytes(suffix).decode("utf-8")
        )))

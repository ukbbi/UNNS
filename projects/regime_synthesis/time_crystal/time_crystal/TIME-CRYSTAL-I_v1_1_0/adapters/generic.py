from __future__ import annotations

import json
from pathlib import Path


def load_candidate(path: str | Path) -> dict:
    """
    Load a chamber-native candidate record.

    TIME-CRYSTAL-I v1.0.0 deliberately does not guess sector status from an
    arbitrary raw time series. Raw-data conversion belongs in a domain adapter.
    """
    return json.loads(Path(path).read_text(encoding="utf-8"))

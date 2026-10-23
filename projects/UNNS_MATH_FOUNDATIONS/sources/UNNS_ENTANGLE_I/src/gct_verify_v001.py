from __future__ import annotations

import json
from pathlib import Path

from .gct_generator_v001 import run_gct

OUTPUT = Path(__file__).resolve().parents[1] / "output" / "GCT_RESULTS_v001.json"

def main() -> None:
    data = run_gct()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(data, indent=2, sort_keys=True), encoding="utf-8")
    print(f"WROTE {OUTPUT}")
    print(data["scientific_verdict"])

if __name__ == "__main__":
    main()

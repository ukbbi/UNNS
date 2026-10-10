from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.scr_i_v003 import runner  # noqa: E402
from src.scr_i_v003.safe_io import safe_dump  # noqa: E402

# Windows-safe persistence is now canonical for v003.
runner.dump = safe_dump


def primary_complete() -> bool:
    progress = ROOT / "output" / "RUN_PROGRESS_v003.json"
    result = ROOT / "output" / "PRIMARY_RESULT_v003.json"
    if not (progress.is_file() and result.is_file()):
        return False
    try:
        state = json.loads(progress.read_text(encoding="utf-8"))
        return state.get("status") == "COMPLETE" and int(state.get("completed_cells", 0)) == int(state.get("total_cells", -1)) == 15
    except Exception:
        return False


if __name__ == "__main__":
    if primary_complete():
        print("SCR-I-A v003 primary run is already COMPLETE (15/15). Rerun blocked to preserve the frozen primary result.")
        raise SystemExit(0)
    try:
        records = runner.run(ROOT)
        print(f"SCR-I-A v003 primary run complete: {len(records)} cells.")
        raise SystemExit(0)
    except KeyboardInterrupt:
        print("\nSCR-I-A v003 interrupted. Completed cells/null replicates remain checkpointed; run the same batch file again to resume.")
        raise SystemExit(130)

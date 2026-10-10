from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from src.scr_i_v003.safe_io import safe_dump


class SafeIOTests(unittest.TestCase):
    def test_repeated_checkpoint_replacement(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "checkpoint.json"
            for i in range(250):
                safe_dump(p, {"generation": i, "completed": list(range(i % 17))})
                got = json.loads(p.read_text(encoding="utf-8"))
                self.assertEqual(got["generation"], i)

    def test_nested_parent_creation(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "a" / "b" / "progress.json"
            safe_dump(p, {"ok": True})
            self.assertTrue(json.loads(p.read_text(encoding="utf-8"))["ok"])


if __name__ == "__main__":
    unittest.main()

from __future__ import annotations

import json
import unittest
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from chamber.runner import run_record


def record(domain, temporal, rigidity, collective, spectral):
    return {
        "id": "test",
        "label": "test",
        "domain": domain,
        "sectors": {
            "temporal": {"status": temporal, "q0": 2 if temporal == "SUPPORTED" else None},
            "rigidity": {"status": rigidity},
            "collective": {"status": collective},
            "spectral": {"status": spectral},
        },
        "provenance": [],
    }


class VerdictTests(unittest.TestCase):
    def test_no_temporal(self):
        r = run_record(record("quantum_many_body","NOT_SUPPORTED","NOT_SUPPORTED","NOT_SUPPORTED","NOT_SUPPORTED"))
        self.assertEqual(r["verdict"], "NO_TEMPORAL_ORDER")

    def test_classical_recurrence(self):
        r = run_record(record("classical","SUPPORTED","NOT_TESTED","N/A","N/A"))
        self.assertEqual(r["verdict"], "TEMPORAL_RECURRENCE")

    def test_classical_rigid(self):
        r = run_record(record("classical","SUPPORTED","SUPPORTED","N/A","N/A"))
        self.assertEqual(r["verdict"], "RIGID_RECURRENCE")

    def test_quantum_missing_collective(self):
        r = run_record(record("quantum_many_body","SUPPORTED","SUPPORTED","NOT_TESTED","NOT_TESTED"))
        self.assertEqual(r["verdict"], "INSUFFICIENT_DOMAIN_EVIDENCE")

    def test_quantum_collective(self):
        r = run_record(record("quantum_many_body","SUPPORTED","SUPPORTED","SUPPORTED","NOT_SUPPORTED"))
        self.assertEqual(r["verdict"], "COLLECTIVE_TEMPORAL_ORDER")

    def test_quantum_full(self):
        r = run_record(record("quantum_many_body","SUPPORTED","SUPPORTED","SUPPORTED","SUPPORTED"))
        self.assertEqual(r["verdict"], "MANY_BODY_TIME_CRYSTAL_ADMISSIBLE")


if __name__ == "__main__":
    unittest.main()

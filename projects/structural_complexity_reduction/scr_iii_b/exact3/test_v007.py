#!/usr/bin/env python3
"""Unit tests for the v007 verifier on small patches. Run: python3 scr_iii_b/exact3/test_v007.py  (needs g++)"""
import sys
sys.dont_write_bytecode = True
import pathlib, subprocess, tempfile, unittest
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parents[1] / "scr_iii_b" / "feasibility"))
import energy_windows_v006 as ew
import validate_v007 as v7

pe = ew.load_v005()
TMP = pathlib.Path(tempfile.mkdtemp(prefix="t7_"))
BIN = TMP / "verify3"
subprocess.run(["g++", "-std=c++17", "-O2", str(v7.SRC), "-o", str(BIN)], check=True)


class T(unittest.TestCase):
    def test_input_roundtrip_and_counts(self):
        for L, g in ((1, 6), (2, 82)):
            txt, isl, pairs, inc, masks = v7.make_input(pe, L)
            f = TMP / ("i%d.txt" % L); f.write_text(txt)
            kv, wins, _, _ = v7.run([str(BIN), str(f), "full", "0"])
            self.assertEqual(int(kv["grammar_states"]), g)
            self.assertEqual(int(kv["evaluated_direct"]), 1 << len(isl))
            self.assertEqual(int(kv["ground_states"]), 2)
            self.assertEqual(wins[0][3], 0)          # ground states are ice-admissible

    def test_failure_window_detected(self):
        txt, isl, pairs, inc, masks = v7.make_input(pe, 2)
        f = TMP / "i2.txt"; f.write_text(txt)
        n = len(isl)
        En = [pe.energy_norm(pe.decode(s, n), pairs) for s in range(1 << n)]
        lv, levels, _, _ = ew.group_levels(En)
        W2 = levels[2]["E_min"] - levels[0]["E_min"]
        kv, wins, _, _ = v7.run([str(BIN), str(f), "full", "%.17g" % W2])
        self.assertEqual(wins[0][3], 16)

    def test_constructive_matches_python(self):
        txt, isl, pairs, inc, masks = v7.make_input(pe, 2)
        f = TMP / "c2.txt"; f.write_text(txt)
        kv, _, _, _ = v7.run([str(BIN), str(f), "construct"])
        S, nodes = ew.constructive_enumerate(inc, len(isl))
        self.assertEqual(int(kv["found"]), len(S)); self.assertEqual(int(kv["id_sum"]), sum(S))

    def test_energy_ids_mode(self):
        txt, isl, pairs, inc, masks = v7.make_input(pe, 1)
        f = TMP / "e1.txt"; f.write_text(txt)
        idf = TMP / "ids.txt"; idf.write_text("\n".join(map(str, range(16))) + "\n")
        _, _, _, out = v7.run([str(BIN), str(f), "ids", str(idf)])
        got = {int(a): float(b) for a, b in (l.split() for l in out.splitlines())}
        for s in range(16):
            self.assertAlmostEqual(got[s], pe.energy_norm(pe.decode(s, 4), pairs), places=15)


if __name__ == "__main__":
    unittest.main(verbosity=2)

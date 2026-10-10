#!/usr/bin/env python3
"""Unit tests for physical_energy_v005.py (pure python, no source files needed).
Run:  python3 scr_iii_b/reference_check/test_v005.py"""
import pathlib, sys, unittest
from math import isclose
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import physical_energy_v005 as pe


def patch(L):
    isl = pe.source_geometry(L)
    return isl, pe.K_pairs(isl), len(isl)


class T(unittest.TestCase):
    def test_island_count(self):
        for L in (1, 2, 3):
            self.assertEqual(len(pe.source_geometry(L)), 2 * L * (L + 1))

    def test_K_symmetric_identical_islands(self):
        isl = pe.source_geometry(2)
        for i in range(len(isl)):
            for j in range(len(isl)):
                if i != j and (isl[i].ux, isl[i].uy) == (isl[j].ux, isl[j].uy):
                    self.assertTrue(isclose(pe.K_pair(isl[i], isl[j]), pe.K_pair(isl[j], isl[i]), rel_tol=1e-13))

    def test_global_reversal(self):
        isl, pairs, n = patch(2)
        for sid in (0, 5, 77, 1234, 4095):
            s = pe.decode(sid, n)
            self.assertAlmostEqual(pe.energy_norm(s, pairs), pe.energy_norm([-x for x in s], pairs), places=14)

    def test_flip_identity(self):
        isl, pairs, n = patch(2)
        s = pe.decode(1234, n); h = pe.local_fields(s, pairs, n)
        for k in range(n):
            t = list(s); t[k] = -t[k]
            self.assertAlmostEqual(pe.energy_norm(t, pairs) - pe.energy_norm(s, pairs), pe.flip_delta_norm(s, k, h), places=13)

    def test_encoding_roundtrip(self):
        for sid in (0, 1, 2047, 4095):
            self.assertEqual(pe.encode(pe.decode(sid, 12)), sid)

    def test_tc_guard(self):
        for T_ in (820.0, 900.0, -1.0):
            with self.assertRaises(ValueError):
                pe.moment_M(T_)

    def test_temperature_factor(self):
        r = pe.A_joule(780.0) / pe.A_joule(792.0)
        self.assertTrue(isclose(r, (1 - 780 / 820) / (1 - 792 / 820), rel_tol=1e-12))

    def test_charge_model_equals_A_times_K(self):
        isl = pe.source_geometry(1)
        for i in range(len(isl)):
            for j in range(i + 1, len(isl)):
                self.assertTrue(isclose(pe.pair_energy_charge_model_J(isl[i], isl[j], 792.0),
                                        pe.A_joule(792.0) * pe.K_pair(isl[i], isl[j]), rel_tol=2e-6))

    def test_ice_counts_and_ground_states(self):
        for L, n_ice in ((1, 6), (2, 82)):
            isl, pairs, n = patch(L); vpos = pe.vertex_positions(L)
            En = [pe.energy_norm(pe.decode(s, n), pairs) for s in range(1 << n)]
            ice = [pe.ice_ok_geometric(pe.decode(s, n), isl, vpos) for s in range(1 << n)]
            self.assertEqual(sum(ice), n_ice)
            emin = min(En)
            ground = [s for s, e in enumerate(En) if abs(e - emin) < 1e-12]
            self.assertEqual(len(ground), 2)
            self.assertTrue(all(ice[s] for s in ground))

    def test_legacy_sign_is_exact_negative(self):
        isl, pairs, n = patch(1)
        s = pe.decode(9, n)
        self.assertEqual(pe.energy_norm_legacy_v004(s, pairs), -pe.energy_norm(s, pairs))


if __name__ == "__main__":
    unittest.main(verbosity=2)

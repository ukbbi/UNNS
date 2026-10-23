"""Frozen scientific verdict must remain negative even when software checks pass."""
import json,math,unittest
import numpy as np
from pathlib import Path
from src import xvi_spectral_conditioning_v001 as m

class SpectralConditioningAuditV001(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw=json.loads((m.ROOT/m.RAW_PATH).read_text('utf8'))
        cls.report=m.run()

    def test_01_frozen_exact_sha(self):
        self.assertEqual(m.sha256(m.ROOT/'docs/frozen/XVI_INVARIANTS_AUDIT_v001.json'),
            'a0653783748355b06a96c86eb3b12fd07845c5976273a6bc8c7fcd0a40f8651e')

    def test_02_negative_verdict_is_unchanged(self):
        self.assertTrue(m.locked()['negative_verdict_preserved'])
        self.assertEqual(self.report['old_scientific_verdict'],'INVARIANT_FIDELITY_NOT_CERTIFIED')

    def test_03_canonical_html_sha_locked(self):
        self.assertEqual(m.sha256(m.ROOT/'docs/sources/XVI_ENGINE_v084.html'),
            'da4f217eaba86eba02517e6f6c2d70d8e5da43b189158b3ad22b93399d47d44d')

    def test_04_direct_source_raw_fields_are_nonempty(self):
        self.assertEqual(len(self.raw['cases']),4)
        for row in self.raw['cases']:self.assertEqual(len(row['tau']),row['N']**2)

    def test_05_old_export_raw_block_preserved(self):
        self.assertEqual(self.report['gates']['P6'],'BLOCKED_HISTORICAL_RAW_FIELDS_MISSING')

    def test_06_source_js_python_bins_match(self):
        for row in self.raw['cases']:
            k,pk,_=m.source_bin_spectrum(np.asarray(row['tau']).reshape(row['N'],row['N']))
            self.assertTrue(np.array_equal(k,np.asarray(row['original_js']['k'])))
            js=np.asarray(row['original_js']['Pk'])
            mask=js>=js.max()*1e-12
            self.assertLess(np.max(np.abs(js[mask]-pk[mask])/js[mask]),1e-8)

    def test_07_source_js_python_slope_match(self):
        for row in self.report['original_engine_cases']:
            self.assertLess(row['all_bin_parity']['p_abs_difference'],1e-8)
            self.assertLess(row['all_bin_parity']['r2_abs_difference'],1e-8)

    def test_08_conditioned_js_python_match(self):
        self.assertEqual(self.report['gates']['P3'],'PASS_CONDITIONED_JS_PY_PARITY')
        self.assertTrue(all(c['supported_js_python_agreement'] for c in self.report['original_engine_cases']))

    def test_09_known_powerlaw_calibration(self):
        for row in self.report['synthetic_controls']:
            if row['kind']=='known_powerlaw':
                self.assertTrue(row['conditioned']['reliable_power_law'])
                self.assertLess(abs(row['conditioned']['power_law_fit']['p']-2.28),0.15)

    def test_10_narrowband_rejected(self):
        for row in self.report['synthetic_controls']:
            if row['kind']=='narrowband':self.assertFalse(row['conditioned']['supported'])

    def test_11_white_noise_null_is_laplacian_blue(self):
        for row in self.report['synthetic_controls']:
            if row['kind']=='white_noise_null':
                self.assertTrue(row['conditioned']['supported'])
                self.assertLess(abs(row['conditioned']['power_law_fit']['p']+4),0.30)

    def test_12_source_target_failure_not_hidden(self):
        self.assertEqual(self.report['gates']['P4b'],'FAIL_FROZEN_SOURCE_P_TARGET')

    def test_13_source_has_2d_fft_laplacian(self):
        source=(m.ROOT/'docs/sources/XVI_ENGINE_v084.html').read_text('utf8')
        self.assertIn('captureSpectrum()',source)
        self.assertIn('const kappa = this.computeLaplacian(0)',source)
        self.assertIn('const k_bin = Math.floor(k)',source)
        self.assertIn('Pk_vals.push(bins[i].sum / bins[i].count)',source)

    def test_14_fixed_policy_no_silent_retuning(self):
        self.assertEqual(m.POLICY['bin_relative_power_floor'],1e-12)
        self.assertEqual(m.POLICY['fixed_k_min'],2)
        self.assertEqual(m.POLICY['source_p_target'],2.28)

    def test_15_bad_shapes_rejected(self):
        with self.assertRaises(ValueError):m.source_bin_spectrum(np.ones((20,20)))

    def test_16_zero_input_undefined_not_false_pass(self):
        k,pk,c=m.source_bin_spectrum(np.zeros((64,64)))
        self.assertFalse(m.condition(k,pk,c,64)['supported'])

    def test_17_identical_replay(self):
        self.assertTrue(np.array_equal(m.synthetic_field(64,41),m.synthetic_field(64,41)))

    def test_18_independent_windows_reported(self):
        for row in self.report['original_engine_cases']:
            self.assertEqual(len(row['condition_sensitivity']),12)
            self.assertEqual(len(row['noise_stress']),3)

    def test_19_no_physics_claim(self):
        self.assertFalse(self.report['full_canonical_invariant_certified'])
        self.assertEqual(self.report['born_rule'],'NOT_DERIVED')

    def test_20_original_html_not_modified_or_replaced(self):
        self.assertTrue(self.report['original_source_unmodified'])
        self.assertTrue(self.report['locked_inputs']['pass'])

if __name__=='__main__':unittest.main()

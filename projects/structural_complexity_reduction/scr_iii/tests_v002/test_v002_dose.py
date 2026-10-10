import unittest
from scr_iii.engine_v002_common import dose_delivered_family

class DoseTest(unittest.TestCase):
    def test_dose_free(self):
        self.assertFalse(dose_delivered_family([{"coverage_C":0.0},{"coverage_C":0.0}]))
        self.assertFalse(dose_delivered_family([{"coverage_C":None},{"coverage_C":None}]))
    def test_delivered(self):
        self.assertTrue(dose_delivered_family([{"coverage_C":0.0},{"coverage_C":0.5}]))

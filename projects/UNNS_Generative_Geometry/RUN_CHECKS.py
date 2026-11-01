"""Run exact standard-library tests. No remote writes and no source edits."""
import unittest
if __name__ == '__main__':
    suite = unittest.defaultTestLoader.discover('tests')
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    raise SystemExit(0 if result.wasSuccessful() else 1)

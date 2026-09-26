"""CI wrapper: runs 'rqgm_check.py selftest' (fixtures P01-P23) and checks the suite's shape."""
import hashlib
import json
import os
import subprocess
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
CHECK = os.path.join(os.path.dirname(os.path.dirname(HERE)), 'skills', 'rqgm-loop', 'rqgm_check.py')


def run(*args):
    return subprocess.run([sys.executable, CHECK] + list(args), capture_output=True, text=True, timeout=300)


class CheckerSelfTest(unittest.TestCase):
    def test_selftest_passes(self):
        p = run('selftest', HERE)
        self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
        self.assertTrue(json.loads(p.stdout)['ok'])

    def test_suite_covers_every_invariant_and_positives(self):
        with open(os.path.join(HERE, 'expected.json'), encoding='utf-8') as f:
            cases = json.load(f)['cases']
        self.assertEqual({c['invariant'] for c in cases}, {'P%02d' % i for i in range(1, 24)})
        positives = [c for c in cases if c['invariant'] == 'P23' and not c['codes'] and 'pending' not in c]
        self.assertGreaterEqual(len(positives), 6)  # guards against a reject-everything checker

    def test_hash_matches_hashlib(self):
        f = os.path.join(HERE, 'expected.json')
        with open(f, 'rb') as fh:
            want = hashlib.sha256(fh.read()).hexdigest()
        self.assertEqual(run('hash', f).stdout.split()[0], want)


if __name__ == '__main__':
    unittest.main()

"""CI wrapper: runs 'rqgm_check.py selftest' (fixtures P01-P23) and checks the suite's shape."""
import contextlib
import hashlib
import importlib.util
import io
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

    def test_no_t_records_is_an_integrity_error(self):  # PARITY-3: SKILL Memory 'Lines {"t":name,...fields}'
        p = run('audit', os.path.join(HERE, 'fixtures', 'p18_no_t_records.jsonl'))
        self.assertEqual(p.returncode, 2, p.stdout + p.stderr)
        out = json.loads(p.stdout)
        self.assertFalse(out['ok'])
        self.assertIn('no RQGM records', out['integrity']['error'])

    def test_audit_cli_never_crashes(self):  # round-2 c01-c05: huge ints, year-1 times, values echoed 2996 deep
        spec = importlib.util.spec_from_file_location('rqgm_check', CHECK)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        fx = os.path.join(HERE, 'fixtures')
        for name in sorted(n for n in os.listdir(fx) if n.endswith('.jsonl')):
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                code = mod.main(['audit', os.path.join(fx, name)])   # main() prints the report, as the CLI does
            out = json.loads(buf.getvalue())       # the report always serializes
            self.assertNotIn('error', out, name)   # a caught crash prints {"ok": false, "error": ...}, exit 2
            self.assertEqual(code, 2 if out['integrity'] else 0 if out['ok'] else 1, name)

    def test_hash_matches_hashlib(self):
        f = os.path.join(HERE, 'expected.json')
        with open(f, 'rb') as fh:
            want = hashlib.sha256(fh.read()).hexdigest()
        self.assertEqual(run('hash', f).stdout.split()[0], want)


if __name__ == '__main__':
    unittest.main()

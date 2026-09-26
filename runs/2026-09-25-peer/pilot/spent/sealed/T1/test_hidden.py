"""Sealed oracle for T1. Never shown to acting agents. Run against a candidate directory."""
import itertools
import random
import sys
import unittest

sys.path.insert(0, sys.argv.pop(1) if len(sys.argv) > 1 else ".")
from intervals import merge  # noqa: E402


def brute(intervals):
    pts = set()
    for a, b in intervals:
        pts.update(range(a, b))
    out = []
    for p in sorted(pts):
        if out and out[-1][1] == p:
            out[-1] = (out[-1][0], p + 1)
        else:
            out.append((p, p + 1))
    return out


class Hidden(unittest.TestCase):
    def test_touching_merge(self):            # seeded defect 1
        self.assertEqual(merge([(1, 3), (3, 5)]), [(1, 5)])

    def test_touching_chain(self):
        self.assertEqual(merge([(5, 7), (1, 3), (3, 5)]), [(1, 7)])

    def test_empty_dropped(self):             # seeded defect 2
        self.assertEqual(merge([(2, 2)]), [])

    def test_empty_between(self):
        self.assertEqual(merge([(1, 2), (4, 4), (6, 8)]), [(1, 2), (6, 8)])

    def test_empty_inside(self):
        self.assertEqual(merge([(1, 5), (3, 3)]), [(1, 5)])

    def test_input_not_mutated(self):         # seeded defect 3
        data = [(5, 6), (1, 2)]
        copy = list(data)
        merge(data)
        self.assertEqual(data, copy)

    def test_nested_and_duplicates(self):
        self.assertEqual(merge([(1, 10), (2, 3), (1, 10)]), [(1, 10)])

    def test_negative(self):
        self.assertEqual(merge([(-5, -2), (-2, 0)]), [(-5, 0)])

    def test_bad_interval_still_raises(self):
        with self.assertRaises(ValueError):
            merge([(1, 2), (4, 3)])

    def test_tuple_types(self):
        out = merge([[1, 3], [2, 4]])
        self.assertTrue(all(type(x) is tuple and len(x) == 2 for x in out))

    def test_property_vs_bruteforce(self):
        rng = random.Random(20260925)
        for _ in range(400):
            n = rng.randint(0, 6)
            ivs = []
            for _ in range(n):
                a = rng.randint(-6, 6)
                ivs.append((a, a + rng.randint(0, 4)))
            self.assertEqual(merge(list(ivs)), brute(ivs), ivs)


if __name__ == "__main__":
    unittest.main(argv=[sys.argv[0], "-v"])

import unittest
from intervals import merge


class PublicTests(unittest.TestCase):
    def test_overlap(self):
        self.assertEqual(merge([(1, 5), (3, 8)]), [(1, 8)])

    def test_disjoint_sorted(self):
        self.assertEqual(merge([(10, 12), (1, 3)]), [(1, 3), (10, 12)])

    def test_single(self):
        self.assertEqual(merge([(2, 4)]), [(2, 4)])

    def test_empty_list(self):
        self.assertEqual(merge([]), [])

    def test_bad_interval(self):
        with self.assertRaises(ValueError):
            merge([(5, 1)])


if __name__ == "__main__":
    unittest.main()

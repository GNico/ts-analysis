import pandas as pd
import unittest
from model.baseline import Baseline


class TestBaseline(unittest.TestCase):

    def test_baseline(self):

        baseline = Baseline()
        baseline.add_point(pd.Timestamp(1, unit='s'), 0, 1)
        baseline.add_point(pd.Timestamp(2, unit='s'), 1, 2)

        output = baseline.output_format()
        self.assertEqual(2, len(output))
        self.assertEqual(1000, output[0][0])
        self.assertEqual(0, output[0][1])
        self.assertEqual(1, output[0][2])
        self.assertEqual(2000, output[1][0])
        self.assertEqual(1, output[1][1])
        self.assertEqual(2, output[1][2])
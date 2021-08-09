import pandas as pd
import unittest

from model.pipeline.nodes.transformers.stl import STL

class TestSTL(unittest.TestCase):

    def test_stl_period_samples(self):
        self.case([1, 2, 3, 1, 2, 3], 3, [1, 2, 3])
        self.case([1, 2, 3, 4], 2, [2, 3])

    def case(self, values, period, expected_values):
        output = STL.model_period_sample(values, period)
        period_values = [i[1] for i in output]
        self.assertEqual(expected_values, period_values)

import unittest
import json
import os
import hashlib
from pathlib import Path

from model.series import Series
from model.pipeline.pipeline import Pipeline
from model.analyzer import Analyzer

class TestIntegrationPerformance(unittest.TestCase):

    def test_integration_performance(self):
        pipeline = Pipeline.from_json(self.load_json('pipeline'))
        input1 = Series.from_array(self.load_json('input1'), interval=3600, unit='ms')
        input2 = Series.from_array(self.load_json('input2'), interval=3600, unit='ms')
        
        analyzer = Analyzer(pipeline, True)
        result = analyzer.analyze({'1': input1, '2': input2})

        actual_output = result.output_format()
        expected_output = self.load_json('expected_output')
        # self.maxDiff = None
        self.assertEqual(expected_output, actual_output)

    def load_json(self, file):
        dir = os.path.dirname(__file__)
        path = os.path.join(dir, 'resources/perf/' + file + '.json')
        content = Path(path).read_text()
        return json.loads(content)
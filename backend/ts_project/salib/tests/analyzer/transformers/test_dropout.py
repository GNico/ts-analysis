import unittest

from model.analyzer import Analyzer
from model.anomaly import Anomaly
from model.analysis import Analysis
from model.series import Series
from model.pipeline.pipeline import Pipeline
from model.pipeline.node_factory import NodeFactory
from model.pipeline.nodes.node_source import InputRef
from model.test.test_series_builder import TestSeriesBuilder
from model.test.testcase import TestCase

class TestDropout(unittest.TestCase):

    def test_dropout_mean(self):
        
        factory = NodeFactory.transformer('test', 'Dropout')
        factory.set_param_value('context_window', 4)
        factory.set_param_value('dropout_window', 2)
        factory.set_param_value('center', False)
        factory.set_param_value('min_periods', None)
        factory.set_param_value('agg_method', 'mean')
        factory.add_source(InputRef('input'))
        ram = factory.build()

        self.case(ram, [])

    def case(self, node, expected_series):
        series = self.build_series()
        pipeline = Pipeline([node])
        analyzer = Analyzer(pipeline=pipeline, debug=False)
        analysis = analyzer.analyze({'input':series})
        result = analysis.result_for_node(node.id)

        self.assertEqual(expected_series, result.output_series.as_list())

    def build_series(self):
        series = Series.from_array([
            [0, 1],
            [1, 1],
            [2, 1],
            [3, 1],
            [4, 3],
            [5, 3],
            [6, 3],
        ])
        return series

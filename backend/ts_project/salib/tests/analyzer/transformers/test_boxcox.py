import unittest

from model.analyzer import Analyzer
from model.anomaly import Anomaly
from model.analysis import Analysis
from model.pipeline.pipeline import Pipeline
from model.pipeline.node_factory import NodeFactory
from model.test.test_series_builder import TestSeriesBuilder
from model.test.testcase import TestCase
from model.pipeline.nodes.node_source import InputRef

from model.utils import timestamp_to_epoch

class TestBoxCox(unittest.TestCase):

    def test_boxcox_implied_lambda(self):
        series = self.build_triangle()
        factory = NodeFactory.transformer('boxcox', 'BoxCox')
        # factory.set_param_value('lambda', 1)
        factory.add_source(InputRef('input'))
        boxcox = factory.build()

        expected_debug = {
            'lambda': None,
            'fitted_lambda': 0.7569500835813396,
        }
        self.case(series, boxcox,
            [0.0,
            3.8069844496343204,
            6.792535931588043,
            9.45326887138231,
            11.915823446529231,
            11.915823446529231,
            11.435878585907972,
            10.950062851581707,
            10.457989331193566,
            9.959222501860888,
            9.45326887138231,
            8.939565111800931,
            8.417462798503934,
            7.88620846728669,
            7.344917074353449,
            6.792535931588043,
            6.227794497220499,
            5.649132457366781,
            5.054593159635213,
            4.441659075192572,
            3.8069844496343204,
            3.1459316503179107,
            2.45169446968289,
            1.7134270251968304,
            0.9114396216016829],
            expected_debug)

    def test_boxcox_fixed_lambda(self):
        series = self.build_triangle()
        factory = NodeFactory.transformer('boxcox', 'BoxCox')
        factory.set_param_value('lambda', 1)
        factory.add_source(InputRef('input'))
        boxcox = factory.build()

        expected_debug = {
            'lambda': 1,
            'fitted_lambda': 1,
        }
        self.maxDiff = None
        self.case(series, boxcox,
            [0.0,
            5.0,
            10.000000000000002,
            14.999999999999998,
            20.0,
            20.0,
            18.999999999999996,
            17.999999999999996,
            16.999999999999996,
            16.0,
            14.999999999999998,
            14.0,
            12.999999999999996,
            12.0,
            11.0,
            10.000000000000002,
            9.000000000000002,
            8.000000000000002,
            6.999999999999998,
            5.999999999999999,
            5.0,
            3.999999999999999,
            3.0,
            2.0000000000000004,
            1.0],
            expected_debug)

    def case(self, series, node, expected_series, expected_debug):
        pipeline = Pipeline([node])
        analyzer = Analyzer(pipeline=pipeline, debug=False)
        inputs = {
            'input': series
        }
        analysis = analyzer.analyze(inputs)
        result = analysis.result_for_node(node.id)
        self.assertEqual(expected_debug, result.debug_info)
        self.assertEqual(expected_series, result.output_series.as_list())

    def build_triangle(self):
        sb_up = TestSeriesBuilder.linear(5, 0, 5)
        sb_down = TestSeriesBuilder.linear(20, 0, -1)
        sb_up.append(sb_down, True)
        series = sb_up.build()
        return series

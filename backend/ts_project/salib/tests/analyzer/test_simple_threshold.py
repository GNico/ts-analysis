import unittest

from model.analyzer import Analyzer
from model.anomaly import Anomaly
from model.analysis import Analysis
from model.pipeline.pipeline import Pipeline
from model.pipeline.node_factory import NodeFactory
from model.pipeline.nodes.mock import NoBaseline
from model.pipeline.params.float import Float, BoundedFloat
from model.test.test_series_builder import TestSeriesBuilder
from model.test.testcase import TestCase


class TestSimpleThreshold(unittest.TestCase):

    # TODO: complete
    def test_simple_threshold(self):
        series = self.build_triangle()
        
        factory = NodeFactory.detector('test', 'SimpleThreshold')
        factory.set_param_value('inside', False)
        factory.set_param_value('above', 1)
        factory.set_param_value('below', 0)
        st = factory.build()

        pipeline = Pipeline(st)
        analyzer = Analyzer(pipeline=pipeline)
        analysis = analyzer.analyze(series)
        anomalies = analysis.anomalies

        # self.assertEqual(1, len(anomalies))
        # self.assertEqual(1, len(analysis.anomalies_by_algo))
        # algo_ids = list(analysis.anomalies_by_algo.keys())
        # algo_key = "SimpleThreshold("+str(st.decay())+","+str(st.threshold())+")[test]"
        # self.assertEqual([algo_key], algo_ids)
        # self.assertEqual(analysis.anomalies_by_algo[algo_key], anomalies)

        # anomaly = anomalies[0]
        # self.assertEqual(100, series.time_idx(anomaly.start))
        # self.assertEqual(105, series.time_idx(anomaly.end))
        # self.assertEqual(1, anomaly.score)

        # expected_anomalies = [
        #     Anomaly.from_epoch(series, 100, 103, 1.0),
        #     Anomaly.from_epoch(series, 10, 25, 1.0),
        # ]
        # expected_analysis = Analysis(series, expected_anomalies, NoBaseline())

        # test_case = TestCase("test_st", series, analyzer, expected_analysis)
        # result = test_case.run()
        # # result.export_for_visuals()
        # metrics = result.anomaly_metrics
        # self.assertEqual(4, metrics.tp_count())
        # self.assertEqual(178, metrics.tn_count())
        # self.assertEqual(2, metrics.fp_count())
        # self.assertEqual(16, metrics.fn_count())
        # self.assertAlmostEqual(0.666, metrics.precision(), 2)
        # self.assertAlmostEqual(0.2, metrics.recall(), 2)
        # self.assertAlmostEqual(0.307, metrics.f1(), 2)

    def build_triangle(self):
        sb_up = TestSeriesBuilder.linear(100, 0, 1)
        sb_down = TestSeriesBuilder.linear(100, 0, -1)
        sb_up.append(sb_down, True)
        series = sb_up.build()

        raw_values = series.as_list()
        self.assertEqual(2, raw_values.count(0))
        self.assertEqual(0, min(raw_values))
        self.assertEqual(0, raw_values[0])
        self.assertEqual(0, raw_values[-1])
        self.assertEqual(99, raw_values[100])
        self.assertEqual(99, max(raw_values))
        self.assertEqual(2, raw_values.count(99))
        return series

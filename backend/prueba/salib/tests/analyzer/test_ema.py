import unittest

from model.analyzer import Analyzer
from model.test.test_series_builder import TestSeriesBuilder
from model.algos.ema import EMA


class TestEMA(unittest.TestCase):

    def test_ema(self):
        series = self.build_triangle()
        decay = 0.95
        threshold = 1
        ema = EMA(decay=decay, threshold=threshold)

        analyzer = Analyzer(anomalies_algos=[ema])
        analysis = analyzer.analyze(series)
        anomalies = analysis.anomalies

        self.assertEqual(1, len(anomalies))
        self.assertEqual(1, len(analysis.anomalies_by_algo))
        algo_ids = list(analysis.anomalies_by_algo.keys())
        algo_key = "EMA("+str(decay)+","+str(threshold)+")"
        self.assertEqual([algo_key], algo_ids)
        self.assertEqual(analysis.anomalies_by_algo[algo_key], anomalies)

        anomaly = anomalies[0]
        self.assertEqual(100, series.time_idx(anomaly.start))
        self.assertEqual(105, series.time_idx(anomaly.end))
        self.assertEqual(1, anomaly.score)

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

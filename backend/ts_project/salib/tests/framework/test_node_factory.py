import unittest

from model.pipeline.node_factory import NodeFactory


class TestNodeFactory(unittest.TestCase):
    def test_node_list(self):
        self.maxDiff = None
        expected = {
            "aggregator": [
                {
                    "desc": "Combine all anomalies from sources",
                    "display": "Or",
                    "params": [],
                    "type": "OR",
                },
                {
                    "desc": "Combine overlapping anomalies from sources",
                    "display": "And",
                    "params": [],
                    "type": "AND",
                },
            ],
            "detector": [
                {
                    "desc": "Detect values outside of bounds",
                    "display": "Simple Threshold",
                    "params": [
                        {
                            "conditions": [],
                            "desc": "If true, value must be within bounds",
                            "display": "Inside",
                            "id": "inside",
                            "type": "Boolean",
                            "value": False,
                        },
                        {
                            "conditions": [],
                            "desc": "Strict comparison on bounds",
                            "display": "Strict",
                            "id": "strict",
                            "type": "Boolean",
                            "value": False,
                        },
                        {
                            "conditions": [],
                            "desc": "Lower bound",
                            "display": "Lower",
                            "id": "lower",
                            "type": "Float",
                            "value": None,
                        },
                        {
                            "conditions": [],
                            "desc": "Upper bound",
                            "display": "Upper",
                            "id": "upper",
                            "type": "Float",
                            "value": None,
                        },
                    ],
                    "type": "SimpleThreshold",
                }
            ],
            "transformer": [
                {
                    "desc": "Normalize data such that mean = 0 and std dev = 1",
                    "display": "Standard normalization",
                    "params": [],
                    "type": "StdNormalize",
                },
                {
                    "desc": "Exponential moving average with decay rate",
                    "display": "Exponential moving average",
                    "params": [
                        {
                            "conditions": [],
                            "desc": "Decay rate",
                            "display": "Decay",
                            "id": "decay",
                            "max": 1,
                            "min": 0,
                            "type": "BoundedFloat",
                            "value": 0.9,
                        }
                    ],
                    "type": "EMA",
                },
                {
                    "desc": "Rolling aggregate",
                    "display": "Rolling Aggregate",
                    "params": [
                        {
                            "conditions": [],
                            "desc": "Window size in time interval (eg: 1h)",
                            "display": "Window",
                            "id": "window",
                            "type": "String",
                            "value": "30m",
                        },
                        {
                            "conditions": [],
                            "desc": "Center aggregation window around value",
                            "display": "Center",
                            "id": "center",
                            "type": "Boolean",
                            "value": False,
                        },
                        {
                            "conditions": [],
                            "desc": "Min number of periods",
                            "display": "Min. periods",
                            "id": "min_periods",
                            "max": None,
                            "min": 0,
                            "type": "BoundedInt",
                            "value": 0,
                        },
                        {
                            "conditions": [],
                            "desc": "Aggregation method",
                            "display": "Aggregation",
                            "id": "agg_method",
                            "options": [
                                {"code": "mean", "display": "Mean"},
                                {"code": "median", "display": "Median"},
                                {"code": "sum", "display": "Sum"},
                                {"code": "min", "display": "Min"},
                                {"code": "max", "display": "Max"},
                                {"code": "quantile", "display": "Quantile"},
                                {"code": "iqr", "display": "Inter-quartile range"},
                                {"code": "idr", "display": "Inter-decile range"},
                                {"code": "count", "display": "Value count"},
                                {"code": "nnz", "display": "Non zero count"},
                                {"code": "nunique", "display": "Unique count"},
                                {"code": "std", "display": "Sample standard dev."},
                                {"code": "var", "display": "Sample variance"},
                                {"code": "skew", "display": "Sample skewness"},
                                {"code": "kurt", "display": "Sample kurtosis"},
                            ],
                            "type": "Select",
                            "value": "mean",
                        },
                        {
                            'conditions': [
                                {
                                    'args': {'param': 'agg_method', 'value': 'quantile'},
                                    'type': 'param_equals_value'
                                }
                            ],
                            'desc': 'Quantile range [q;1-q]',
                            'display': 'Quantile range',
                            'id': 'quantile_range',
                            'max': 0.5,
                            'min': 0,
                            'type': 'BoundedFloat',
                            'value': 0.25
                        }
                    ],
                    "type": "RollingAggregate",
                },
            ],
        }

        self.assertEqual(expected, NodeFactory.nodes_list())

    def test_parsing(self):
        builder = NodeFactory.detector("test_id", "SimpleThreshold")
        builder.set_param_value("inside", False)
        builder.set_param_value("strict", False)
        builder.set_param_value("lower", 1)
        builder.set_param_value("upper", None)
        threshold = builder.build()
        self.assertEqual(str(threshold), "SimpleThreshold(1,None,False,False)[test_id]")

        obj = {
            "id": "test_id",
            "group": "detector",
            "type": "SimpleThreshold",
            "params": [
                {"id": "lower", "value": 1},
                {"id": "inside", "value": False},
                {"id": "strict", "value": False},
            ],
        }
        th_from_json = NodeFactory.from_json(obj)
        self.assertEqual(str(threshold), str(th_from_json))

    def test_parsing_debug(self):
        builder = NodeFactory.detector("test_id", "SimpleThreshold")
        builder.set_param_value("inside", False)
        builder.set_param_value("strict", False)
        builder.set_param_value("lower", 1)
        builder.set_param_value("upper", None)
        builder.set_debug(True)
        threshold = builder.build()
        self.assertEqual(str(threshold), "SimpleThreshold(1,None,False,False)[test_id]")

        obj = {
            "id": "test_id",
            "group": "detector",
            "type": "SimpleThreshold",
            "params": [
                {"id": "lower", "value": 1},
                {"id": "inside", "value": False},
                {"id": "strict", "value": False},
            ],
            "debug": True
        }
        th_from_json = NodeFactory.from_json(obj)
        self.assertEqual(threshold.is_debug(), th_from_json.is_debug())

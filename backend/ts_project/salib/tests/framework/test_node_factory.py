import unittest
import json
import os
from pathlib import Path

from model.pipeline.node_factory import NodeFactory


class TestNodeFactory(unittest.TestCase):
    def test_node_list(self):
        self.maxDiff = None
        dir = os.path.dirname(__file__)
        expected_file = os.path.join(dir, 'resources/expected_nodes.json')
        expected = json.loads(Path(expected_file).read_text())
        actual = NodeFactory.nodes_list()
        self.assertEqual(expected, actual)

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
            "debug": True,
        }
        th_from_json = NodeFactory.from_json(obj)
        self.assertEqual(threshold.is_debug(), th_from_json.is_debug())

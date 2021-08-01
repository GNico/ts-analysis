import unittest
import json
import os
from pathlib import Path

from model.pipeline.node_factory import NodeFactory


class TestNodeFactory(unittest.TestCase):

    def test_node_list(self):
        actual = NodeFactory.nodes_list()
        dir = os.path.dirname(__file__)
        expected_file = os.path.join(dir, 'resources/expected_nodes.json')
        # Uncomment to fix test
        # print(json.dumps(actual, indent=2), file=open(expected_file, 'w'))
        expected = json.loads(Path(expected_file).read_text())
        self.maxDiff = None
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

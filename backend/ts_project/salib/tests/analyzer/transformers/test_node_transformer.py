import unittest

from model.pipeline.nodes.node_transformer import NodeTransformer

class TestNodeTransformer(unittest.TestCase):

    def test_window_slicing_uncentered(self):
        test_data = [1, 2, 3]
        
        self.case(test_data, 0, 1, False, [1])
        self.case(test_data, 1, 1, False, [2])
        self.case(test_data, 2, 1, False, [3])

        self.case(test_data, 0, 2, False, [1])
        self.case(test_data, 1, 2, False, [1, 2])
        self.case(test_data, 2, 2, False, [2, 3])

        self.case(test_data, 0, 3, False, [1])
        self.case(test_data, 1, 3, False, [1, 2])
        self.case(test_data, 2, 3, False, [1, 2, 3])

    def test_window_slicing_centered(self):
        test_data = [1, 2, 3]
        
        self.case(test_data, 0, 1, True, [1])
        self.case(test_data, 1, 1, True, [2])
        self.case(test_data, 2, 1, True, [3])

        self.case(test_data, 0, 3, True, [1, 2])
        self.case(test_data, 1, 3, True, [1, 2, 3])
        self.case(test_data, 2, 3, True, [2, 3])
        
        self.case(test_data, 0, 2, True, [1])
        self.case(test_data, 1, 2, True, [1, 2])
        self.case(test_data, 2, 2, True, [2, 3])


    def case(self, data, index, window_size, center, expected):
        actual = NodeTransformer.window_slice(data, index, window_size, center)
        self.assertEqual(expected, actual)


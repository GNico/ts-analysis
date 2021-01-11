import unittest

from model.pipeline.component_factory import ComponentFactory


class TestComponentFactory(unittest.TestCase):

    def test_definitions(self):
        expected = {
            'EMA': {
                'type': 'detector',
                'desc': 'sarasa',
                'params': {
                    'decay': {
                        'id': 'decay',
                        'max': 1,
                        'min': 0,
                        'type': 'BoundedFloat',
                        'value': 0.9,
                    },
                    'threshold': {
                        'id': 'threshold',
                        'type': 'Float',
                        'value': 2,
                    }
                }
            }
        }
        self.assertEqual(expected, ComponentFactory.components_description())
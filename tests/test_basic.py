import unittest
import tiza.foo

class TestBasic(unittest.TestCase):

    def test_foo(self):
        t = tiza.foo.Foo()
        self.assertEqual(5, t.value())
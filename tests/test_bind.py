import unittest
from typing import Callable

from injkt import Bind


class TestBind(unittest.TestCase):
    def test_bind_data_structure(self):
        interface = int
        implementation = lambda: 42
        bind = Bind(interface, implementation, True)
        self.assertEqual(bind.interface, int)
        self.assertIsInstance(bind.implementation, Callable)
        self.assertTrue(bind.always_reinit)

    def test_hash(self):
        bind1 = Bind(int, lambda: 42)
        bind2 = Bind(int, lambda: 24)
        self.assertEqual(hash(bind1), hash(bind2))

    def test_equality(self):
        bind1 = Bind(int, lambda: 42)
        bind2 = Bind(int, lambda: 24)
        bind3 = Bind(str, lambda: "hello")
        self.assertEqual(bind1, bind2)
        self.assertNotEqual(bind1, bind3)

    def test_inequality_with_different_type(self):
        bind = Bind(int, lambda: 42)
        self.assertNotEqual(bind, 42)


if __name__ == "__main__":
    unittest.main()

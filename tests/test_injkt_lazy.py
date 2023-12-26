import unittest

from injkt import InjktLazy
from injkt.exceptions import InterfaceNotFound
from injkt.injectable import Injectable


class TestInjktLazy(unittest.TestCase):
    def setUp(self):
        self.injkt_lazy = InjktLazy()

    def test_getattribute_with_injectable(self):
        injectable = Injectable(int)
        setattr(self.injkt_lazy, "injectable_attr", injectable)
        with self.assertRaises(InterfaceNotFound):
            getattr(self.injkt_lazy, "injectable_attr")

    def test_getattribute_without_injectable(self):
        test_value = "test_value"
        attr_name = "some_attr"
        setattr(self.injkt_lazy, attr_name, test_value)
        result = getattr(self.injkt_lazy, attr_name)
        self.assertEqual(result, test_value)

    def test_is_lazy(self):
        setattr(InjktLazy, "injectable_attr", Injectable(int))
        attr_type = type(getattr(InjktLazy, "injectable_attr"))
        self.assertEqual(attr_type, Injectable)


if __name__ == "__main__":
    unittest.main()

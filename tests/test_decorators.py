import unittest
from unittest.mock import Mock, patch

from injkt import inject_args_deps, inject_attr_deps
from injkt.injectable import Injectable
from injkt.injktor import Injktor


class NonInjectable:
    pass


class TestInjectAttrDeps(unittest.TestCase):
    def setUp(self):
        self.mock_impl_cls = Mock()

    @patch.object(Injktor, "get", return_value=Mock())
    def test_inject_attr_deps_with_injectable(self, mock_get):
        @inject_attr_deps
        class MyClass:
            my_attr = Injectable(str)

        MyClass()
        mock_get.assert_called_with(str)
        self.assertIsInstance(MyClass.my_attr, Mock)

    def test_inject_attr_deps_with_non_injectable(self):
        @inject_attr_deps
        class MyClass:
            my_attr = NonInjectable()

        self.assertIsInstance(MyClass.my_attr, NonInjectable)


class TestInjectArgsDeps(unittest.TestCase):
    def setUp(self):
        self.mock_impl_cls = Mock()

    @patch.object(Injktor, "get", return_value=Mock())
    def test_inject_args_deps_with_injectable(self, mock_get):
        @inject_args_deps
        def my_func(my_arg=Injectable(str)):
            return my_arg

        result = my_func()
        mock_get.assert_called_with(str)
        self.assertIsInstance(result, Mock)

    def test_inject_args_deps_with_non_injectable(self):
        @inject_args_deps
        def my_func(my_arg=NonInjectable()):
            return my_arg

        result = my_func()
        self.assertIsInstance(result, NonInjectable)

    @patch.object(Injktor, "get", return_value=Mock())
    def test_inject_args_deps_without_default(self, mock_get):
        @inject_args_deps
        def my_func(my_arg):
            return my_arg

        with self.assertRaises(TypeError):
            my_func()  # type: ignore

        my_func("test")
        mock_get.assert_not_called()


if __name__ == "__main__":
    unittest.main()

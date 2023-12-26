import unittest

from injkt import DIConfigurationError, Injectable


class MyInjectionClass:
    pass


class TestInjectable(unittest.TestCase):
    def test_instantiation_with_valid_class(self):
        injectable_instance = Injectable(MyInjectionClass)
        self.assertIsInstance(injectable_instance, Injectable)
        self.assertEqual(injectable_instance.__injection__, MyInjectionClass)  # type: ignore

    def test_instantiation_with_injectable_class(self):
        with self.assertRaises(ValueError) as context:
            Injectable(Injectable)

        self.assertEqual(str(context.exception), "Injectable cannot be injected.")

    def test_getattr_raises_di_configuration_error(self):
        injectable_instance = Injectable(MyInjectionClass)

        with self.assertRaises(DIConfigurationError):
            _ = injectable_instance.some_nonexistent_attribute  # type: ignore


if __name__ == "__main__":
    unittest.main()

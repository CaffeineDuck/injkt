import unittest

from injkt.meta import Singleton


class SingletonClass(metaclass=Singleton):
    pass


class AnotherSingletonClass(metaclass=Singleton):
    pass


class TestSingleton(unittest.TestCase):
    def test_singleton_instance(self):
        instance1 = SingletonClass()
        instance2 = SingletonClass()
        self.assertIs(instance1, instance2)

    def test_singleton_instance_with_different_classes(self):
        instance1 = SingletonClass()
        instance2 = AnotherSingletonClass()
        self.assertIsNot(instance1, instance2)

    def test_singleton_with_parameters(self):
        class SingletonWithInit(metaclass=Singleton):
            def __init__(self, param):
                self.param = param

        instance1 = SingletonWithInit(1)
        instance2 = SingletonWithInit(2)

        self.assertIs(instance1, instance2)
        self.assertEqual(instance1.param, 1)
        self.assertEqual(instance2.param, 1)


if __name__ == "__main__":
    unittest.main()

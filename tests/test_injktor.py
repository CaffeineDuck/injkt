import random
import unittest

from injkt import Bind, Injktor
from injkt.exceptions import AlwaysReinitNotCallable, InterfaceNotFound


class TestInjktor(unittest.TestCase):
    def setUp(self):
        self.injktor = Injktor()

    def tearDown(self) -> None:
        self.injktor.clear()

    def test_init(self):
        self.assertIsInstance(self.injktor, Injktor)
        print(self.injktor._binds_map)
        self.assertEqual(len(self.injktor._binds_map), 0)

    def test_install_binds(self):
        binds = {Bind(interface=int, implementation=lambda: 123)}
        self.injktor.install_binds(binds)
        self.assertEqual(self.injktor._binds_map, {int: binds.pop()})

    def test_set_and_get(self):
        self.injktor.set(Bind(interface=str, implementation=lambda: "hello"))
        result = self.injktor.get(str)
        self.assertEqual(result, "hello")

    def test_delete(self):
        self.injktor.set(Bind(interface=float, implementation=lambda: 3.14))
        self.injktor.delete(float)
        with self.assertRaises(InterfaceNotFound):
            self.injktor.get(float)

    def test_clear(self):
        self.injktor.set(Bind(interface=list, implementation=lambda: [1, 2, 3]))
        self.injktor.clear()
        self.assertEqual(len(self.injktor._binds_map), 0)

    def test_is_singleton(self):
        injktor1 = Injktor()
        injktor2 = Injktor()
        self.assertEqual(injktor1, injktor2)

    def test_get_with_no_bind(self):
        with self.assertRaises(InterfaceNotFound):
            self.injktor.get(int)

    def test_get_with_always_reinit(self):
        self.injktor.set(
            Bind(
                interface=int,
                implementation=lambda: random.randint(1, 100),
                always_reinit=True,
            )
        )
        val = self.injktor.get(int)
        val2 = self.injktor.get(int)
        self.assertNotEqual(val, val2)

    def test_get_with_always_reinit_not_callable(self):
        self.injktor.set(
            Bind(interface=int, implementation=123, always_reinit=True)  # type: ignore
        )
        with self.assertRaises(AlwaysReinitNotCallable):
            self.injktor.get(int)


if __name__ == "__main__":
    unittest.main()

import unittest

from abc import ABC

from Illuminate.Container.Container import Container
from Illuminate.Foundation.Application import Application


class ContainerTest(unittest.TestCase):
    def test_it_is_an_abstract_class(self):
        self.assertTrue(issubclass(Container, ABC))

    def test_it_can_not_be_initiated(self):
        with self.assertRaises(TypeError) as context:
            Container()

        self.assertTrue(
            str(context.exception).startswith(
                "Can't instantiate abstract class Container"
            ),
        )

    def test_it_has_bind_method(self):
        self.assertTrue(hasattr(Container, "bind"))

    def test_it_has_singleton_method(self):
        self.assertTrue(hasattr(Container, "singleton"))

    def test_it_has_make_method(self):
        self.assertTrue(hasattr(Container, "make"))

    def test_it_has_instance_method(self):
        self.assertTrue(hasattr(Container, "instance"))

    def test_it_has_private_bindings_attribute(self):
        app = Application()

        with self.assertRaises(AttributeError):
            bindings = app.__bindings

    def test_it_has_bindings_getter(self):
        app = Application()

        self.assertTrue(hasattr(app, "get_bindings"))

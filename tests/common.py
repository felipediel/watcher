"""Common."""
from django.test import SimpleTestCase


class BaseTestCase(SimpleTestCase):
    """Base test case."""

    def assertAttrEqual(self, obj, name, value):  # pylint: disable=C0103
        """Assert attribute is equal."""
        self.assertTrue(
            hasattr(obj, name), f"{obj} does not have attribute {name}"
        )
        self.assertEqual(
            getattr(obj, name),
            value,
            f"{name} attribute of {obj} is not equal to {value}",
        )

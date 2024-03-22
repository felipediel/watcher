"""Common."""
from django.test import SimpleTestCase


class BaseTestCase(SimpleTestCase):
    """Base test case."""

    def assertAttrEqual(self, obj, attr, value):  # pylint: disable=C0103
        """Assert attribute is equal."""
        self.assertTrue(
            hasattr(obj, attr), f"{obj} does not have attribute {attr}"
        )
        self.assertEqual(
            getattr(obj, attr),
            value,
            f"{attr} attribute of {obj} is not equal to {value}",
        )

    def getItemFromList(self, obj, attr, value):  # pylint: disable=C0103
        try:
            return next(
                item
                for item in obj
                if getattr(item, attr) == value
            )
        except (AttributeError, StopIteration):
            self.fail(
                f"{obj} does not have item with attribute '{attr}' == {value}"
            )

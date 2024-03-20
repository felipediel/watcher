"""Specifications."""

import abc
from typing import Any, Iterable


class Specification(abc.ABC):
    """Specification.

    Interface for defining specifications to be applied to objects.
    Specifications encapsulate criteria that objects must satisfy.
    """

    @abc.abstractmethod
    def is_satisfied_by(self, obj: Any) -> bool:
        """Check if the given object satisfies the specification."""


class EqualsSpecification(Specification):
    """Equals specification.

    Specification that checks if an object is equal to a specified value.
    """

    __slots__ = ["field", "value"]

    def __init__(self, field: str, value: Any) -> None:
        """Initialize the specification."""
        self.field = field
        self.value = value

    def is_satisfied_by(self, obj: Any) -> bool:
        """Check if the given object satisfies the specification."""
        return getattr(obj, self.field) == self.value


class InSpecification(Specification):
    """In specification.

    Specification that checks if an object is contained within a collection.
    """

    __slots__ = ["field", "value"]

    def __init__(self, field: str, value: Iterable[Any]) -> None:
        """Initialize the specification."""
        self.field = field
        self.value = value

    def is_satisfied_by(self, obj: Any) -> bool:
        """Check if the given object satisfies the specification."""
        return getattr(obj, self.field) in self.value

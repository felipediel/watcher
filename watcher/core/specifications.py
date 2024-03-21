"""Specifications."""

import abc
from typing import Any, Generator, Iterable, Mapping


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
        """Initialize specification."""
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
        """Initialize specification."""
        self.field = field
        self.value = value

    def is_satisfied_by(self, obj: Any) -> bool:
        """Check if the given object satisfies the specification."""
        return getattr(obj, self.field) in self.value


class AndSpecification(Specification):
    """And specification.

    Specification that checks if an object satisfies all child specifications.
    """

    __slots__ = ["specs"]

    def __init__(self, *specs: Iterable[Specification]) -> None:
        """Initialize specification."""
        self.specs = specs

    def is_satisfied_by(self, obj: Any) -> bool:
        """Check if the given object satisfies the specification."""
        return all(spec.is_satisfied_by(obj) for spec in self.specs)


class SpecificationBuilder(abc.ABC):
    """Specification builder."""

    @abc.abstractmethod
    def build(self, data: Mapping[str, Any]) -> Specification:
        """Build specification."""


class CompositeSpecificationBuilder(SpecificationBuilder):
    """Composite specification builder."""

    def _iter_specs(
        self, data: Mapping[str, Any]
    ) -> Generator[Specification, None, None]:
        """Iterate specifications."""
        for field_name, value in data.items():
            if value is None:
                continue

            if isinstance(value, list):
                for field_value in value:
                    spec = self._build_field_spec(field_name, field_value)
                    yield spec
            else:
                spec = self._build_field_spec(field_name, value)
                yield spec

    def _build_field_spec(self, field_name: str, value: Any) -> Specification:
        """Build specification for a field name and value."""
        if field_name.endswith("__in"):
            return InSpecification(field_name, value)
        return EqualsSpecification(field_name, value)


class AndSpecificationBuilder(CompositeSpecificationBuilder):
    """And specification builder."""

    def build(self, data: Mapping[str, Any]) -> Specification:
        """Build specification."""
        return AndSpecification(*self._iter_specs(data))


class OrSpecificationBuilder(CompositeSpecificationBuilder):
    """Or specification builder."""

    def build(self, data: Mapping[str, Any]) -> Specification:
        """Build specification."""
        return OrSpecification(*self._iter_specs(data))

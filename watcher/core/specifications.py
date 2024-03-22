"""Specifications."""

import abc
from contextlib import suppress
from typing import Any, Generator, Iterable, Mapping

from django.core.exceptions import ImproperlyConfigured
from django.http import HttpRequest
from django.views import View


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


class ContainsSpecification(Specification):
    """Contains specification.

    Specification that checks if an object contains a value.
    """

    __slots__ = ["field", "value"]

    def __init__(self, field: str, value: Iterable[Any]) -> None:
        """Initialize specification."""
        self.field = field
        self.value = value

    def is_satisfied_by(self, obj: Any) -> bool:
        """Check if the given object satisfies the specification."""
        return self.value in getattr(obj, self.field)


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


class OrSpecification(Specification):
    """Or specification.

    Specification that checks if an object satisfies all child specifications.
    """

    __slots__ = ["specs"]

    def __init__(self, *specs: Iterable[Specification]) -> None:
        """Initialize specification."""
        self.specs = specs

    def is_satisfied_by(self, obj: Any) -> bool:
        """Check if the given object satisfies the specification."""
        return any(spec.is_satisfied_by(obj) for spec in self.specs)


class AtomicSpecificationBuilder(abc.ABC):
    """Atomic specification builder."""

    @abc.abstractmethod
    def build(self, field_name: str, value: Any) -> Specification:
        """Build specification for a given field."""


class FieldSpecificationBuilder(AtomicSpecificationBuilder):
    """Field specification builder."""

    def build(self, field_name: str, value: Any) -> Specification:
        """Build specification for a given field."""
        if field_name.endswith("__in"):
            return InSpecification(field_name.rstrip("__in"), value)
        if field_name.endswith("__contains"):
            return ContainsSpecification(
                field_name.rstrip("__contains"), value
            )
        return EqualsSpecification(field_name, value)


class CompositeSpecificationBuilder(abc.ABC):
    """Composite specification builder."""

    def __init__(self, spec_builder: AtomicSpecificationBuilder):
        """Initialize composite specification builder."""
        self.spec_builder = spec_builder

    @abc.abstractmethod
    def build(self, params: Mapping[str, Any]) -> Specification:
        """Build specification for a field-value mapping."""

    def _iter_specs(
        self, params: Mapping[str, Any]
    ) -> Generator[Specification, None, None]:
        """Iterate specifications."""
        for field_name, value in params.items():
            if value is None:
                continue

            if isinstance(value, list):
                for field_value in value:
                    spec = self.spec_builder.build(field_name, field_value)
                    yield spec
            else:
                spec = self.spec_builder.build(field_name, value)
                yield spec


class AndSpecificationBuilder(CompositeSpecificationBuilder):
    """And specification builder."""

    def build(self, params: Mapping[str, Any]) -> Specification:
        """Build specification for a field-value mapping."""
        return AndSpecification(*self._iter_specs(params))


class OrSpecificationBuilder(CompositeSpecificationBuilder):
    """Or specification builder."""

    def build(self, params: Mapping[str, Any]) -> Specification:
        """Build specification for a field-value mapping."""
        return OrSpecification(*self._iter_specs(params))


class SpecificationBackend:

    @abc.abstractmethod
    def build(self, request: HttpRequest, view: View) -> Specification:
        """Build specification for a request."""


class FieldSpecificationBackend:
    """Field specification backend."""

    def build(self, request: HttpRequest, view: View) -> Specification:
        """Build specification for a request."""
        if not hasattr(view, "get_query_params"):
            raise ImproperlyConfigured(
                "FieldSpecificationBackend requires a 'get_query_params' "
                "method defined in the view class."
            )

        params = view.get_query_params()
        if not params:
            return None

        field_spec_builder = FieldSpecificationBuilder()
        and_spec_builder = AndSpecificationBuilder(field_spec_builder)
        return and_spec_builder.build(params)


class SearchSpecificationBackend:
    """Search specification backend."""
    
    def build(self, request: HttpRequest, view: View) -> Specification:
        """Build specification for a request."""
        search_fields = getattr(view, "search_fields", None)
        if not search_fields:
            raise ImproperlyConfigured(
                "SearchSpecificationBackend requires a 'search_fields' "
                "attribute defined in the view class."
            )

        search = request.GET.get("search")
        if not search:
            return None

        params: dict[str, Any] = {}
        for field, field_type in search_fields.items():
            field_lookup_list = params.setdefault(field, [])
            if isinstance(search, list):
                for value in search:
                    value = self._cast_type(value, field_type)
                    field_lookup_list.append(value)
            else:
                value = self._cast_type(search, field_type)
                field_lookup_list.append(value)

        field_spec_builder = FieldSpecificationBuilder()
        or_spec_builder = OrSpecificationBuilder(field_spec_builder)
        return or_spec_builder.build(params)

    def _cast_type(self, value: Any, field_type: Any) -> Any:
        """Cast lookup value to field type."""
        with suppress(ValueError, TypeError):
            return field_type(value)

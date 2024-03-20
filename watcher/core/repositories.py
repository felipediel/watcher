"""Repositories."""

import abc
import csv
from typing import Generator, Generic, Mapping, TypeVar

from django.core.exceptions import ObjectDoesNotExist
from django.core.files.storage import default_storage

from .specifications import EqualsSpecification, Specification

T = TypeVar("T")


class Repository(Generic[T]):
    """Repository."""

    def __init__(self, context: Mapping | None = None) -> None:
        """Initialize repository."""
        if context is None:
            context = {}
        elif not (
            callable(getattr(context, "keys", None))
            and callable(getattr(context, "__getitem__", None))
        ):
            raise ValueError("'context' must be a mapping or None.")

        self.context: Mapping = context


class ReadRepository(Repository[T], abc.ABC):
    """Read repository."""

    @abc.abstractmethod
    def get_by_id(self, pk: int) -> T:
        """Get item by primary key."""

    @abc.abstractmethod
    def get_all(self, spec: Specification | None = None) -> list[T]:
        """Get all items."""

    @abc.abstractmethod
    def get_dict(self, spec: Specification | None = None) -> dict[int, T]:
        """Get dict of items with their primary keys as indices."""


class ReadCsvRepository(ReadRepository[T]):
    """Read CSV repository."""

    pk_field: str = "id"
    default_file_path: str | None = None

    def __init__(self, context: Mapping | None = None) -> None:
        """Initialize repository."""
        super().__init__(context)
        file_path = self.context.get("file_path") or self.default_file_path
        if not file_path:
            raise ValueError("No 'file_path' provided.")
        self.file_path = file_path

    @abc.abstractmethod
    def _build_item(self, row: dict) -> T:
        """Build item from dict."""

    def iter_items(
        self, spec: Specification | None = None
    ) -> Generator[T, None, None]:
        """Generate items from storage, optionally filtered by a specification."""
        with default_storage.open(self.file_path, mode="r") as file:
            reader = csv.DictReader(file)

            for item_data in reader:
                item = self._build_item(item_data)

                if spec and not spec.is_satisfied_by(item):
                    continue

                yield item

    def get_by_id(self, pk: int) -> T:
        """Get item by primary key."""
        spec = EqualsSpecification(self.pk_field, pk)
        try:
            return next(self.iter_items(spec))
        except StopIteration as err:
            raise ObjectDoesNotExist() from err

    def get_all(self, spec: Specification | None = None) -> list[T]:
        """Get list of items."""
        return list(self.iter_items(spec))

    def get_dict(self, spec: Specification | None = None) -> dict[int, T]:
        """Get dict of items with their primary keys as indices."""
        return {
            getattr(item, self.pk_field): item
            for item in self.iter_items(spec)
        }

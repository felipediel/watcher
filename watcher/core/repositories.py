"""Repositories."""

from __future__ import annotations

import abc
import csv
from typing import Generator, Generic, TypeVar

from django.core.exceptions import ObjectDoesNotExist
from django.core.files.storage import default_storage

from .specifications import EqualsSpecification, Specification

T = TypeVar("T")


class ReadRepository(abc.ABC, Generic[T]):
    """Read repository."""

    @classmethod
    @abc.abstractmethod
    def using(cls, **_) -> ReadRepository:
        """Build repository from config params."""

    @abc.abstractmethod
    def get_by_id(self, pk: int) -> T:
        """Get item by primary key."""

    @abc.abstractmethod
    def get_all(self, spec: Specification | None = None) -> list[T]:
        """Get all items."""

    @abc.abstractmethod
    def get_dict(self, spec: Specification | None = None) -> dict[int, T]:
        """Get dict of items with their primary keys as indices."""


class IterableReadRepository(ReadRepository[T]):
    """Iterable read repository."""

    pk_field: str = "id"

    @abc.abstractmethod
    def iter_items(
        self, spec: Specification | None = None
    ) -> Generator[T, None, None]:
        """Generate items, optionally filtered by a specification."""

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


class CsvReadRepository(IterableReadRepository[T]):
    """CSV read repository."""

    pk_field: str = "id"

    def __init__(self, file_path: str) -> None:
        """Initialize repository."""
        self._file_path = file_path

    @property
    def file_path(self):
        """Return file path."""
        return self._file_path

    @classmethod
    def using(cls, file_path: str | None = None, **_) -> ReadRepository:
        """Build repository from config params."""
        if not file_path:
            raise ValueError("No file path provided.")
        return cls(file_path)

    @abc.abstractmethod
    def build_item(self, data: dict) -> T:
        """Build item from dict."""

    def iter_items(
        self, spec: Specification | None = None
    ) -> Generator[T, None, None]:
        """Generate items, optionally filtered by a specification."""
        with default_storage.open(self.file_path, mode="r") as file:
            reader = csv.DictReader(file)

            for item_data in reader:
                item = self.build_item(item_data)

                if spec and not spec.is_satisfied_by(item):
                    continue

                yield item

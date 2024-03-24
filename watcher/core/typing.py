"""Typing."""

from typing import TypeVar

T = TypeVar("T")

ObjectOrType = T | type[T]

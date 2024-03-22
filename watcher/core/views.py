"""Views."""

from typing import Any

from django.core.exceptions import ImproperlyConfigured
from django.views.generic import ListView

from .repositories import ReadRepository
from .specifications import (
    AndSpecification,
    Specification,
    SpecificationBackend,
)
from .typing import ObjectOrType


class RepositoryListView(ListView):
    """Repository list view."""

    repository_class: type[ReadRepository]
    specification_backends: list[ObjectOrType[SpecificationBackend]] = None

    def get_queryset(self):
        """Get queryset."""
        repository = self.get_repository()
        spec = self.get_specification()
        return repository.get_all(spec)

    def get_repository(self) -> ReadRepository:
        """Get repository."""
        if not hasattr(self, "repository_class"):
            raise ImproperlyConfigured(
                "'repository_class' attribute is not defined"
            )

        config = self.get_repository_config()
        return self.repository_class.using(**config)

    def get_repository_config(self) -> dict[str, Any]:
        """Get repository config."""
        return {}

    def get_specification(self) -> Specification | None:
        """Get specification."""
        if not self.specification_backends:
            return None

        specs: list[Specification] = []
        for backend in self.specification_backends:
            if callable(backend):
                backend = backend()

            spec = backend.build(self.request, self)
            if spec:
                specs.append(spec)

        if not specs:
            return None

        if len(specs) > 1:
            return AndSpecification(*specs)

        return specs[0]

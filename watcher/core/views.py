"""Views."""

from typing import Any

from django.core.exceptions import ImproperlyConfigured
from django.views.generic import ListView

from .repositories import ReadRepository
from .specifications import Specification, SpecificationBuilder


class RepositoryListView(ListView):
    """Repository list view."""

    repository_class: type[ReadRepository]
    spec_builder_class: type[SpecificationBuilder] | None = None

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

    def get_query_params(self) -> dict[str, Any]:
        """Get query parameters."""
        return {}

    def get_specification(self) -> Specification | None:
        """Get specification."""
        if not self.spec_builder_class:
            return None

        query_params = self.get_query_params()
        if not query_params:
            return None

        spec_builder = self.spec_builder_class()
        return spec_builder.build(query_params)

"""Views."""

from django.core.exceptions import ImproperlyConfigured
from django.views.generic import ListView

from .repositories import ReadRepository


class RepositoryListView(ListView):
    """Repository list view."""

    repository_cls: type[ReadRepository]
    repository_ctx: dict | None = None

    def get_queryset(self):
        """Get queryset."""
        repository = self.get_repository()
        return repository.get_all()

    def get_repository(self) -> ReadRepository:
        """Get repository."""
        if not hasattr(self, "repository_cls"):
            raise ImproperlyConfigured(
                "'repository_cls' attribute is not defined"
            )

        repository_ctx = self.get_repository_context()
        return self.repository_cls(context=repository_ctx)

    def get_repository_context(self) -> dict | None:
        """Get repository context."""
        return self.repository_ctx

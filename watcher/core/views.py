"""Views."""

from django.core.exceptions import ImproperlyConfigured
from django.views.generic import ListView

from .repositories import ReadRepository


class RepositoryListView(ListView):
    """Repository list view."""

    repository_class: type[ReadRepository]

    def get_queryset(self):
        """Get queryset."""
        repository = self.get_repository()
        return repository.get_all()

    def get_repository(self) -> ReadRepository:
        """Get repository."""
        if not hasattr(self, "repository_class"):
            raise ImproperlyConfigured(
                "'repository_class' attribute is not defined"
            )

        config = self.get_repository_config()
        return self.repository_class.using(**config)

    def get_repository_config(self) -> dict:
        """Get repository config."""
        return {}

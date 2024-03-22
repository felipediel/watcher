"""Views."""

from typing import Any

from django.conf import settings
from django.views.generic import ListView

from watcher.core.forms import SearchForm
from watcher.core.specifications import (
    FieldSpecificationBackend,
    SearchSpecificationBackend,
)
from watcher.core.views import RepositoryListView

from .schemas import (
    BillQueryParams,
    PersonQueryParams,
    VoteQueryParams,
    VoteResultQueryParams,
)
from .services import BillVoteSummaryService, LegislatorVoteSummaryService
from .repositories import (
    BillCsvRepository,
    LegislatorCsvRepository,
    VoteCsvRepository,
    VoteResultCsvRepository,
)


class LegislatorListView(RepositoryListView):
    """Legislator list view."""

    paginate_by = 15
    form_class = SearchForm
    repository_class = LegislatorCsvRepository
    specification_backends = [
        FieldSpecificationBackend,
        SearchSpecificationBackend,
    ]
    template_name = "legislator_list.html"
    search_fields = {
        "id": int,
        "name": str,
        "name__contains": str,
    }

    def get_repository_config(self) -> dict[str, Any]:
        """Get repository config."""
        return {"file_path": settings.MEDIA_FILES["legislators"]}

    def get_query_params(self) -> dict[str, Any]:
        """Get query parameters."""
        return PersonQueryParams(**self.request.GET).model_dump()


class BillListView(RepositoryListView):
    """Bill list view."""

    paginate_by = 15
    form_class = SearchForm
    repository_class = BillCsvRepository
    specification_backends = [
        FieldSpecificationBackend,
        SearchSpecificationBackend,
    ]
    template_name = "bill_list.html"
    search_fields = {
        "id": int,
        "title": str,
        "title__contains": str,
        "sponsor_id": int,
    }

    def get_repository_config(self) -> dict[str, Any]:
        """Get repository config."""
        return {"file_path": settings.MEDIA_FILES["bills"]}

    def get_query_params(self) -> dict[str, Any]:
        """Get query parameters."""
        return BillQueryParams(**self.request.GET).model_dump()


class VoteListView(RepositoryListView):
    """Vote list view."""

    paginate_by = 15
    form_class = SearchForm
    repository_class = VoteCsvRepository
    specification_backends = [
        FieldSpecificationBackend,
        SearchSpecificationBackend,
    ]
    template_name = "vote_list.html"
    search_fields = {"id": int, "bill_id": int}

    def get_repository_config(self) -> dict[str, Any]:
        """Get repository config."""
        return {"file_path": settings.MEDIA_FILES["votes"]}

    def get_query_params(self) -> dict[str, Any]:
        """Get query parameters."""
        return VoteQueryParams(**self.request.GET).model_dump()


class VoteResultListView(RepositoryListView):
    """Vote result list view."""

    paginate_by = 15
    form_class = SearchForm
    repository_class = VoteResultCsvRepository
    specification_backends = [
        FieldSpecificationBackend,
        SearchSpecificationBackend,
    ]
    template_name = "vote_result_list.html"
    search_fields = {
        "id": int,
        "legislator_id": int,
        "vote_id": int,
        "vote_type": int,
    }

    def get_repository_config(self) -> dict[str, Any]:
        """Get repository config."""
        return {"file_path": settings.MEDIA_FILES["vote_results"]}

    def get_query_params(self) -> dict[str, Any]:
        """Get query parameters."""
        return VoteResultQueryParams(**self.request.GET).model_dump()


class LegislatorVoteSummaryListView(ListView):
    """Legislator vote summary list view."""

    paginate_by = 15
    template_name = "legislator_vote_summary_list.html"

    def get_queryset(self):
        """Get queryset."""
        service = self.get_service()
        vote_summary = service.summarize_votes()
        return vote_summary

    def get_service(self) -> LegislatorVoteSummaryService:
        """Get service."""
        vote_result_repository = VoteResultCsvRepository.using(
            file_path=settings.MEDIA_FILES["vote_results"]
        )
        vote_repository = VoteCsvRepository.using(
            file_path=settings.MEDIA_FILES["votes"]
        )
        legislator_repository = LegislatorCsvRepository.using(
            file_path=settings.MEDIA_FILES["legislators"]
        )
        service = LegislatorVoteSummaryService(
            vote_repository=vote_repository,
            vote_result_repository=vote_result_repository,
            legislator_repository=legislator_repository,
        )
        return service


class BillVoteSummaryListView(ListView):
    """Bill vote summary list view."""

    paginate_by = 15
    template_name = "bill_vote_summary_list.html"

    def get_queryset(self):
        """Get queryset."""
        service = self.get_service()
        bill_vote_summary = service.summarize_votes()
        return bill_vote_summary

    def get_service(self) -> BillVoteSummaryService:
        """Get service."""
        vote_repository = VoteCsvRepository.using(
            file_path=settings.MEDIA_FILES["votes"]
        )
        vote_result_repository = VoteResultCsvRepository.using(
            file_path=settings.MEDIA_FILES["vote_results"]
        )
        bill_repository = BillCsvRepository.using(
            file_path=settings.MEDIA_FILES["bills"]
        )
        legislator_repository = LegislatorCsvRepository.using(
            file_path=settings.MEDIA_FILES["legislators"]
        )
        service = BillVoteSummaryService(
            vote_repository=vote_repository,
            vote_result_repository=vote_result_repository,
            bill_repository=bill_repository,
            legislator_repository=legislator_repository,
        )
        return service

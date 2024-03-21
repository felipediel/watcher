"""Views."""

from django.conf import settings
from django.views.generic import ListView

from watcher.core.views import RepositoryListView

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
    repository_class = LegislatorCsvRepository
    template_name = "legislator_list.html"

    def get_repository_config(self) -> dict:
        """Get repository config."""
        return {"file_path": settings.MEDIA_FILES["legislators"]}


class BillListView(RepositoryListView):
    """Bill list view."""

    paginate_by = 15
    repository_class = BillCsvRepository
    template_name = "bill_list.html"

    def get_repository_config(self) -> dict:
        """Get repository config."""
        return {"file_path": settings.MEDIA_FILES["bills"]}


class VoteListView(RepositoryListView):
    """Vote list view."""

    paginate_by = 15
    repository_class = VoteCsvRepository
    template_name = "vote_list.html"

    def get_repository_config(self) -> dict:
        """Get repository config."""
        return {"file_path": settings.MEDIA_FILES["votes"]}


class VoteResultListView(RepositoryListView):
    """Vote result list view."""

    paginate_by = 15
    repository_class = VoteResultCsvRepository
    template_name = "vote_result_list.html"

    def get_repository_config(self) -> dict:
        """Get repository config."""
        return {"file_path": settings.MEDIA_FILES["vote_results"]}


class LegislatorVoteSummaryListView(ListView):
    """Legislator vote summary list view."""

    paginate_by = 15
    template_name = "legislator_vote_summary_list.html"

    def get_queryset(self):
        """Get queryset."""
        vote_result_repository = VoteResultCsvRepository.using(
            file_path=settings.MEDIA_FILES["vote_results"]
        )
        legislator_repository = LegislatorCsvRepository.using(
            file_path=settings.MEDIA_FILES["legislators"]
        )
        service = LegislatorVoteSummaryService()

        vote_summary = service.summarize_votes(
            vote_result_repository=vote_result_repository,
            legislator_repository=legislator_repository,
        )
        return vote_summary


class BillVoteSummaryListView(ListView):
    """Bill vote summary list view."""

    paginate_by = 15
    template_name = "bill_vote_summary_list.html"

    def get_queryset(self):
        """Get queryset."""
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
        service = BillVoteSummaryService()

        bill_vote_summary = service.summarize_votes(
            vote_repository=vote_repository,
            vote_result_repository=vote_result_repository,
            bill_repository=bill_repository,
            legislator_repository=legislator_repository,
        )
        return bill_vote_summary

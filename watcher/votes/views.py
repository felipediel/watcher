"""Views."""

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
    repository_cls = LegislatorCsvRepository
    template_name = "legislator_list.html"


class BillListView(RepositoryListView):
    """Bill list view."""

    paginate_by = 15
    repository_cls = BillCsvRepository
    template_name = "bill_list.html"


class VoteListView(RepositoryListView):
    """Vote list view."""

    paginate_by = 15
    repository_cls = VoteCsvRepository
    template_name = "vote_list.html"


class VoteResultListView(RepositoryListView):
    """Vote result list view."""

    paginate_by = 15
    repository_cls = VoteResultCsvRepository
    template_name = "vote_result_list.html"


class LegislatorVoteSummaryListView(ListView):
    """Legislator vote summary list view."""

    paginate_by = 15
    template_name = "legislator_vote_summary_list.html"

    def get_queryset(self):
        """Get queryset."""
        vote_result_repository = VoteResultCsvRepository()
        legislator_repository = LegislatorCsvRepository()
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
        vote_repository = VoteCsvRepository()
        vote_result_repository = VoteResultCsvRepository()
        bill_repository = BillCsvRepository()
        legislator_repository = LegislatorCsvRepository()
        service = BillVoteSummaryService()

        bill_vote_summary = service.summarize_votes(
            vote_repository=vote_repository,
            vote_result_repository=vote_result_repository,
            bill_repository=bill_repository,
            legislator_repository=legislator_repository,
        )
        return bill_vote_summary

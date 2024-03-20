"""Views."""

from watcher.core.views import RepositoryListView
from watcher.votes.repositories import (
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

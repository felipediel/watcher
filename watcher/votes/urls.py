"""URLs."""

from django.urls import path, include

from .views import (
    BillListView,
    BillVoteSummaryListView,
    LegislatorListView,
    LegislatorVoteSummaryListView,
    VoteListView,
    VoteResultListView,
)

app_name = "votes"

dataset_urls = [
    path("legislators/", LegislatorListView.as_view(), name="legislator-list"),
    path("bills/", BillListView.as_view(), name="bill-list"),
    path("votes/", VoteListView.as_view(), name="vote-list"),
    path(
        "vote_results/", VoteResultListView.as_view(), name="vote-result-list"
    ),
]

summary_urls = [
    path(
        "legislators_votes/",
        LegislatorVoteSummaryListView.as_view(),
        name="legislator-vote-summary-list",
    ),
    path(
        "bills_votes/",
        BillVoteSummaryListView.as_view(),
        name="bill-vote-summary-list",
    ),
]

urlpatterns = [
    path("summaries/", include(summary_urls)),
    path("datasets/", include(dataset_urls)),
]

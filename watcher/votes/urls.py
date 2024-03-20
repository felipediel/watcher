"""URLs."""

from django.urls import path, include

from .views import (
    BillListView,
    LegislatorListView,
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
    path("legislators_votes/", LegislatorListView.as_view(), name="legislators-votes-list"),
    path("bills_votes/", BillListView.as_view(), name="bills-votes-list"),
]

urlpatterns = [
    path("summaries/", include(summary_urls)),
    path("datasets/", include(dataset_urls)),
]

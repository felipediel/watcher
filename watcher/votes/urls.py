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

urlpatterns = [path("datasets/", include(dataset_urls))]

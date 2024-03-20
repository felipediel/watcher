"""Repositories."""

from django.conf import settings

from watcher.core.repositories import ReadCsvRepository

from .enum import VoteType
from .models import Bill, Vote, VoteResult, Person


class LegislatorCsvRepository(ReadCsvRepository[Person]):
    """Legislator CSV repository."""

    default_file_path = settings.LEGISLATORS_CSV

    def _build_item(self, row: dict) -> Person:
        """Build item from dict."""
        return Person(id=int(row["id"]), name=row["name"])


class BillCsvRepository(ReadCsvRepository[Bill]):
    """Bill CSV repository."""

    default_file_path = settings.BILLS_CSV

    def _build_item(self, row: dict) -> Bill:
        """Build item from dict."""
        return Bill(
            id=int(row["id"]),
            title=row["title"],
            sponsor_id=int(row["sponsor_id"]),
        )


class VoteCsvRepository(ReadCsvRepository[Vote]):
    """Vote CSV repository."""

    default_file_path = settings.VOTES_CSV

    def _build_item(self, row: dict) -> Vote:
        """Build item from dict."""
        return Vote(id=int(row["id"]), bill_id=int(row["bill_id"]))


class VoteResultCsvRepository(ReadCsvRepository[VoteResult]):
    """Vote result CSV repository."""

    default_file_path = settings.VOTE_RESULTS_CSV

    def _build_item(self, row: dict) -> VoteResult:
        """Build item from dict."""
        return VoteResult(
            id=int(row["id"]),
            legislator_id=int(row["legislator_id"]),
            vote_id=int(row["vote_id"]),
            vote_type=VoteType(int(row["vote_type"])),
        )

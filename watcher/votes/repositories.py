"""Repositories."""

from watcher.core.repositories import CsvReadRepository

from .enum import VoteType
from .models import Bill, Vote, VoteResult, Person


class LegislatorCsvRepository(CsvReadRepository[Person]):
    """Legislator CSV repository."""

    def build_item(self, data: dict) -> Person:
        """Build item from dict."""
        return Person(id=int(data["id"]), name=data["name"])


class BillCsvRepository(CsvReadRepository[Bill]):
    """Bill CSV repository."""

    def build_item(self, data: dict) -> Bill:
        """Build item from dict."""
        return Bill(
            id=int(data["id"]),
            title=data["title"],
            sponsor_id=int(data["sponsor_id"]),
        )


class VoteCsvRepository(CsvReadRepository[Vote]):
    """Vote CSV repository."""

    def build_item(self, data: dict) -> Vote:
        """Build item from dict."""
        return Vote(id=int(data["id"]), bill_id=int(data["bill_id"]))


class VoteResultCsvRepository(CsvReadRepository[VoteResult]):
    """Vote result CSV repository."""

    def build_item(self, data: dict) -> VoteResult:
        """Build item from dict."""
        return VoteResult(
            id=int(data["id"]),
            legislator_id=int(data["legislator_id"]),
            vote_id=int(data["vote_id"]),
            vote_type=VoteType(int(data["vote_type"])),
        )

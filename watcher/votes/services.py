"""Services."""

import logging

from watcher.core.repositories import ReadRepository
from watcher.core.specifications import Specification

from .enum import VoteType
from .models import (
    Bill,
    BillVoteSummary,
    LegislatorVoteSummary,
    Person,
    Vote,
    VoteResult,
)

_LOGGER = logging.getLogger(__name__)


class LegislatorVoteSummaryService:
    """Legislator vote summary service."""

    def __init__(
        self,
        vote_repository: ReadRepository[Vote],
        vote_result_repository: ReadRepository[VoteResult],
        legislator_repository: ReadRepository[Person],
    ) -> None:
        """Initialize service."""
        self.vote_repository = vote_repository
        self.vote_result_repository = vote_result_repository
        self.legislator_repository = legislator_repository

    def summarize_votes(
        self, spec: Specification | None = None
    ) -> list[LegislatorVoteSummary]:
        """Summarize vote results into legislator vote summary list."""
        vote_result_list = self.vote_result_repository.get_all()
        vote_dict = self.vote_repository.get_dict()
        legislator_dict = self.legislator_repository.get_dict()
        legislator_vote_dict: dict[int, tuple[set[int], set[int]]] = {}
        vote_summary_list: list[LegislatorVoteSummary] = []

        for vote_result in vote_result_list:
            try:
                vote = vote_dict[vote_result.vote_id]
            except KeyError:
                _LOGGER.debug("Vote not found: %s", vote_result.vote_id)
                continue

            supported_bills, opposed_bills = legislator_vote_dict.setdefault(
                vote_result.legislator_id, (set(), set())
            )

            if vote_result.vote_type == VoteType.YES:
                supported_bills.add(vote.bill_id)
            else:
                opposed_bills.add(vote.bill_id)

        for legislator_id, legislator_votes in legislator_vote_dict.items():
            try:
                legislator = legislator_dict[legislator_id]
                legislator_name = legislator.name
            except KeyError:
                _LOGGER.debug(
                    "Legislator not found: %s", vote_result.legislator_id
                )
                legislator_name = "N/A"

            supported_bills, opposed_bills = legislator_votes
            vote_summary = LegislatorVoteSummary(
                legislator_id=legislator_id,
                legislator_name=legislator_name,
                supported_bills=len(supported_bills),
                opposed_bills=len(opposed_bills),
            )

            if spec and not spec.is_satisfied_by(vote_summary):
                continue

            vote_summary_list.append(vote_summary)

        return vote_summary_list


class BillVoteSummaryService:
    """Bill vote summary service."""

    def __init__(
        self,
        vote_repository: ReadRepository[Vote],
        vote_result_repository: ReadRepository[VoteResult],
        bill_repository: ReadRepository[Bill],
        legislator_repository: ReadRepository[Person],
    ) -> None:
        """Initialize service."""
        self.vote_repository = vote_repository
        self.vote_result_repository = vote_result_repository
        self.bill_repository = bill_repository
        self.legislator_repository = legislator_repository

    def summarize_votes(
        self, spec: Specification | None = None
    ) -> list[BillVoteSummary]:
        """Summarize vote results into bill vote summary list."""
        vote_summary_dict: dict[int, BillVoteSummary] = {}
        vote_dict = self.vote_repository.get_dict()
        vote_result_list = self.vote_result_repository.get_all()
        bill_dict = self.bill_repository.get_dict()
        legislator_dict = self.legislator_repository.get_dict()

        for vote_result in vote_result_list:
            try:
                vote = vote_dict[vote_result.vote_id]
            except KeyError:
                _LOGGER.debug("Vote not found: %s", vote_result.vote_id)
                continue

            try:
                bill = bill_dict[vote.bill_id]
                bill_id = bill.id
                bill_title = bill.title
            except KeyError:
                _LOGGER.debug("Bill not found: %s", vote.bill_id)
                bill_id = vote.bill_id
                bill_title = "N/A"
                sponsor_id = None
                sponsor_name = "N/A"
            else:
                try:
                    sponsor = legislator_dict[bill.sponsor_id]
                    sponsor_id = sponsor.id
                    sponsor_name = sponsor.name
                except KeyError:
                    _LOGGER.debug("Sponsor not found: %s", bill.sponsor_id)
                    sponsor_id = bill.sponsor_id
                    sponsor_name = "N/A"

            try:
                vote_summary = vote_summary_dict[bill_id]
            except KeyError:
                vote_summary = BillVoteSummary(
                    bill_id=bill_id,
                    bill_title=bill_title,
                    sponsor_id=sponsor_id,
                    sponsor_name=sponsor_name,
                )
                vote_summary_dict[bill_id] = vote_summary

            if vote_result.vote_type == VoteType.YES:
                vote_summary.supporters += 1
            else:
                vote_summary.opposers += 1

        if spec:
            return [
                vote_summary
                for vote_summary in vote_summary_dict.values()
                if spec.is_satisfied_by(vote_summary)
            ]

        return list(vote_summary_dict.values())

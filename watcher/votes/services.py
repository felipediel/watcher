"""Services."""

import logging

from watcher.core.repositories import ReadRepository

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

    def summarize_votes(
        self,
        vote_result_repository: ReadRepository[VoteResult],
        legislator_repository: ReadRepository[Person],
    ) -> list[LegislatorVoteSummary]:
        """Summarize vote results into legislator vote summary list."""
        vote_summary_dict: dict[int, LegislatorVoteSummary] = {}

        vote_result_list = vote_result_repository.get_all()
        legislator_dict = legislator_repository.get_dict()

        for vote_result in vote_result_list:
            try:
                legislator = legislator_dict[vote_result.legislator_id]
                legislator_id = legislator.id
                legislator_name = legislator.name
            except KeyError:
                _LOGGER.debug(
                    "Legislator not found: %s", vote_result.legislator_id
                )
                legislator_id = vote_result.legislator_id
                legislator_name = "N/A"

            try:
                vote_summary = vote_summary_dict[legislator_id]
            except KeyError:
                vote_summary = LegislatorVoteSummary(
                    legislator_id=legislator_id,
                    legislator_name=legislator_name,
                )
                vote_summary_dict[legislator_id] = vote_summary

            if vote_result.vote_type == VoteType.YES:
                vote_summary.supported_bills += 1
            else:
                vote_summary.opposed_bills += 1

        return list(vote_summary_dict.values())


class BillVoteSummaryService:
    """Bill vote summary service."""

    def summarize_votes(
        self,
        vote_repository: ReadRepository[Vote],
        vote_result_repository: ReadRepository[VoteResult],
        bill_repository: ReadRepository[Bill],
        legislator_repository: ReadRepository[Person],
    ) -> list[BillVoteSummary]:
        """Summarize vote results into bill vote summary list."""
        vote_summary_dict: dict[int, BillVoteSummary] = {}
        vote_dict = vote_repository.get_dict()
        vote_result_list = vote_result_repository.get_all()
        bill_dict = bill_repository.get_dict()
        legislator_dict = legislator_repository.get_dict()

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

        return list(vote_summary_dict.values())

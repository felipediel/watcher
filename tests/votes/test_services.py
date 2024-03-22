"""Tests for services."""

from django.test import override_settings

from watcher.votes.repositories import (
    BillCsvRepository,
    LegislatorCsvRepository,
    VoteCsvRepository,
    VoteResultCsvRepository,
)
from watcher.votes.services import (
    BillVoteSummaryService,
    LegislatorVoteSummaryService,
)

from tests.common import BaseTestCase

MEDIA_ROOT = "tests/samples/media"


@override_settings(MEDIA_ROOT=MEDIA_ROOT)
class TestLegislatorVoteSummaryService(BaseTestCase):
    """Tests for legislator vote summary service."""

    def setUp(self):
        """Set up test data."""
        vote_results_file_path = "csv/vote_results_md.csv"
        votes_file_path = "csv/votes_md.csv"
        legislators_file_path = "csv/legislators_md.csv"
        vote_repository = VoteCsvRepository(votes_file_path)
        vote_result_repository = VoteResultCsvRepository(
            vote_results_file_path
        )
        legislator_repository = LegislatorCsvRepository(legislators_file_path)
        self.vote_summary_service = LegislatorVoteSummaryService(
            vote_repository=vote_repository,
            vote_result_repository=vote_result_repository,
            legislator_repository=legislator_repository,
        )

    def test_summarize_votes(self):
        """Test summarize votes."""
        vote_summary_list = self.vote_summary_service.summarize_votes()

        self.assertIsInstance(vote_summary_list, list)
        self.assertEqual(len(vote_summary_list), 3)

        find_item = (
            item
            for item in vote_summary_list
            if getattr(item, "legislator_id") == 400440
        )
        item1 = next(find_item, None)
        self.assertIsNotNone(item1)
        self.assertAttrEqual(item1, "legislator_name", "Rep. Don Young (R-AK-1)")
        self.assertAttrEqual(item1, "supported_bills", 1)
        self.assertAttrEqual(item1, "opposed_bills", 2)

        find_item = (
            item
            for item in vote_summary_list
            if getattr(item, "legislator_id") == 412393
        )
        item2 = next(find_item, None)
        self.assertAttrEqual(item2, "legislator_name", "Rep. Tom Reed (R-NY-23)")
        self.assertAttrEqual(item2, "supported_bills", 0)
        self.assertAttrEqual(item2, "opposed_bills", 3)

        find_item = (
            item
            for item in vote_summary_list
            if getattr(item, "legislator_id") == 412421
        )
        item3 = next(find_item, None)
        self.assertAttrEqual(item3, "legislator_name", "Rep. Adam Kinzinger (R-IL-16)")
        self.assertAttrEqual(item3, "supported_bills", 2)
        self.assertAttrEqual(item3, "opposed_bills", 0)


@override_settings(MEDIA_ROOT=MEDIA_ROOT)
class TestBillVoteSummaryService(BaseTestCase):
    """Tests for bill vote summary service."""

    def setUp(self):
        """Set up test data."""
        vote_results_file_path = "csv/vote_results_md.csv"
        votes_file_path = "csv/votes_md.csv"
        bills_file_path = "csv/bills_md.csv"
        legislators_file_path = "csv/legislators_md.csv"
        vote_result_repository = VoteResultCsvRepository(
            vote_results_file_path
        )
        vote_repository = VoteCsvRepository(votes_file_path)
        bill_repository = BillCsvRepository(bills_file_path)
        legislator_repository = LegislatorCsvRepository(legislators_file_path)
        self.vote_summary_service = BillVoteSummaryService(
            vote_result_repository=vote_result_repository,
            vote_repository=vote_repository,
            bill_repository=bill_repository,
            legislator_repository=legislator_repository,
        )

    def test_summarize_votes(self):
        """Test summarize votes."""
        vote_summary_list = self.vote_summary_service.summarize_votes()

        self.assertIsInstance(vote_summary_list, list)
        self.assertEqual(len(vote_summary_list), 3)

        find_item = (
            item
            for item in vote_summary_list
            if getattr(item, "bill_id") == 2952375
        )
        item1 = next(find_item, None)
        self.assertIsNotNone(item1)
        self.assertAttrEqual(item1, "bill_title", "H.R. 5376: Build Back Better Act")
        self.assertAttrEqual(item1, "sponsor_id", 412211)
        self.assertAttrEqual(item1, "sponsor_name", "Rep. John Yarmuth (D-KY-3)")
        self.assertAttrEqual(item1, "supporters", 2)
        self.assertAttrEqual(item1, "opposers", 1)

        find_item = (
            item
            for item in vote_summary_list
            if getattr(item, "bill_id") == 2900994
        )
        item2 = next(find_item, None)
        self.assertIsNotNone(item2)
        self.assertAttrEqual(item2, "bill_title", "H.R. 3684: Infrastructure Investment and Jobs Act")
        self.assertAttrEqual(item2, "sponsor_id", 400100)
        self.assertAttrEqual(item2, "sponsor_name", "N/A")
        self.assertAttrEqual(item2, "supporters", 2)
        self.assertAttrEqual(item2, "opposers", 3)

        find_item = (
            item
            for item in vote_summary_list
            if getattr(item, "bill_id") == 3568720
        )
        item3 = next(find_item, None)
        self.assertIsNotNone(item3)
        self.assertAttrEqual(item3, "bill_title", "H.R. 7623: Telehealth Modernization Act of 2024")
        self.assertAttrEqual(item3, "sponsor_id", 17941)
        self.assertAttrEqual(item3, "sponsor_name", "Rep. Jeff Van Drew (R-NJ-2)")
        self.assertAttrEqual(item3, "supporters", 0)
        self.assertAttrEqual(item3, "opposers", 2)

"""Tests for repositories."""

from django.test import override_settings

from watcher.votes.repositories import (
    BillCsvRepository,
    LegislatorCsvRepository,
    VoteCsvRepository,
    VoteResultCsvRepository,
)

from tests.common import BaseTestCase

MEDIA_ROOT = "tests/samples/media"


@override_settings(MEDIA_ROOT=MEDIA_ROOT)
class TestLegislatorCsvRepository(BaseTestCase):
    """Tests for legislators CSV repository."""

    def setUp(self):
        """Set up test data."""
        file_path = "csv/legislators_sm.csv"
        self.repository = LegislatorCsvRepository(file_path)

    def test_build_item(self):
        """Test build item."""
        sample_data = {
            "id": 904789,
            "name": "Rep. Don Bacon (R-NE-2)",
        }
        item = self.repository.build_item(sample_data)

        self.assertAttrEqual(item, "id", 904789)
        self.assertAttrEqual(item, "name", "Rep. Don Bacon (R-NE-2)")

    def test_iter_items(self):
        """Test iter items."""
        items = self.repository.iter_items()

        item1 = self.getItemFromList(items, "id", 904789)
        self.assertAttrEqual(item1, "name", "Rep. Don Bacon (R-NE-2)")

        item2 = self.getItemFromList(items, "id", 1603850)
        self.assertAttrEqual(item2, "name", "Rep. Jamaal Bowman (D-NY-16)")

    def test_get_all(self):
        """Test get list of items."""
        items = self.repository.get_all()

        self.assertIsInstance(items, list)
        self.assertEqual(len(items), 2)

        item1 = items[0]
        self.assertAttrEqual(item1, "id", 904789)
        self.assertAttrEqual(item1, "name", "Rep. Don Bacon (R-NE-2)")

        item2 = items[1]
        self.assertAttrEqual(item2, "id", 1603850)
        self.assertAttrEqual(item2, "name", "Rep. Jamaal Bowman (D-NY-16)")

    def test_get_dict(self):
        """Test get dict of items."""
        items = self.repository.get_dict()

        self.assertIsInstance(items, dict)
        self.assertEqual(len(items), 2)

        self.assertIn(904789, items)
        item1 = items[904789]
        self.assertAttrEqual(item1, "id", 904789)
        self.assertAttrEqual(item1, "name", "Rep. Don Bacon (R-NE-2)")

        self.assertIn(1603850, items)
        item2 = items[1603850]
        self.assertAttrEqual(item2, "id", 1603850)
        self.assertAttrEqual(item2, "name", "Rep. Jamaal Bowman (D-NY-16)")


@override_settings(MEDIA_ROOT=MEDIA_ROOT)
class TestBillCsvRepository(BaseTestCase):
    """Tests for bill CSV repository."""

    def setUp(self):
        """Set up test data."""
        file_path = "csv/bills_sm.csv"
        self.repository = BillCsvRepository(file_path)

    def test_build_item(self):
        """Test build item."""
        sample_data = {
            "id": 2952375,
            "title": "H.R. 5376: Build Back Better Act",
            "sponsor_id": 412211,
        }
        item = self.repository.build_item(sample_data)

        self.assertAttrEqual(item, "id", 2952375)
        self.assertAttrEqual(item, "title", "H.R. 5376: Build Back Better Act")
        self.assertAttrEqual(item, "sponsor_id", 412211)

    def test_iter_items(self):
        """Test iter items."""
        items = self.repository.iter_items()

        item1 = self.getItemFromList(items, "id", 2952375)
        self.assertAttrEqual(item1, "title", "H.R. 5376: Build Back Better Act")
        self.assertAttrEqual(item1, "sponsor_id", 412211)

        item2 = self.getItemFromList(items, "id", 2900994)
        self.assertAttrEqual(item2, "title", "H.R. 3684: Infrastructure Investment and Jobs Act")
        self.assertAttrEqual(item2, "sponsor_id", 400100)

    def test_get_all(self):
        """Test get list of items."""
        items = self.repository.get_all()

        self.assertIsInstance(items, list)
        self.assertEqual(len(items), 2)

        item1 = items[0]
        self.assertAttrEqual(item1, "id", 2952375)
        self.assertAttrEqual(item1, "title", "H.R. 5376: Build Back Better Act")
        self.assertAttrEqual(item1, "sponsor_id", 412211)

        item2 = items[1]
        self.assertAttrEqual(item2, "id", 2900994)
        self.assertAttrEqual(item2, "title", "H.R. 3684: Infrastructure Investment and Jobs Act")
        self.assertAttrEqual(item2, "sponsor_id", 400100)

    def test_get_dict(self):
        """Test get dict of items."""
        items = self.repository.get_dict()

        self.assertIsInstance(items, dict)
        self.assertEqual(len(items), 2)

        self.assertIn(2952375, items)
        item1 = items[2952375]
        self.assertAttrEqual(item1, "id", 2952375)
        self.assertAttrEqual(item1, "title", "H.R. 5376: Build Back Better Act")
        self.assertAttrEqual(item1, "sponsor_id", 412211)

        self.assertIn(2900994, items)
        item2 = items[2900994]
        self.assertAttrEqual(item2, "id", 2900994)
        self.assertAttrEqual(item2, "title", "H.R. 3684: Infrastructure Investment and Jobs Act")
        self.assertAttrEqual(item2, "sponsor_id", 400100)


@override_settings(MEDIA_ROOT=MEDIA_ROOT)
class TestVoteCsvRepository(BaseTestCase):
    """Tests for vote CSV repository."""

    def setUp(self):
        """Set up test data."""
        file_path = "csv/votes_sm.csv"
        self.repository = VoteCsvRepository(file_path)

    def test_build_item(self):
        """Test build item."""
        sample_data = {
            "id": 3314452,
            "bill_id": 2900994,
        }
        item = self.repository.build_item(sample_data)

        self.assertAttrEqual(item, "id", 3314452)
        self.assertAttrEqual(item, "bill_id", 2900994)

    def test_iter_items(self):
        """Test iter items."""
        items = self.repository.iter_items()

        item1 = self.getItemFromList(items, "id", 3314452)
        self.assertAttrEqual(item1, "bill_id", 2900994)

        item2 = self.getItemFromList(items, "id", 3321166)
        self.assertAttrEqual(item2, "bill_id", 2952375)

    def test_get_all(self):
        """Test get list of items."""
        items = self.repository.get_all()

        self.assertIsInstance(items, list)
        self.assertEqual(len(items), 2)

        item1 = items[0]
        self.assertAttrEqual(item1, "id", 3314452)
        self.assertAttrEqual(item1, "bill_id", 2900994)

        item2 = items[1]
        self.assertAttrEqual(item2, "id", 3321166)
        self.assertAttrEqual(item2, "bill_id", 2952375)

    def test_get_dict(self):
        """Test get dict of items."""
        items = self.repository.get_dict()

        self.assertIsInstance(items, dict)
        self.assertEqual(len(items), 2)

        self.assertIn(3314452, items)
        item1 = items[3314452]
        self.assertAttrEqual(item1, "id", 3314452)
        self.assertAttrEqual(item1, "bill_id", 2900994)

        self.assertIn(3321166, items)
        item2 = items[3321166]
        self.assertAttrEqual(item2, "id", 3321166)
        self.assertAttrEqual(item2, "bill_id", 2952375)


@override_settings(MEDIA_ROOT=MEDIA_ROOT)
class TestVoteResultCsvRepository(BaseTestCase):
    """Tests for vote result CSV repository."""

    def setUp(self):
        """Set up test data."""
        file_path = "csv/vote_results_sm.csv"
        self.repository = VoteResultCsvRepository(file_path)

    def test_build_item(self):
        """Test build item."""
        sample_data = {
            "id": 92516553,
            "legislator_id": 1269790,
            "vote_id": 3321166,
            "vote_type": 1,
        }
        item = self.repository.build_item(sample_data)

        self.assertAttrEqual(item, "id", 92516553)
        self.assertAttrEqual(item, "legislator_id", 1269790)
        self.assertAttrEqual(item, "vote_id", 3321166)
        self.assertAttrEqual(item, "vote_type", 1)

    def test_iter_items(self):
        """Test iter items."""
        items = self.repository.iter_items()

        item1 = self.getItemFromList(items, "id", 92516553)
        self.assertAttrEqual(item1, "legislator_id", 1269790)
        self.assertAttrEqual(item1, "vote_id", 3321166)
        self.assertAttrEqual(item1, "vote_type", 1)

        item2 = self.getItemFromList(items, "id", 92516784)
        self.assertAttrEqual(item2, "legislator_id", 400440)
        self.assertAttrEqual(item2, "vote_id", 3321166)
        self.assertAttrEqual(item2, "vote_type", 2)

    def test_get_all(self):
        """Test get list of items."""
        items = self.repository.get_all()

        self.assertIsInstance(items, list)
        self.assertEqual(len(items), 2)

        item1 = self.getItemFromList(items, "id", 92516553)
        self.assertAttrEqual(item1, "id", 92516553)
        self.assertAttrEqual(item1, "legislator_id", 1269790)
        self.assertAttrEqual(item1, "vote_id", 3321166)
        self.assertAttrEqual(item1, "vote_type", 1)

        item2 = self.getItemFromList(items, "id", 92516784)
        self.assertAttrEqual(item2, "legislator_id", 400440)
        self.assertAttrEqual(item2, "vote_id", 3321166)
        self.assertAttrEqual(item2, "vote_type", 2)

    def test_get_dict(self):
        """Test get dict of items."""
        items = self.repository.get_dict()

        self.assertIsInstance(items, dict)
        self.assertEqual(len(items), 2)

        self.assertIn(92516553, items)
        item1 = items[92516553]
        self.assertAttrEqual(item1, "id", 92516553)
        self.assertAttrEqual(item1, "legislator_id", 1269790)
        self.assertAttrEqual(item1, "vote_id", 3321166)
        self.assertAttrEqual(item1, "vote_type", 1)

        self.assertIn(92516784, items)
        item2 = items[92516784]
        self.assertAttrEqual(item2, "id", 92516784)
        self.assertAttrEqual(item2, "legislator_id", 400440)
        self.assertAttrEqual(item2, "vote_id", 3321166)
        self.assertAttrEqual(item2, "vote_type", 2)

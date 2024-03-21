"""Tests for views."""

from unittest import mock

from django.urls import reverse
from django.template.response import TemplateResponse
from watcher.core.repositories import ReadRepository
from watcher.votes.enum import VoteType

from watcher.votes.models import Bill, Person, Vote, VoteResult
from watcher.votes.views import (
    BillListView,
    LegislatorListView,
    VoteListView,
    VoteResultListView,
)

from tests.common import BaseTestCase


class TestLegislatorListView(BaseTestCase):
    """Tests for legislator list view."""

    view_name = "votes:legislator-list"

    def repository(self, mock_repository: mock.MagicMock):
        """Patch repository object."""
        return mock.patch.object(
            LegislatorListView, "get_repository", return_value=mock_repository
        )

    def test_list_legislators(self):
        """Test list legislators."""
        mock_repository_class = mock.MagicMock(spec=ReadRepository[Person])
        mock_repository = mock_repository_class.return_value
        mock_repository.get_all.return_value = [
            Person(id=904789, name="Rep. Don Bacon (R-NE-2)"),
            Person(id=1603850, name="Rep. Jamaal Bowman (D-NY-16)"),
        ]

        with self.repository(mock_repository):
            response = self.client.get(reverse(self.view_name))

        mock_repository.get_all.assert_called_once()

        assert isinstance(response, TemplateResponse)
        context = response.context

        self.assertIn("object_list", context)
        object_list = context["object_list"]
        self.assertIsInstance(object_list, list)
        self.assertEqual(len(object_list), 2)

        item1 = object_list[0]
        self.assertAttrEqual(item1, "id", 904789)
        self.assertAttrEqual(item1, "name", "Rep. Don Bacon (R-NE-2)")

        item2 = object_list[1]
        self.assertAttrEqual(item2, "id", 1603850)
        self.assertAttrEqual(item2, "name", "Rep. Jamaal Bowman (D-NY-16)")


class TestBillListView(BaseTestCase):
    """Tests for bill list view."""

    view_name = "votes:bill-list"

    def repository(self, mock_repository: mock.MagicMock):
        """Patch repository object."""
        return mock.patch.object(
            BillListView, "get_repository", return_value=mock_repository
        )

    def test_list_bills(self):
        """Test list bills."""
        mock_repository_class = mock.MagicMock(spec=ReadRepository[Bill])
        mock_repository = mock_repository_class.return_value
        mock_repository.get_all.return_value = [
            Bill(
                id=2952375,
                title="H.R. 5376: Build Back Better Act",
                sponsor_id=412211,
            ),
            Bill(
                id=2900994,
                title="H.R. 3684: Infrastructure Investment and Jobs Act",
                sponsor_id=400100,
            ),
        ]

        with self.repository(mock_repository):
            response = self.client.get(reverse(self.view_name))

        mock_repository.get_all.assert_called_once()

        assert isinstance(response, TemplateResponse)
        context = response.context

        self.assertIn("object_list", context)
        object_list = context["object_list"]
        self.assertIsInstance(object_list, list)
        self.assertEqual(len(object_list), 2)

        item1 = object_list[0]
        self.assertAttrEqual(item1, "id", 2952375)
        self.assertAttrEqual(
            item1, "title", "H.R. 5376: Build Back Better Act"
        )
        self.assertAttrEqual(item1, "sponsor_id", 412211)

        item2 = object_list[1]
        self.assertAttrEqual(item2, "id", 2900994)
        self.assertAttrEqual(
            item2, "title", "H.R. 3684: Infrastructure Investment and Jobs Act"
        )
        self.assertAttrEqual(item2, "sponsor_id", 400100)


class TestVoteListView(BaseTestCase):
    """Tests for vote list view."""

    view_name = "votes:vote-list"

    def repository(self, mock_repository: mock.MagicMock):
        """Patch repository object."""
        return mock.patch.object(
            VoteListView, "get_repository", return_value=mock_repository
        )

    def test_list_votes(self):
        """Test list votes."""
        mock_repository_class = mock.MagicMock(spec=ReadRepository[Vote])
        mock_repository = mock_repository_class.return_value
        mock_repository.get_all.return_value = [
            Vote(id=3314452, bill_id=2900994),
            Vote(id=3321166, bill_id=2952375),
        ]

        with self.repository(mock_repository):
            response = self.client.get(reverse(self.view_name))

        mock_repository.get_all.assert_called_once()

        assert isinstance(response, TemplateResponse)
        context = response.context

        self.assertIn("object_list", context)
        object_list = context["object_list"]
        self.assertIsInstance(object_list, list)
        self.assertEqual(len(object_list), 2)

        item1 = object_list[0]
        self.assertAttrEqual(item1, "id", 3314452)
        self.assertAttrEqual(item1, "bill_id", 2900994)

        item2 = object_list[1]
        self.assertAttrEqual(item2, "id", 3321166)
        self.assertAttrEqual(item2, "bill_id", 2952375)


class TestVoteResultListView(BaseTestCase):
    """Tests for vote list view."""

    view_name = "votes:vote-result-list"

    def repository(self, mock_repository: mock.MagicMock):
        """Patch repository object."""
        return mock.patch.object(
            VoteResultListView, "get_repository", return_value=mock_repository
        )

    def test_list_votes(self):
        """Test list votes."""
        mock_repository_class = mock.MagicMock(spec=ReadRepository[VoteResult])
        mock_repository = mock_repository_class.return_value
        mock_repository.get_all.return_value = [
            VoteResult(
                id=92516553,
                legislator_id=1269790,
                vote_id=3321166,
                vote_type=VoteType(1),
            ),
            VoteResult(
                id=92516784,
                legislator_id=400440,
                vote_id=3321166,
                vote_type=VoteType(2),
            ),
        ]

        with self.repository(mock_repository):
            response = self.client.get(reverse(self.view_name))

        mock_repository.get_all.assert_called_once()

        assert isinstance(response, TemplateResponse)
        context = response.context

        self.assertIn("object_list", context)
        object_list = context["object_list"]
        self.assertIsInstance(object_list, list)
        self.assertEqual(len(object_list), 2)

        item1 = object_list[0]
        self.assertAttrEqual(item1, "id", 92516553)
        self.assertAttrEqual(item1, "legislator_id", 1269790)
        self.assertAttrEqual(item1, "vote_id", 3321166)
        self.assertAttrEqual(item1, "vote_type", VoteType(1))

        item2 = object_list[1]
        self.assertAttrEqual(item2, "id", 92516784)
        self.assertAttrEqual(item2, "legislator_id", 400440)
        self.assertAttrEqual(item2, "vote_id", 3321166)
        self.assertAttrEqual(item2, "vote_type", VoteType(2))

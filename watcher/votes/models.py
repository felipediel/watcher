"""Models."""

from dataclasses import dataclass

from .enum import VoteType


@dataclass
class Person:
    """Person."""

    id: int
    name: str


@dataclass
class Bill:
    """Bill."""

    id: int
    title: str
    sponsor_id: int


@dataclass
class Vote:
    """Vote."""

    id: int
    bill_id: int


@dataclass
class VoteResult:
    """Vote result."""

    id: int
    legislator_id: int
    vote_id: int
    vote_type: VoteType


@dataclass
class LegislatorVoteSummary:
    """Legislator vote summary."""

    legislator_id: int
    legislator_name: str
    supported_bills: int = 0
    opposed_bills: int = 0


@dataclass
class BillVoteSummary:
    """Bill vote summary."""

    bill_id: int
    bill_title: str
    sponsor_id: int | None
    sponsor_name: str
    supporters: int = 0
    opposers: int = 0

"""Schemas."""
from pydantic import BaseModel, ConfigDict, Field


class PersonQueryParams(BaseModel):
    """Person query params."""

    id: list[int] | None = Field(title="ID", default=None)
    name: list[str] | None = Field(title="Name", default=None)
    model_config = ConfigDict(extra='ignore')


class BillQueryParams(BaseModel):
    """Bill query params."""

    id: list[int] | None = Field(title="ID", default=None)
    title: list[str] | None = Field(title="Title", default=None)
    sponsor_id: list[int] | None = Field(title="Sponsor ID", default=None)
    model_config = ConfigDict(extra='ignore')


class VoteQueryParams(BaseModel):
    """Vote query params."""

    id: list[int] | None = Field(title="ID", default=None)
    bill_id: list[int] | None = Field(title="Bill ID", default=None)
    model_config = ConfigDict(extra='ignore')


class VoteResultQueryParams(BaseModel):
    """Vote result query params."""

    id: list[int] | None = Field(title="ID", default=None)
    legislator_id: list[int] | None = Field(title="Legislator ID", default=None)
    vote_id: list[int] | None = Field(title="Vote ID", default=None)
    vote_type: list[int] | None = Field(title="Vote type", default=None)
    model_config = ConfigDict(extra='ignore')


class LegislatorVoteSummaryQueryParams(BaseModel):
    """Legislator vote summary query params."""

    legislator_id: list[int] | None = Field(title="Legislator ID", default=None)
    legislator_name: list[str] | None = Field(title="Legislator name", default=None)
    supported_bills: list[int] | None = Field(title="Supported bills", default=None)
    opposed_bills: list[int] | None = Field(title="Opposed bills", default=None)
    model_config = ConfigDict(extra='ignore')


class BillVoteSummaryQueryParams(BaseModel):
    """Bill vote summary query params."""

    bill_id: list[int] | None = Field(title="Bill ID", default=None)
    bill_title: list[str] | None = Field(title="Bill title", default=None)
    sponsor_id: list[int] | None = Field(title="Sponsor ID", default=None)
    sponsor_name: list[str] | None = Field(title="Sponsor name", default=None)
    supporters: list[int] | None = Field(title="Supporters", default=None)
    opposers: list[int] | None = Field(title="Opposers", default=None)
    model_config = ConfigDict(extra='ignore')

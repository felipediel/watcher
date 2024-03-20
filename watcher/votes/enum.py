"""Enum."""

import enum


@enum.unique
class VoteType(enum.IntEnum):
    """Vote type."""

    YES = 1
    NO = 2

## Questions

1. If you were asked to model and query the data using ORM or raw SQL, how would you do to retrieve the legislators vote summary and bills vote summary?

### Models

```python
from django.db import models


class Person(models.Model):
    """Person."""

    name = models.CharField(max_length=80)


class Bill(models.Model):
    """Bill."""

    title = models.CharField(max_length=255)
    sponsor = models.ForeignKey(
        Person,
        on_delete=models.SET_NULL,
        related_name="sponsored_bills",
        null=True,
    )


class Vote(models.Model):
    """Vote."""

    bill = models.ForeignKey(
        Bill,
        on_delete=models.CASCADE,
        related_name="votes",
    )


class VoteResult(models.Model):
    """Vote result."""

    legislator = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        related_name="vote_results",
    )
    vote = models.ForeignKey(
        Vote,
        on_delete=models.CASCADE,
        related_name="vote_results",
    )
    vote_type = models.PositiveSmallIntegerField(
        choices=[(1, "Yes"), (2, "No")]
    )
```

### Legislators Vote Summary

#### Expected Result

```python
[{'id': 1, 'name': 'Rep. Don Bacon (R-NE-2)', 'supported_bills': 1, 'opposed_bills': 1}, {'id': 2, 'name': 'Rep. Jamaal Bowman (D-NY-16)', 'supported_bills': 1, 'opposed_bills': 1}, {'id': 3, 'name': 'Rep. Cori Bush (D-MO-1)', 'supported_bills': 1, 'opposed_bills': 1}, {'id': 4, 'name': 'Rep. Brian Fitzpatrick (R-PA-1)', 'supported_bills': 1, 'opposed_bills': 1}, {'id': 5, 'name': 'Rep. Andrew Garbarino (R-NY-2)', 'supported_bills': 1, 'opposed_bills': 1}, {'id': 6, 'name': 'Rep. Anthony Gonzalez (R-OH-16)', 'supported_bills': 1, 'opposed_bills': 1}, ...]
```

#### ORM Query

```python
from django.db.models import Q, Count


Person.objects.values('id', 'name').annotate(
    supported_bills=Count('vote_results__vote__bill', filter=Q(vote_results__vote_type=1)),
    opposed_bills=Count('vote_results__vote__bill', filter=Q(vote_results__vote_type=2))
)
```

#### Raw SQL Query:

```SQL
SELECT
    "votes_person"."id",
    "votes_person"."name",
    COUNT("votes_vote"."bill_id") FILTER (WHERE "votes_voteresult"."vote_type" = 1) AS "supported_bills",
    COUNT("votes_vote"."bill_id") FILTER (WHERE "votes_voteresult"."vote_type" = 2) AS "opposed_bills"
FROM
    "votes_person"
LEFT OUTER JOIN
    "votes_voteresult" ON ("votes_person"."id" = "votes_voteresult"."legislator_id")
LEFT OUTER JOIN
    "votes_vote" ON ("votes_voteresult"."vote_id" = "votes_vote"."id")
GROUP BY
    "votes_person"."id"
```

### Bill Vote Summary

#### Expected Result

```python
[{'id': 1, 'title': 'H.R. 5376: Build Back Better Act', 'supporters': 13, 'opposers': 6}, {'id': 2, 'title': 'H.R. 3684: Infrastructure Investment and Jobs Act', 'supporters': 6, 'opposers': 13}]
```
#### ORM Query

```python
from django.db.models import Q, Count


Bill.objects.values('id', 'title').annotate(
    supporters=Count('votes__vote_results__legislator', filter=Q(votes__vote_results__vote_type=1)),
    opposers=Count('votes__vote_results__legislator', filter=Q(votes__vote_results__vote_type=2))
)
```

#### Raw SQL Query

```SQL
SELECT
    "votes_bill"."id",
    "votes_bill"."title",
    COUNT("votes_voteresult"."legislator_id") FILTER (WHERE "votes_voteresult"."vote_type" = 1) AS "supporters",
    COUNT("votes_voteresult"."legislator_id") FILTER (WHERE "votes_voteresult"."vote_type" = 2) AS "opposers"
FROM
    "votes_bill"
LEFT OUTER JOIN
    "votes_vote" ON ("votes_bill"."id" = "votes_vote"."bill_id")
LEFT OUTER JOIN
    "votes_voteresult" ON ("votes_vote"."id" = "votes_voteresult"."vote_id")
GROUP BY
    "votes_bill"."id"
```

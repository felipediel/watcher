"""App config."""

from django.apps import AppConfig


class VotesConfig(AppConfig):
    """Votes app config."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "watcher.votes"

"""Forms."""

from django import forms


class SearchForm(forms.Form):
    """Search form."""

    search = forms.CharField(label="Search", required=False)

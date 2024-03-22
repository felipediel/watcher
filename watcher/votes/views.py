"""Views."""

import io
import os
import zipfile
from typing import Any

from django.conf import settings
from django.core.files.storage import default_storage
from django.http import FileResponse
from django.views.generic import ListView, View

from watcher.core.forms import SearchForm
from watcher.core.specifications import (
    FieldSpecificationBackend,
    SearchSpecificationBackend,
)
from watcher.core.views import RepositoryListView, SpecificationMixin

from .schemas import (
    BillQueryParams,
    BillVoteSummaryQueryParams,
    LegislatorVoteSummaryQueryParams,
    PersonQueryParams,
    VoteQueryParams,
    VoteResultQueryParams,
)
from .services import BillVoteSummaryService, LegislatorVoteSummaryService
from .repositories import (
    BillCsvRepository,
    LegislatorCsvRepository,
    VoteCsvRepository,
    VoteResultCsvRepository,
)


class LegislatorListView(RepositoryListView):
    """Legislator list view."""

    template_name = "legislator_list.html"
    form_class = SearchForm
    repository_class = LegislatorCsvRepository
    specification_backends = [
        FieldSpecificationBackend,
        SearchSpecificationBackend,
    ]
    search_fields = {
        "id": int,
        "name": str,
        "name__contains": str,
    }
    paginate_by = 15

    def get_repository_config(self) -> dict[str, Any]:
        """Get repository config."""
        return {"file_path": settings.MEDIA_FILES["legislators"]}

    def get_query_params(self) -> dict[str, Any]:
        """Get query parameters."""
        return PersonQueryParams(**self.request.GET).model_dump()


class BillListView(RepositoryListView):
    """Bill list view."""

    template_name = "bill_list.html"
    form_class = SearchForm
    repository_class = BillCsvRepository
    specification_backends = [
        FieldSpecificationBackend,
        SearchSpecificationBackend,
    ]
    search_fields = {
        "id": int,
        "title": str,
        "title__contains": str,
        "sponsor_id": int,
    }
    paginate_by = 15

    def get_repository_config(self) -> dict[str, Any]:
        """Get repository config."""
        return {"file_path": settings.MEDIA_FILES["bills"]}

    def get_query_params(self) -> dict[str, Any]:
        """Get query parameters."""
        return BillQueryParams(**self.request.GET).model_dump()


class VoteListView(RepositoryListView):
    """Vote list view."""

    template_name = "vote_list.html"
    form_class = SearchForm
    repository_class = VoteCsvRepository
    specification_backends = [
        FieldSpecificationBackend,
        SearchSpecificationBackend,
    ]
    search_fields = {"id": int, "bill_id": int}
    paginate_by = 15

    def get_repository_config(self) -> dict[str, Any]:
        """Get repository config."""
        return {"file_path": settings.MEDIA_FILES["votes"]}

    def get_query_params(self) -> dict[str, Any]:
        """Get query parameters."""
        return VoteQueryParams(**self.request.GET).model_dump()


class VoteResultListView(RepositoryListView):
    """Vote result list view."""

    template_name = "vote_result_list.html"
    form_class = SearchForm
    repository_class = VoteResultCsvRepository
    specification_backends = [
        FieldSpecificationBackend,
        SearchSpecificationBackend,
    ]
    search_fields = {
        "id": int,
        "legislator_id": int,
        "vote_id": int,
        "vote_type": int,
    }
    paginate_by = 15

    def get_repository_config(self) -> dict[str, Any]:
        """Get repository config."""
        return {"file_path": settings.MEDIA_FILES["vote_results"]}

    def get_query_params(self) -> dict[str, Any]:
        """Get query parameters."""
        return VoteResultQueryParams(**self.request.GET).model_dump()


class LegislatorVoteSummaryListView(SpecificationMixin, ListView):
    """Legislator vote summary list view."""

    template_name = "legislator_vote_summary_list.html"
    form_class = SearchForm
    specification_backends = [
        FieldSpecificationBackend,
        SearchSpecificationBackend,
    ]
    search_fields = {
        "legislator_id": int,
        "legislator_name": str,
        "legislator_name__contains": str,
        "supported_bills": int,
        "opposed_bills": int,
    }
    paginate_by = 15

    def get_queryset(self):
        """Get queryset."""
        service = self.get_service()
        spec = self.get_specification()
        vote_summary = service.summarize_votes(spec)
        return vote_summary

    def get_service(self) -> LegislatorVoteSummaryService:
        """Get service."""
        vote_result_repository = VoteResultCsvRepository.using(
            file_path=settings.MEDIA_FILES["vote_results"]
        )
        vote_repository = VoteCsvRepository.using(
            file_path=settings.MEDIA_FILES["votes"]
        )
        legislator_repository = LegislatorCsvRepository.using(
            file_path=settings.MEDIA_FILES["legislators"]
        )
        service = LegislatorVoteSummaryService(
            vote_repository=vote_repository,
            vote_result_repository=vote_result_repository,
            legislator_repository=legislator_repository,
        )
        return service

    def get_query_params(self) -> dict[str, Any]:
        """Get query parameters."""
        return LegislatorVoteSummaryQueryParams(
            **self.request.GET
        ).model_dump()


class BillVoteSummaryListView(SpecificationMixin, ListView):
    """Bill vote summary list view."""

    template_name = "bill_vote_summary_list.html"
    form_class = SearchForm
    specification_backends = [
        FieldSpecificationBackend,
        SearchSpecificationBackend,
    ]
    search_fields = {
        "bill_id": int,
        "bill_title__contains": str,
        "sponsor_id": int,
        "sponsor_name__contains": str,
        "supporters": int,
        "opposers": int,
    }
    paginate_by = 15

    def get_queryset(self):
        """Get queryset."""
        service = self.get_service()
        spec = self.get_specification()
        bill_vote_summary = service.summarize_votes(spec)
        return bill_vote_summary

    def get_service(self) -> BillVoteSummaryService:
        """Get service."""
        vote_repository = VoteCsvRepository.using(
            file_path=settings.MEDIA_FILES["votes"]
        )
        vote_result_repository = VoteResultCsvRepository.using(
            file_path=settings.MEDIA_FILES["vote_results"]
        )
        bill_repository = BillCsvRepository.using(
            file_path=settings.MEDIA_FILES["bills"]
        )
        legislator_repository = LegislatorCsvRepository.using(
            file_path=settings.MEDIA_FILES["legislators"]
        )
        service = BillVoteSummaryService(
            vote_repository=vote_repository,
            vote_result_repository=vote_result_repository,
            bill_repository=bill_repository,
            legislator_repository=legislator_repository,
        )
        return service

    def get_query_params(self) -> dict[str, Any]:
        """Get query parameters."""
        return BillVoteSummaryQueryParams(**self.request.GET).model_dump()


class DownloadAllView(View):
    """Download all files."""

    def get(self, request, *args, **kwargs):
        files_to_zip = [
            settings.MEDIA_FILES["bills"],
            settings.MEDIA_FILES["votes"],
            settings.MEDIA_FILES["vote_results"],
            settings.MEDIA_FILES["legislators"],
        ]
        zip_filename = "datasets.zip"
        stream = io.BytesIO()

        with zipfile.ZipFile(stream, "w", zipfile.ZIP_DEFLATED, False) as zf:
            for filename in files_to_zip:
                with default_storage.open(filename, "r") as file:
                    zf.writestr(os.path.basename(filename), file.read())

        stream.seek(0)
        response = FileResponse(stream, content_type='application/zip')
        response['Content-Disposition'] = f'attachment; filename="{zip_filename}"'
        return response

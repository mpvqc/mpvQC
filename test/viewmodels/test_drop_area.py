# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from unittest.mock import MagicMock

import inject
import pytest
from PySide6.QtCore import QUrl

from mpvqc.services import ImporterService, MimetypeProviderService
from mpvqc.viewmodels import MpvqcDropAreaViewModel


@pytest.fixture
def importer_service_mock() -> MagicMock:
    return MagicMock(spec_set=ImporterService)


@pytest.fixture(autouse=True)
def configure_inject(common_bindings_with, importer_service_mock):
    def custom_bindings(binder: inject.Binder):
        binder.bind(ImporterService, importer_service_mock)
        binder.bind_to_constructor(MimetypeProviderService, MimetypeProviderService)

    common_bindings_with(custom_bindings)


@pytest.fixture
def view_model() -> MpvqcDropAreaViewModel:
    # noinspection PyCallingNonCallable
    return MpvqcDropAreaViewModel()


def test_open_routes_dropped_files_by_extension(view_model, importer_service_mock):
    urls = [
        QUrl.fromLocalFile("/work/report.txt"),
        QUrl.fromLocalFile("/work/report.json"),
        QUrl.fromLocalFile("/work/subtitle.ass"),
        QUrl.fromLocalFile("/work/movie.mkv"),
    ]

    view_model.open(urls)

    documents, videos, subtitles = importer_service_mock.open.call_args.args
    assert [path.name for path in documents] == ["report.txt", "report.json"]
    assert [path.name for path in videos] == ["movie.mkv"]
    assert [path.name for path in subtitles] == ["subtitle.ass"]

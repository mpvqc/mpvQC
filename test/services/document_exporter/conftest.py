# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from pathlib import Path
from unittest.mock import MagicMock, patch

import inject
import pytest

from mpvqc.services import PlayerService, ResourceReaderService, ResourceService, SettingsService

MODULE = "mpvqc.services.document_exporter"


@pytest.fixture
def qt_app():
    with patch(f"{MODULE}.QCoreApplication.instance", return_value=MagicMock()) as mock:
        yield mock.return_value


@pytest.fixture
def make_mock(qt_app, settings_service):
    def _make_mock(
        video: Path | str | None = None,
        nickname: str | None = None,
        comments: list | None = None,
        subtitles: list | None = None,
        write_header_date: bool = False,
        write_header_generator: bool = False,
        write_header_nickname: bool = False,
        write_header_video_path: bool = False,
        write_header_subtitles: bool = False,
    ):
        qt_app.find_object.return_value.comments.return_value = comments or []

        settings_service.nickname = nickname
        settings_service.write_header_date = write_header_date
        settings_service.write_header_generator = write_header_generator
        settings_service.write_header_nickname = write_header_nickname
        settings_service.write_header_video_path = write_header_video_path
        settings_service.write_header_subtitles = write_header_subtitles
        settings_service.language = "en-US"

        player_mock = MagicMock(spec_set=PlayerService)
        player_mock.path = str(video) if video else None
        player_mock.has_video = bool(video)
        player_mock.external_subtitles = subtitles or []

        def config(binder: inject.Binder):
            binder.bind(PlayerService, player_mock)
            binder.bind(SettingsService, settings_service)
            binder.bind(ResourceReaderService, ResourceReaderService())
            binder.bind(ResourceService, ResourceService())

        inject.configure(config, clear=True)

    return _make_mock

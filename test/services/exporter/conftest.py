# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from pathlib import Path
from unittest.mock import MagicMock

import inject
import pytest

from mpvqc.services import (
    ApplicationPathsService,
    BuildInfoService,
    CommentsService,
    PlayerService,
    SettingsService,
    StateService,
)
from mpvqc.services.exporter.context import RenderContext


@pytest.fixture
def comments_service_mock() -> MagicMock:
    return MagicMock(spec_set=CommentsService)


@pytest.fixture
def application_paths_service_mock() -> MagicMock:
    return MagicMock(spec_set=ApplicationPathsService)


@pytest.fixture
def build_info_service_mock() -> MagicMock:
    return MagicMock(spec_set=BuildInfoService)


@pytest.fixture
def player_service_mock():
    return MagicMock(spec_set=PlayerService)


@pytest.fixture
def state_service_mock() -> MagicMock:
    return MagicMock(spec_set=StateService)


@pytest.fixture(autouse=True)
def configure_injections(
    common_bindings_with,
    application_paths_service_mock,
    build_info_service_mock,
    comments_service_mock,
    player_service_mock,
    settings_service,
    state_service_mock,
):
    def custom_bindings(binder: inject.Binder):
        binder.bind(ApplicationPathsService, application_paths_service_mock)
        binder.bind(BuildInfoService, build_info_service_mock)
        binder.bind(CommentsService, comments_service_mock)
        binder.bind(PlayerService, player_service_mock)
        binder.bind(SettingsService, settings_service)
        binder.bind(StateService, state_service_mock)

    common_bindings_with(custom_bindings)


@pytest.fixture
def make_context():
    def _make_context(
        video: Path | str | None = None,
        nickname: str | None = None,
        generator: str = "mpvQC 0.0.0",
        comments: list | None = None,
        subtitles: list | None = None,
        write_header_date: bool = False,
        write_header_generator: bool = False,
        write_header_nickname: bool = False,
        write_header_video_path: bool = False,
        write_header_subtitles: bool = False,
    ) -> RenderContext:
        return RenderContext(
            write_header_date=write_header_date,
            write_header_generator=write_header_generator,
            write_header_nickname=write_header_nickname,
            write_header_video_path=write_header_video_path,
            write_header_subtitles=write_header_subtitles,
            nickname=nickname,
            video_path=str(video) if video else None,
            external_subtitles=tuple(str(s) for s in subtitles or ()),
            generator=generator,
            comments=tuple(comments or ()),
        )

    return _make_context

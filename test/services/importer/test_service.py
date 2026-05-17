# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from unittest.mock import MagicMock

import inject
import pytest
from PySide6.QtTest import QSignalSpy

from mpvqc.services.comments import CommentsService
from mpvqc.services.document_importer import DocumentImporterService
from mpvqc.services.importer import FinishedPlan, ImporterService
from mpvqc.services.importer.concerns import session, subtitles, video
from mpvqc.services.player import PlayerService
from mpvqc.services.settings import SettingsService
from mpvqc.services.state import StateService
from mpvqc.services.subtitle_importer import SubtitleImporterService


@pytest.fixture(autouse=True)
def stub_threadpool(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("mpvqc.services.importer.service.QThreadPool", MagicMock())


@pytest.fixture(autouse=True)
def configure_inject() -> None:
    comments = MagicMock(spec_set=CommentsService)
    comments.count = 0

    def config(binder: inject.Binder) -> None:
        binder.bind(PlayerService, MagicMock(spec_set=PlayerService))
        binder.bind(SettingsService, MagicMock(spec_set=SettingsService))
        binder.bind(StateService, MagicMock(spec_set=StateService))
        binder.bind(CommentsService, comments)
        binder.bind(DocumentImporterService, MagicMock(spec_set=DocumentImporterService))
        binder.bind(SubtitleImporterService, MagicMock(spec_set=SubtitleImporterService))

    inject.configure(config, allow_override=True, bind_in_runtime=False, clear=True)


@pytest.fixture
def service() -> ImporterService:
    return ImporterService()


NOOP_PLAN = FinishedPlan(
    comments=(),
    session=session.Merge(),
    video=video.Skip(),
    subtitles=subtitles.Skip(),
)


def test_second_open_while_busy_is_ignored(service: ImporterService) -> None:
    service.open([], [], [])
    spy = QSignalSpy(service.busy_changed)
    service.open([], [], [])
    assert service.busy is True
    assert spy.count() == 0


def test_cancel_pending_unblocks_next_open(service: ImporterService) -> None:
    service.open([], [], [])
    service.cancel_pending()
    spy = QSignalSpy(service.busy_changed)
    service.open([], [], [])
    assert service.busy is True
    assert spy.count() == 1
    assert spy.at(0) == [True]


def test_execute_unblocks_next_open(service: ImporterService) -> None:
    service.open([], [], [])
    service.execute(NOOP_PLAN)
    spy = QSignalSpy(service.busy_changed)
    service.open([], [], [])
    assert service.busy is True
    assert spy.count() == 1
    assert spy.at(0) == [True]

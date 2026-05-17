# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from pathlib import Path
from typing import NamedTuple, cast
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


V = Path("/movies/v.mp4")
S1 = Path("/work/a.srt")
S2 = Path("/work/b.srt")


class DispatchCase(NamedTuple):
    name: str
    plan: FinishedPlan
    expected: dict[str, Path | tuple[Path, ...] | None] | None


DISPATCH_CASES = [
    DispatchCase(
        name="video and subtitles both load",
        plan=FinishedPlan(
            comments=(),
            session=session.Merge(),
            video=video.Load(path=V),
            subtitles=subtitles.Load(paths=(S1, S2)),
        ),
        expected={"video": V, "subtitles": (S1, S2)},
    ),
    DispatchCase(
        name="video loads, subtitles skipped",
        plan=FinishedPlan(
            comments=(),
            session=session.Merge(),
            video=video.Load(path=V),
            subtitles=subtitles.Skip(),
        ),
        expected={"video": V, "subtitles": ()},
    ),
    DispatchCase(
        name="subtitles load without a video",
        plan=FinishedPlan(
            comments=(),
            session=session.Merge(),
            video=video.Skip(),
            subtitles=subtitles.Load(paths=(S1,)),
        ),
        expected={"video": None, "subtitles": (S1,)},
    ),
    DispatchCase(
        name="nothing to load leaves the player untouched",
        plan=NOOP_PLAN,
        expected=None,
    ),
]


@pytest.mark.parametrize("case", DISPATCH_CASES, ids=lambda c: c.name)
def test_execute_dispatches_to_open_media(service: ImporterService, case: DispatchCase) -> None:
    player = cast("MagicMock", inject.instance(PlayerService))

    service.execute(case.plan)

    if case.expected is None:
        player.open_media.assert_not_called()
    else:
        player.open_media.assert_called_once_with(**case.expected)

# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from typing import TYPE_CHECKING, NamedTuple
from unittest.mock import MagicMock

import inject
import pytest

from mpvqc.datamodels import Comment
from mpvqc.importing.domain import (
    FinishedPlan,
    LoadFoundVideo,
    PendingImport,
    SessionMerge,
    SessionReplace,
    SubtitlesLoad,
    SubtitlesSkip,
    UnfinishedPlan,
    VideoLoad,
    VideoSkip,
)
from mpvqc.importing.services import ImporterService, ImportSettingsService
from mpvqc.services.comments import CommentsService
from mpvqc.services.player import PlayerService
from mpvqc.services.resetter import ResetService
from mpvqc.services.state import StateService
from test.importing.plans import SUB_A, SUB_B, UNRESOLVED_VIDEO, VIDEO_A, plan_with

if TYPE_CHECKING:
    from collections.abc import Callable
    from pathlib import Path

    from test.conftest import ManualJobExecutor


@pytest.fixture
def player_service_mock() -> MagicMock:
    mock = MagicMock(spec_set=PlayerService)
    mock.path = ""
    return mock


@pytest.fixture
def import_settings_service_mock() -> MagicMock:
    mock = MagicMock(spec_set=ImportSettingsService)
    mock.import_found_video = LoadFoundVideo.ASK_EVERY_TIME
    return mock


@pytest.fixture
def state_service_mock() -> MagicMock:
    return MagicMock(spec_set=StateService)


@pytest.fixture
def comments_service_mock() -> MagicMock:
    mock = MagicMock(spec_set=CommentsService)
    mock.count = 0
    return mock


@pytest.fixture
def reset_service_mock() -> MagicMock:
    return MagicMock(spec_set=ResetService)


@pytest.fixture(autouse=True)
def configure_inject(
    player_service_mock: MagicMock,
    import_settings_service_mock: MagicMock,
    state_service_mock: MagicMock,
    comments_service_mock: MagicMock,
    reset_service_mock: MagicMock,
) -> None:
    def config(binder: inject.Binder) -> None:
        binder.bind(PlayerService, player_service_mock)
        binder.bind(ImportSettingsService, import_settings_service_mock)
        binder.bind(StateService, state_service_mock)
        binder.bind(CommentsService, comments_service_mock)
        binder.bind(ResetService, reset_service_mock)

    inject.configure(config, allow_override=True, bind_in_runtime=False, clear=True)


@pytest.fixture
def make_importer(manual_executor: ManualJobExecutor) -> Callable[[FinishedPlan | UnfinishedPlan], ImporterService]:
    def _make(planned: FinishedPlan | UnfinishedPlan) -> ImporterService:
        return ImporterService(manual_executor, plan=lambda *_args, **_kwargs: planned)

    return _make


NOOP_PLAN = FinishedPlan(
    comments=(),
    session=SessionMerge(),
    video=VideoSkip(),
    subtitles=SubtitlesSkip(),
)

NEEDS_A_VIDEO_CHOICE = plan_with(video=UNRESOLVED_VIDEO)


class DispatchCase(NamedTuple):
    name: str
    plan: FinishedPlan
    expected: dict[str, Path | tuple[Path, ...] | None] | None


DISPATCH_CASES = [
    DispatchCase(
        name="video and subtitles both load",
        plan=FinishedPlan(
            comments=(),
            session=SessionMerge(),
            video=VideoLoad(path=VIDEO_A),
            subtitles=SubtitlesLoad(paths=(SUB_A, SUB_B)),
        ),
        expected={"video": VIDEO_A, "subtitles": (SUB_A, SUB_B)},
    ),
    DispatchCase(
        name="video loads, subtitles skipped",
        plan=FinishedPlan(
            comments=(),
            session=SessionMerge(),
            video=VideoLoad(path=VIDEO_A),
            subtitles=SubtitlesSkip(),
        ),
        expected={"video": VIDEO_A, "subtitles": ()},
    ),
    DispatchCase(
        name="subtitles load without a video",
        plan=FinishedPlan(
            comments=(),
            session=SessionMerge(),
            video=VideoSkip(),
            subtitles=SubtitlesLoad(paths=(SUB_A,)),
        ),
        expected={"video": None, "subtitles": (SUB_A,)},
    ),
    DispatchCase(
        name="nothing to load leaves the player untouched",
        plan=NOOP_PLAN,
        expected=None,
    ),
]


@pytest.mark.parametrize("case", DISPATCH_CASES, ids=lambda c: c.name)
def test_open_dispatches_a_finished_plan_to_open_media(
    qt_app,
    manual_executor: ManualJobExecutor,
    make_importer,
    player_service_mock: MagicMock,
    case: DispatchCase,
) -> None:
    make_importer(case.plan).open([], [], [])
    manual_executor.drain()

    if case.expected is None:
        player_service_mock.open_media.assert_not_called()
    else:
        player_service_mock.open_media.assert_called_once_with(**case.expected)


class RecordImportCase(NamedTuple):
    name: str
    plan: FinishedPlan
    player_already_has_video: bool
    expected_record: bool


RECORD_IMPORT_CASES = [
    RecordImportCase(
        name="new video, no comments: records",
        plan=FinishedPlan(
            comments=(),
            session=SessionMerge(),
            video=VideoLoad(path=VIDEO_A),
            subtitles=SubtitlesSkip(),
        ),
        player_already_has_video=False,
        expected_record=True,
    ),
    RecordImportCase(
        name="re-import of current video, no comments: skips (preserves document)",
        plan=FinishedPlan(
            comments=(),
            session=SessionMerge(),
            video=VideoLoad(path=VIDEO_A),
            subtitles=SubtitlesSkip(),
        ),
        player_already_has_video=True,
        expected_record=False,
    ),
    RecordImportCase(
        name="re-import of current video with comments: records",
        plan=FinishedPlan(
            comments=(MagicMock(),),
            session=SessionMerge(),
            video=VideoLoad(path=VIDEO_A),
            subtitles=SubtitlesSkip(),
        ),
        player_already_has_video=True,
        expected_record=True,
    ),
    RecordImportCase(
        name="no video, has comments: records",
        plan=FinishedPlan(
            comments=(MagicMock(),),
            session=SessionMerge(),
            video=VideoSkip(),
            subtitles=SubtitlesSkip(),
        ),
        player_already_has_video=False,
        expected_record=True,
    ),
    RecordImportCase(
        name="no video, no comments: skips",
        plan=NOOP_PLAN,
        player_already_has_video=False,
        expected_record=False,
    ),
]


@pytest.mark.parametrize("case", RECORD_IMPORT_CASES, ids=lambda c: c.name)
def test_open_gates_state_record_import(
    qt_app,
    manual_executor: ManualJobExecutor,
    make_importer,
    player_service_mock: MagicMock,
    state_service_mock: MagicMock,
    case: RecordImportCase,
) -> None:
    player_service_mock.is_any_video_loaded.return_value = case.player_already_has_video

    make_importer(case.plan).open([], [], [])
    manual_executor.drain()

    if case.expected_record:
        state_service_mock.record_import.assert_called_once()
    else:
        state_service_mock.record_import.assert_not_called()


COMMENTS = (Comment(time=0, comment_type="Translation", comment="Lorem ipsum"),)


def test_open_resets_the_application_for_a_replacing_session(
    qt_app,
    manual_executor: ManualJobExecutor,
    make_importer,
    reset_service_mock: MagicMock,
) -> None:
    plan = FinishedPlan(comments=(), session=SessionReplace(), video=VideoSkip(), subtitles=SubtitlesSkip())

    make_importer(plan).open([], [], [])
    manual_executor.drain()

    reset_service_mock.reset.assert_called_once()


def test_open_does_not_reset_for_a_merging_session(
    qt_app,
    manual_executor: ManualJobExecutor,
    make_importer,
    reset_service_mock: MagicMock,
) -> None:
    make_importer(NOOP_PLAN).open([], [], [])
    manual_executor.drain()

    reset_service_mock.reset.assert_not_called()


def test_open_imports_the_comments_it_planned(
    qt_app,
    manual_executor: ManualJobExecutor,
    make_importer,
    comments_service_mock: MagicMock,
) -> None:
    plan = FinishedPlan(comments=COMMENTS, session=SessionMerge(), video=VideoSkip(), subtitles=SubtitlesSkip())

    make_importer(plan).open([], [], [])
    manual_executor.drain()

    comments_service_mock.import_comments.assert_called_once_with(COMMENTS)


def test_open_without_comments_imports_nothing(
    qt_app,
    manual_executor: ManualJobExecutor,
    make_importer,
    comments_service_mock: MagicMock,
) -> None:
    make_importer(NOOP_PLAN).open([], [], [])
    manual_executor.drain()

    comments_service_mock.import_comments.assert_not_called()


def test_open_announces_a_pending_import_for_a_plan_needing_decisions(
    qt_app,
    manual_executor: ManualJobExecutor,
    make_importer,
    make_spy,
    player_service_mock: MagicMock,
) -> None:
    service = make_importer(NEEDS_A_VIDEO_CHOICE)
    spy = make_spy(service.pending_import_ready)

    service.open([], [], [])
    manual_executor.drain()

    assert spy.count() == 1
    assert spy.at(invocation=0, argument=0).plan == NEEDS_A_VIDEO_CHOICE
    player_service_mock.open_media.assert_not_called()


class AnnouncedImport(NamedTuple):
    service: ImporterService
    pending: PendingImport


@pytest.fixture
def pending_importer(
    qt_app,
    manual_executor: ManualJobExecutor,
    make_importer: Callable[[FinishedPlan | UnfinishedPlan], ImporterService],
    make_spy,
) -> AnnouncedImport:
    service = make_importer(NEEDS_A_VIDEO_CHOICE)
    spy = make_spy(service.pending_import_ready)
    service.open([], [], [])
    manual_executor.drain()
    return AnnouncedImport(service, spy.at(invocation=0, argument=0))


def test_finishing_the_announced_import_executes_the_resolved_plan(
    pending_importer: AnnouncedImport,
    player_service_mock: MagicMock,
) -> None:
    pending_importer.pending.finish(video=VideoLoad(path=VIDEO_A))

    player_service_mock.open_media.assert_called_once_with(video=VIDEO_A, subtitles=())


def test_dismiss_after_finish_changes_nothing(
    pending_importer: AnnouncedImport,
    manual_executor: ManualJobExecutor,
    make_spy,
    player_service_mock: MagicMock,
) -> None:
    # One close both finishes and dismisses, so the trailing dismissal must neither undo the import nor latch.
    pending_importer.pending.finish(video=VideoLoad(path=VIDEO_A))
    pending_importer.pending.dismiss()
    spy = make_spy(pending_importer.service.pending_import_ready)

    pending_importer.service.open([], [], [])
    manual_executor.drain()

    player_service_mock.open_media.assert_called_once_with(video=VIDEO_A, subtitles=())
    assert spy.count() == 1


def test_dismiss_never_reaches_the_player(
    pending_importer: AnnouncedImport,
    player_service_mock: MagicMock,
) -> None:
    pending_importer.pending.dismiss()

    player_service_mock.open_media.assert_not_called()


def test_a_second_open_while_a_decision_is_pending_is_dropped(
    pending_importer: AnnouncedImport,
    manual_executor: ManualJobExecutor,
    make_spy,
    caplog: pytest.LogCaptureFixture,
) -> None:
    spy = make_spy(pending_importer.service.pending_import_ready)

    pending_importer.service.open([], [], [])
    manual_executor.drain()

    assert spy.count() == 0
    assert "Skipping import while another is in progress" in caplog.text


def test_an_open_after_a_finish_proceeds(
    pending_importer: AnnouncedImport,
    manual_executor: ManualJobExecutor,
    make_spy,
) -> None:
    pending_importer.pending.finish(video=VideoSkip())
    spy = make_spy(pending_importer.service.pending_import_ready)

    pending_importer.service.open([], [], [])
    manual_executor.drain()

    assert spy.count() == 1


def test_an_open_after_a_dismissal_proceeds(
    pending_importer: AnnouncedImport,
    manual_executor: ManualJobExecutor,
    make_spy,
) -> None:
    pending_importer.pending.dismiss()
    spy = make_spy(pending_importer.service.pending_import_ready)

    pending_importer.service.open([], [], [])
    manual_executor.drain()

    assert spy.count() == 1


def test_a_late_dismissal_leaves_a_running_scan_alone(
    pending_importer: AnnouncedImport,
    manual_executor: ManualJobExecutor,
    make_spy,
) -> None:
    pending_importer.pending.dismiss()
    spy = make_spy(pending_importer.service.pending_import_ready)
    # The next scan is queued but undrained, so it is still in flight when the duplicate dismissal arrives.
    pending_importer.service.open([], [], [])

    pending_importer.pending.dismiss()
    pending_importer.service.open([], [], [])
    manual_executor.drain()

    assert spy.count() == 1


def test_open_recovers_when_the_scan_raises(
    qt_app,
    manual_executor: ManualJobExecutor,
    make_spy,
    caplog: pytest.LogCaptureFixture,
) -> None:
    scans = 0

    def explode_once(*_args: object, **_kwargs: object) -> FinishedPlan | UnfinishedPlan:
        nonlocal scans
        scans += 1
        if scans == 1:
            msg = "scan exploded"
            raise RuntimeError(msg)
        return NEEDS_A_VIDEO_CHOICE

    service = ImporterService(manual_executor, plan=explode_once)
    spy = make_spy(service.pending_import_ready)

    service.open([], [], [])
    manual_executor.drain()

    assert "Import scan failed" in caplog.text

    service.open([], [], [])
    manual_executor.drain()

    assert spy.count() == 1

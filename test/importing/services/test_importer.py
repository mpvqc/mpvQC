# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from typing import TYPE_CHECKING, NamedTuple
from unittest.mock import MagicMock

import inject
import pytest

from mpvqc.importing.domain import (
    LoadFoundVideo,
    NotAsked,
    PendingImport,
    ScanResult,
    SessionReplace,
    SubtitlesLoad,
    SubtitlesSkip,
    VideoLoad,
    VideoSkip,
)
from mpvqc.importing.services import ImportService, ImportSettingsService
from mpvqc.services import CommentsService, PlayerService, ResetService, StateService
from mpvqc.shared import Comment
from test.importing.plans import (
    SUB_A,
    SUB_A_FROM_DOCUMENT,
    SUB_B,
    SUB_B_FROM_DOCUMENT,
    UNRESOLVED_VIDEO,
    VIDEO_A,
    VIDEO_A_FROM_DOCUMENT,
    plan_with,
)

if TYPE_CHECKING:
    from collections.abc import Callable
    from pathlib import Path

    from mpvqc.importing.domain import SubtitleSource, SubtitlesResolved, VideoResolved, VideoSource
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
def make_importer(manual_executor: ManualJobExecutor) -> Callable[[ScanResult], ImportService]:
    def _make(scanned: ScanResult) -> ImportService:
        return ImportService(manual_executor, scan=lambda *_args: scanned)

    return _make


COMMENTS = (Comment(time=0, comment_type="Translation", comment="Lorem ipsum"),)


def scan_with(
    *,
    videos: tuple[VideoSource, ...] = (),
    subtitles: tuple[SubtitleSource, ...] = (),
    comments: tuple[Comment, ...] = (),
) -> ScanResult:
    return ScanResult(videos=videos, subtitles=subtitles, comments=comments, rejected_documents=())


EMPTY_SCAN = scan_with()

# Under the fixture's ASK_EVERY_TIME setting every found-media concern stays unresolved,
# so these scans announce a pending import.
VIDEO_CHOICE_SCAN = scan_with(videos=(VIDEO_A_FROM_DOCUMENT,))
MEDIA_CHOICE_SCAN = scan_with(
    videos=(VIDEO_A_FROM_DOCUMENT,),
    subtitles=(SUB_A_FROM_DOCUMENT, SUB_B_FROM_DOCUMENT),
)


class DispatchCase(NamedTuple):
    name: str
    video: VideoResolved
    subtitles: SubtitlesResolved
    expected: dict[str, Path | tuple[Path, ...] | None] | None


DISPATCH_CASES = [
    DispatchCase(
        name="video and subtitles both load",
        video=VideoLoad(path=VIDEO_A),
        subtitles=SubtitlesLoad(paths=(SUB_A, SUB_B)),
        expected={"video": VIDEO_A, "subtitles": (SUB_A, SUB_B)},
    ),
    DispatchCase(
        name="video loads, subtitles skipped",
        video=VideoLoad(path=VIDEO_A),
        subtitles=SubtitlesSkip(),
        expected={"video": VIDEO_A, "subtitles": ()},
    ),
    DispatchCase(
        name="subtitles load without a video",
        video=VideoSkip(),
        subtitles=SubtitlesLoad(paths=(SUB_A,)),
        expected={"video": None, "subtitles": (SUB_A,)},
    ),
    DispatchCase(
        name="nothing to load leaves the player untouched",
        video=VideoSkip(),
        subtitles=SubtitlesSkip(),
        expected=None,
    ),
]


@pytest.mark.parametrize("case", DISPATCH_CASES, ids=lambda c: c.name)
def test_finishing_the_import_dispatches_the_resolved_media_to_open_media(
    qt_app,
    manual_executor: ManualJobExecutor,
    make_importer,
    make_spy,
    player_service_mock: MagicMock,
    case: DispatchCase,
) -> None:
    service = make_importer(MEDIA_CHOICE_SCAN)
    spy = make_spy(service.pending_import_ready)

    service.open((), (), ())
    manual_executor.drain()

    assert spy.count() == 1
    spy.at(invocation=0, argument=0).finish(session=NotAsked(), video=case.video, subtitles=case.subtitles)

    if case.expected is None:
        player_service_mock.open_media.assert_not_called()
    else:
        player_service_mock.open_media.assert_called_once_with(**case.expected)


class RecordImportCase(NamedTuple):
    name: str
    scanned: ScanResult
    resolve_video: VideoResolved | None
    player_already_has_video: bool
    expected_record: bool


RECORD_IMPORT_CASES = [
    RecordImportCase(
        name="new video, no comments: records",
        scanned=VIDEO_CHOICE_SCAN,
        resolve_video=VideoLoad(path=VIDEO_A),
        player_already_has_video=False,
        expected_record=True,
    ),
    RecordImportCase(
        name="re-import of current video, no comments: skips (preserves document)",
        scanned=VIDEO_CHOICE_SCAN,
        resolve_video=VideoLoad(path=VIDEO_A),
        player_already_has_video=True,
        expected_record=False,
    ),
    RecordImportCase(
        name="re-import of current video with comments: records",
        scanned=scan_with(videos=(VIDEO_A_FROM_DOCUMENT,), comments=COMMENTS),
        resolve_video=VideoLoad(path=VIDEO_A),
        player_already_has_video=True,
        expected_record=True,
    ),
    RecordImportCase(
        name="no video, has comments: records",
        scanned=scan_with(comments=COMMENTS),
        resolve_video=None,
        player_already_has_video=False,
        expected_record=True,
    ),
    RecordImportCase(
        name="no video, no comments: skips",
        scanned=EMPTY_SCAN,
        resolve_video=None,
        player_already_has_video=False,
        expected_record=False,
    ),
]


@pytest.mark.parametrize("case", RECORD_IMPORT_CASES, ids=lambda c: c.name)
def test_open_gates_state_record_import(
    qt_app,
    manual_executor: ManualJobExecutor,
    make_importer,
    make_spy,
    player_service_mock: MagicMock,
    state_service_mock: MagicMock,
    case: RecordImportCase,
) -> None:
    player_service_mock.is_any_video_loaded.return_value = case.player_already_has_video

    service = make_importer(case.scanned)
    spy = make_spy(service.pending_import_ready)
    service.open((), (), ())
    manual_executor.drain()

    if case.resolve_video is None:
        assert spy.count() == 0
    else:
        assert spy.count() == 1
        pending = spy.at(invocation=0, argument=0)
        pending.finish(session=NotAsked(), video=case.resolve_video, subtitles=NotAsked())

    if case.expected_record:
        state_service_mock.record_import.assert_called_once()
    else:
        state_service_mock.record_import.assert_not_called()


def test_finishing_with_a_replacing_session_resets_the_application(
    qt_app,
    manual_executor: ManualJobExecutor,
    make_importer,
    make_spy,
    comments_service_mock: MagicMock,
    reset_service_mock: MagicMock,
) -> None:
    comments_service_mock.count = 3

    service = make_importer(scan_with(comments=COMMENTS))
    spy = make_spy(service.pending_import_ready)
    service.open((), (), ())
    manual_executor.drain()

    assert spy.count() == 1
    spy.at(invocation=0, argument=0).finish(session=SessionReplace(), video=NotAsked(), subtitles=NotAsked())

    reset_service_mock.reset.assert_called_once()


def test_open_does_not_reset_for_a_merging_session(
    qt_app,
    manual_executor: ManualJobExecutor,
    make_importer,
    reset_service_mock: MagicMock,
) -> None:
    make_importer(EMPTY_SCAN).open((), (), ())
    manual_executor.drain()

    reset_service_mock.reset.assert_not_called()


def test_open_executes_a_plan_needing_no_decisions_without_the_wizard(
    qt_app,
    manual_executor: ManualJobExecutor,
    make_importer,
    make_spy,
    comments_service_mock: MagicMock,
) -> None:
    service = make_importer(scan_with(comments=COMMENTS))
    spy = make_spy(service.pending_import_ready)

    service.open((), (), ())
    manual_executor.drain()

    assert spy.count() == 0
    comments_service_mock.import_comments.assert_called_once_with(COMMENTS)


def test_open_without_comments_imports_nothing(
    qt_app,
    manual_executor: ManualJobExecutor,
    make_importer,
    comments_service_mock: MagicMock,
) -> None:
    make_importer(EMPTY_SCAN).open((), (), ())
    manual_executor.drain()

    comments_service_mock.import_comments.assert_not_called()


def test_open_announces_a_pending_import_for_a_scan_needing_decisions(
    qt_app,
    manual_executor: ManualJobExecutor,
    make_importer,
    make_spy,
    player_service_mock: MagicMock,
) -> None:
    service = make_importer(VIDEO_CHOICE_SCAN)
    spy = make_spy(service.pending_import_ready)

    service.open((), (), ())
    manual_executor.drain()

    assert spy.count() == 1
    assert spy.at(invocation=0, argument=0).plan == plan_with(video=UNRESOLVED_VIDEO)
    player_service_mock.open_media.assert_not_called()


class AnnouncedImport(NamedTuple):
    service: ImportService
    pending: PendingImport


@pytest.fixture
def pending_importer(
    qt_app,
    manual_executor: ManualJobExecutor,
    make_importer: Callable[[ScanResult], ImportService],
    make_spy,
) -> AnnouncedImport:
    service = make_importer(VIDEO_CHOICE_SCAN)
    spy = make_spy(service.pending_import_ready)
    service.open((), (), ())
    manual_executor.drain()
    return AnnouncedImport(service, spy.at(invocation=0, argument=0))


def test_dismiss_after_finish_changes_nothing(
    pending_importer: AnnouncedImport,
    manual_executor: ManualJobExecutor,
    make_spy,
    player_service_mock: MagicMock,
) -> None:
    # One close both finishes and dismisses, so the trailing dismissal must neither undo the import nor latch.
    pending_importer.pending.finish(session=NotAsked(), video=VideoLoad(path=VIDEO_A), subtitles=NotAsked())
    pending_importer.pending.dismiss()
    spy = make_spy(pending_importer.service.pending_import_ready)

    pending_importer.service.open((), (), ())
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

    pending_importer.service.open((), (), ())
    manual_executor.drain()

    assert spy.count() == 0
    assert "Skipping import while another is in progress" in caplog.text


def test_an_open_after_a_finish_proceeds(
    pending_importer: AnnouncedImport,
    manual_executor: ManualJobExecutor,
    make_spy,
) -> None:
    pending_importer.pending.finish(session=NotAsked(), video=VideoSkip(), subtitles=NotAsked())
    spy = make_spy(pending_importer.service.pending_import_ready)

    pending_importer.service.open((), (), ())
    manual_executor.drain()

    assert spy.count() == 1


def test_an_open_after_a_dismissal_proceeds(
    pending_importer: AnnouncedImport,
    manual_executor: ManualJobExecutor,
    make_spy,
) -> None:
    pending_importer.pending.dismiss()
    spy = make_spy(pending_importer.service.pending_import_ready)

    pending_importer.service.open((), (), ())
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
    pending_importer.service.open((), (), ())

    pending_importer.pending.dismiss()
    pending_importer.service.open((), (), ())
    manual_executor.drain()

    assert spy.count() == 1


def test_open_recovers_when_the_scan_raises(
    qt_app,
    manual_executor: ManualJobExecutor,
    make_spy,
    caplog: pytest.LogCaptureFixture,
) -> None:
    scans = 0

    def explode_once(*_args: object) -> ScanResult:
        nonlocal scans
        scans += 1
        if scans == 1:
            msg = "scan exploded"
            raise RuntimeError(msg)
        return VIDEO_CHOICE_SCAN

    service = ImportService(manual_executor, scan=explode_once)
    spy = make_spy(service.pending_import_ready)

    service.open((), (), ())
    manual_executor.drain()

    assert "Import scan failed" in caplog.text

    service.open((), (), ())
    manual_executor.drain()

    assert spy.count() == 1

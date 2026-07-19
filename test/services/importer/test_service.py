# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, NamedTuple
from unittest.mock import MagicMock

import inject
import pytest

from mpvqc.datamodels import Comment, VideoSource
from mpvqc.enums import ImportFoundVideo
from mpvqc.services.comments import CommentsService
from mpvqc.services.importer import FinishedPlan, ImporterService, UnfinishedPlan, errors, session, subtitles, video
from mpvqc.services.player import PlayerService
from mpvqc.services.resetter import ResetService
from mpvqc.services.settings import SettingsService
from mpvqc.services.state import StateService

if TYPE_CHECKING:
    from test.conftest import ManualJobExecutor


@pytest.fixture
def player_service_mock() -> MagicMock:
    mock = MagicMock(spec_set=PlayerService)
    mock.path = ""
    return mock


@pytest.fixture
def settings_service_mock() -> MagicMock:
    mock = MagicMock(spec_set=SettingsService)
    mock.import_found_video = ImportFoundVideo.ASK_EVERY_TIME.value
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
    settings_service_mock: MagicMock,
    state_service_mock: MagicMock,
    comments_service_mock: MagicMock,
    reset_service_mock: MagicMock,
) -> None:
    def config(binder: inject.Binder) -> None:
        binder.bind(PlayerService, player_service_mock)
        binder.bind(SettingsService, settings_service_mock)
        binder.bind(StateService, state_service_mock)
        binder.bind(CommentsService, comments_service_mock)
        binder.bind(ResetService, reset_service_mock)

    inject.configure(config, allow_override=True, bind_in_runtime=False, clear=True)


@pytest.fixture
def service(manual_executor: ManualJobExecutor) -> ImporterService:
    return ImporterService(manual_executor)


NOOP_PLAN = FinishedPlan(
    comments=(),
    session=session.Merge(),
    video=video.Skip(),
    subtitles=subtitles.Skip(),
)


def test_second_open_while_busy_is_ignored(service: ImporterService, make_spy) -> None:
    service.open([], [], [])
    spy = make_spy(service.busy_changed)
    service.open([], [], [])
    assert service.busy is True
    assert spy.count() == 0


def test_cancel_pending_unblocks_next_open(service: ImporterService, make_spy) -> None:
    service.open([], [], [])
    service.cancel_pending()
    spy = make_spy(service.busy_changed)
    service.open([], [], [])
    assert service.busy is True
    assert spy.count() == 1
    assert spy.at(invocation=0, argument=0) is True


def test_execute_unblocks_next_open(service: ImporterService, make_spy) -> None:
    service.open([], [], [])
    service.execute(NOOP_PLAN)
    spy = make_spy(service.busy_changed)
    service.open([], [], [])
    assert service.busy is True
    assert spy.count() == 1
    assert spy.at(invocation=0, argument=0) is True


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
def test_execute_dispatches_to_open_media(
    service: ImporterService,
    player_service_mock: MagicMock,
    case: DispatchCase,
) -> None:
    service.execute(case.plan)

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
            session=session.Merge(),
            video=video.Load(path=V),
            subtitles=subtitles.Skip(),
        ),
        player_already_has_video=False,
        expected_record=True,
    ),
    RecordImportCase(
        name="re-import of current video, no comments: skips (preserves document)",
        plan=FinishedPlan(
            comments=(),
            session=session.Merge(),
            video=video.Load(path=V),
            subtitles=subtitles.Skip(),
        ),
        player_already_has_video=True,
        expected_record=False,
    ),
    RecordImportCase(
        name="re-import of current video with comments: records",
        plan=FinishedPlan(
            comments=(MagicMock(),),
            session=session.Merge(),
            video=video.Load(path=V),
            subtitles=subtitles.Skip(),
        ),
        player_already_has_video=True,
        expected_record=True,
    ),
    RecordImportCase(
        name="no video, has comments: records",
        plan=FinishedPlan(
            comments=(MagicMock(),),
            session=session.Merge(),
            video=video.Skip(),
            subtitles=subtitles.Skip(),
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
def test_execute_gates_state_record_import(
    service: ImporterService,
    player_service_mock: MagicMock,
    state_service_mock: MagicMock,
    case: RecordImportCase,
) -> None:
    player_service_mock.is_any_video_loaded.return_value = case.player_already_has_video

    service.execute(case.plan)

    if case.expected_record:
        state_service_mock.record_import.assert_called_once()
    else:
        state_service_mock.record_import.assert_not_called()


COMMENTS = (Comment(time=0, comment_type="Translation", comment="Lorem ipsum"),)


def test_execute_replace_session_resets_application(
    service: ImporterService,
    reset_service_mock: MagicMock,
) -> None:
    plan = FinishedPlan(comments=(), session=session.Replace(), video=video.Skip(), subtitles=subtitles.Skip())

    service.execute(plan)

    reset_service_mock.reset.assert_called_once()


def test_execute_merge_session_does_not_reset(
    service: ImporterService,
    reset_service_mock: MagicMock,
) -> None:
    service.execute(NOOP_PLAN)

    reset_service_mock.reset.assert_not_called()


def test_execute_imports_comments(
    service: ImporterService,
    comments_service_mock: MagicMock,
) -> None:
    plan = FinishedPlan(comments=COMMENTS, session=session.Merge(), video=video.Skip(), subtitles=subtitles.Skip())

    service.execute(plan)

    comments_service_mock.import_comments.assert_called_once_with(COMMENTS)


def test_execute_without_comments_imports_nothing(
    service: ImporterService,
    comments_service_mock: MagicMock,
) -> None:
    service.execute(NOOP_PLAN)

    comments_service_mock.import_comments.assert_not_called()


UNRESOLVED_PLAN = UnfinishedPlan(
    comments=(),
    session=session.Merge(),
    video=video.Unresolved(candidates=(VideoSource(path=V, found_in_document=True),)),
    subtitles=subtitles.Skip(),
    errors=errors.Absent(),
)


def test_open_routes_resolvable_scan_to_execute(
    qt_app,
    monkeypatch: pytest.MonkeyPatch,
    service: ImporterService,
    manual_executor: ManualJobExecutor,
    make_spy,
) -> None:
    monkeypatch.setattr("mpvqc.services.importer.service.plan_import", lambda *_args, **_kwargs: NOOP_PLAN)
    unfinished_spy = make_spy(service.unfinished_plan_ready)

    service.open([], [], [])
    manual_executor.drain()

    assert unfinished_spy.count() == 0
    assert service.busy is False


def test_open_routes_unresolvable_scan_to_wizard(
    qt_app,
    monkeypatch: pytest.MonkeyPatch,
    service: ImporterService,
    manual_executor: ManualJobExecutor,
    make_spy,
) -> None:
    monkeypatch.setattr("mpvqc.services.importer.service.plan_import", lambda *_args, **_kwargs: UNRESOLVED_PLAN)
    unfinished_spy = make_spy(service.unfinished_plan_ready)

    service.open([], [], [])
    manual_executor.drain()

    assert unfinished_spy.count() == 1
    assert service.busy is True


def test_open_recovers_when_scan_raises(
    qt_app,
    monkeypatch: pytest.MonkeyPatch,
    service: ImporterService,
    manual_executor: ManualJobExecutor,
    caplog: pytest.LogCaptureFixture,
) -> None:
    def raise_scan_error(*_args: object, **_kwargs: object) -> FinishedPlan | UnfinishedPlan:
        msg = "scan exploded"
        raise RuntimeError(msg)

    monkeypatch.setattr("mpvqc.services.importer.service.plan_import", raise_scan_error)

    service.open([], [], [])
    manual_executor.drain()

    assert service.busy is False
    assert "Import scan failed" in caplog.text

    service.open([], [], [])
    assert service.busy is True

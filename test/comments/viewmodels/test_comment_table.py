# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from unittest.mock import MagicMock

import inject
import pytest
from PySide6.QtGui import QGuiApplication

from mpvqc.comments.services import CommentsService, CommentsSettingsService
from mpvqc.comments.viewmodels import MpvqcCommentTableViewModel
from mpvqc.player.services import PlayerService
from mpvqc.services import StateService
from mpvqc.shared import Comment


@pytest.fixture
def state_service_mock():
    return MagicMock(spec_set=StateService)


@pytest.fixture(autouse=True)
def configure_inject(
    common_bindings_with,
    comments_settings_service,
    fake_player_service,
    state_service_mock,
):
    def custom_bindings(binder: inject.Binder):
        binder.bind(PlayerService, fake_player_service)
        binder.bind(StateService, state_service_mock)
        binder.bind(CommentsSettingsService, comments_settings_service)

    common_bindings_with(custom_bindings)


@pytest.fixture(autouse=True)
def qt_app_must_be_running(qt_app):
    pass


@pytest.fixture
def comments_service() -> CommentsService:
    return inject.instance(CommentsService)


@pytest.fixture
def make_view_model(comments_service):
    def _make(comments: list[Comment]):
        # noinspection PyCallingNonCallable
        vm = MpvqcCommentTableViewModel()
        comments_service.import_comments(tuple(comments))
        return vm

    return _make


def test_state_changes_on_mutation(make_view_model, state_service_mock):
    vm = make_view_model(comments=[Comment(time=0, comment_type="Type", comment="text")])
    state_service_mock.reset_mock()  # ignore setup-time import dirty

    vm.removeRow(0)
    assert state_service_mock.record_change.call_count == 1

    vm.undo()
    assert state_service_mock.record_change.call_count == 2


def test_add_row_captures_exact_player_time(make_view_model, comments_service, fake_player_service):
    fake_player_service.update(time_pos=12.3454)
    vm = make_view_model(comments=[])

    vm.addRow("Translation")

    comment = comments_service.comments()[0]
    assert comment.time == 12345


@pytest.mark.parametrize(
    ("row", "expected"),
    [
        (0, "[00:01:40] [Phrasing] Comment Content 1"),
        (1, "[00:03:20] [Translation] Comment Content 2"),
        (2, "[00:05:00] [Spelling] Comment Content 3"),
    ],
)
def test_copy_to_clipboard(make_view_model, make_spy, row, expected):
    vm = make_view_model(
        comments=[
            Comment(time=100 * 1000, comment_type="Phrasing", comment="Comment Content 1"),
            Comment(time=200 * 1000, comment_type="Translation", comment="Comment Content 2"),
            Comment(time=300 * 1000, comment_type="Spelling", comment="Comment Content 3"),
        ]
    )
    spy = make_spy(vm.copiedToClipboard)

    vm.copyToClipboard(row)

    assert QGuiApplication.clipboard().text() == expected
    assert spy.count() == 1
    assert spy.at(invocation=0, argument=0) == expected


def test_settings_change_reaches_comment_types(make_view_model, comments_settings_service, make_spy):
    vm = make_view_model(comments=[])
    spy = make_spy(vm.commentTypesChanged)
    settled: list[list[str]] = []
    vm.commentTypesChanged.connect(lambda _: settled.append(vm.commentTypes))

    comments_settings_service.comment_types = ["Only One"]

    assert spy.count() == 1
    assert spy.at(invocation=0, argument=0) == ["Only One"]
    assert settled == [["Only One"]]


def test_player_change_reaches_video_duration(make_view_model, fake_player_service, make_spy):
    vm = make_view_model(comments=[])
    spy = make_spy(vm.videoDurationChanged)
    settled: list[float] = []
    vm.videoDurationChanged.connect(lambda _: settled.append(vm.videoDuration))

    fake_player_service.update(duration=42.5)

    assert spy.count() == 1
    assert spy.at(invocation=0, argument=0) == pytest.approx(42.5)
    assert settled == [pytest.approx(42.5)]


def test_import_reaches_comments_about_to_be_imported(make_view_model, comments_service, make_spy):
    vm = make_view_model(comments=[])
    spy = make_spy(vm.commentsAboutToBeImported)

    comments_service.import_comments((Comment(time=0, comment_type="Type", comment="text"),))

    assert spy.count() == 1


def test_add_row_reaches_quick_selection_and_edit(make_view_model, fake_player_service, make_spy):
    vm = make_view_model(comments=[Comment(time=0, comment_type="Type", comment="text")])
    fake_player_service.update(time_pos=5.0)
    quick_spy = make_spy(vm.quickSelectionRequested)
    animated_spy = make_spy(vm.selectionRequested)
    edit_spy = make_spy(vm.editCommentRequested)

    vm.addRow("Translation")

    assert quick_spy.count() == 1
    assert quick_spy.at(invocation=0, argument=0) == 1
    assert animated_spy.count() == 0
    assert edit_spy.count() == 1
    assert edit_spy.at(invocation=0, argument=0) == 1


def test_update_comment_type_reaches_quick_selection(make_view_model, make_spy):
    vm = make_view_model(
        comments=[
            Comment(time=0, comment_type="Type", comment="text"),
            Comment(time=1000, comment_type="Type", comment="text"),
        ]
    )
    quick_spy = make_spy(vm.quickSelectionRequested)
    animated_spy = make_spy(vm.selectionRequested)
    edit_spy = make_spy(vm.editCommentRequested)

    vm.updateCommentType(1, "Phrasing")

    assert quick_spy.count() == 1
    assert quick_spy.at(invocation=0, argument=0) == 1
    assert animated_spy.count() == 0
    assert edit_spy.count() == 0


def test_update_time_reaches_animated_selection(make_view_model, comments_service, make_spy):
    vm = make_view_model(
        comments=[
            Comment(time=0, comment_type="Type", comment="retimed"),
            Comment(time=1000, comment_type="Type", comment="first"),
            Comment(time=2000, comment_type="Type", comment="second"),
        ]
    )
    quick_spy = make_spy(vm.quickSelectionRequested)
    animated_spy = make_spy(vm.selectionRequested)
    edit_spy = make_spy(vm.editCommentRequested)

    vm.updateTime(0, 3000)

    texts = [comment.comment for comment in comments_service.comments()]
    assert texts == ["first", "second", "retimed"]
    assert quick_spy.count() == 0
    assert animated_spy.count() == 1
    assert animated_spy.at(invocation=0, argument=0) == texts.index("retimed")
    assert edit_spy.count() == 0


def test_remove_row_reaches_no_view_action(make_view_model, comments_service, make_spy):
    vm = make_view_model(comments=[Comment(time=0, comment_type="Type", comment="text")])
    quick_spy = make_spy(vm.quickSelectionRequested)
    animated_spy = make_spy(vm.selectionRequested)
    edit_spy = make_spy(vm.editCommentRequested)

    vm.removeRow(0)

    assert quick_spy.count() == 0
    assert animated_spy.count() == 0
    assert edit_spy.count() == 0
    assert comments_service.comments() == ()

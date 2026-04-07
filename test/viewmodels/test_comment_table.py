# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from unittest.mock import MagicMock

import inject
import pytest

from mpvqc.datamodels import Comment
from mpvqc.services import CommentsService, PlayerService, SettingsService, StateService
from mpvqc.viewmodels import MpvqcCommentTableViewModel


@pytest.fixture
def comments_service_mock():
    return MagicMock(spec_set=CommentsService)


@pytest.fixture(autouse=True)
def configure_inject(common_bindings_with, player_service_mock, settings_service, comments_service_mock):
    def custom_bindings(binder: inject.Binder):
        binder.bind(CommentsService, comments_service_mock)
        binder.bind(PlayerService, player_service_mock)
        binder.bind(StateService, MagicMock(spec_set=StateService))
        binder.bind(SettingsService, settings_service)

    common_bindings_with(custom_bindings)


@pytest.fixture(autouse=True)
def qt_app_must_be_running(qt_app):
    pass


@pytest.fixture
def make_view_model():
    def _make(comments: list[Comment]):
        # noinspection PyCallingNonCallable
        vm = MpvqcCommentTableViewModel()
        # pyrefly: ignore [missing-attribute]
        vm.model.import_comments(tuple(comments))
        return vm

    return _make


def test_registers_comments_service_on_construction(make_view_model, comments_service_mock):
    vm = make_view_model(comments=[])
    comments_service_mock.register.assert_called_once_with(vm.model)


def test_copy_to_clipboard(make_view_model, make_spy):
    vm = make_view_model(
        comments=[
            Comment(time=100, comment_type="Phrasing", comment="Comment Content 1"),
            Comment(time=200, comment_type="Translation", comment="Comment Content 2"),
            Comment(time=300, comment_type="Spelling", comment="Comment Content 3"),
        ]
    )

    spy = make_spy(vm.copiedToClipboard)

    vm.copyToClipboard(0)
    assert spy.at(0, 0) == "[00:01:40] [Phrasing] Comment Content 1"

    vm.copyToClipboard(1)
    assert spy.at(1, 0) == "[00:03:20] [Translation] Comment Content 2"

    vm.copyToClipboard(2)
    assert spy.at(2, 0) == "[00:05:00] [Spelling] Comment Content 3"

# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import inject
import pytest
from PySide6.QtCore import QObject, Signal

from mpvqc.comments.services import CommentsSettingsService
from mpvqc.comments.viewmodels import MpvqcCommentNewCommentMenuViewModel


class CommentsSettingsServiceMock(QObject):
    comment_types_changed = Signal(list)

    def __init__(self) -> None:
        super().__init__()
        assert isinstance(CommentsSettingsService.comment_types_changed, Signal), (
            "mocked surface drifted: not a signal anymore"
        )
        assert isinstance(CommentsSettingsService.comment_types, property), (
            "mocked surface drifted: not a property anymore"
        )
        self._comment_types = ["Translation"]

    @property
    def comment_types(self) -> list[str]:
        return self._comment_types

    def change_comment_types(self, comment_types: list[str]) -> None:
        self._comment_types = comment_types
        self.comment_types_changed.emit(comment_types)


@pytest.fixture(autouse=True)
def configure_inject(common_bindings_with, comments_settings_service_mock) -> None:
    def custom_bindings(binder: inject.Binder) -> None:
        binder.bind(CommentsSettingsService, comments_settings_service_mock)

    common_bindings_with(custom_bindings)


@pytest.fixture
def comments_settings_service_mock() -> CommentsSettingsServiceMock:
    return CommentsSettingsServiceMock()


@pytest.fixture
def view_model() -> MpvqcCommentNewCommentMenuViewModel:
    return MpvqcCommentNewCommentMenuViewModel()


def test_mirrors_settings_and_forwards_a_change(view_model, comments_settings_service_mock, make_spy):
    assert view_model.commentTypes == ["Translation"]

    spy = make_spy(view_model.commentTypesChanged)
    comments_settings_service_mock.change_comment_types(["Timing"])

    assert view_model.commentTypes == ["Timing"]
    assert spy.count() == 1
    assert spy.at(invocation=0, argument=0) == ["Timing"]

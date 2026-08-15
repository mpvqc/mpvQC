# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import inject
import pytest

from mpvqc.comments.services import CommentsSettingsService
from mpvqc.comments.viewmodels import MpvqcCommentNewCommentMenuViewModel


@pytest.fixture(autouse=True)
def configure_inject(common_bindings_with, comments_settings_service) -> None:
    def custom_bindings(binder: inject.Binder) -> None:
        binder.bind(CommentsSettingsService, comments_settings_service)

    common_bindings_with(custom_bindings)


def test_mirrors_settings_and_forwards_a_change(comments_settings_service, make_spy):
    comments_settings_service.comment_types = ["Translation"]
    view_model = MpvqcCommentNewCommentMenuViewModel()
    assert view_model.commentTypes == ["Translation"]

    spy = make_spy(view_model.commentTypesChanged)
    comments_settings_service.comment_types = ["Timing"]

    assert view_model.commentTypes == ["Timing"]
    assert spy.count() == 1
    assert spy.at(invocation=0, argument=0) == ["Timing"]

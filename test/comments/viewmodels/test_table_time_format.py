# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import inject
import pytest

from mpvqc.comments.services import CommentsService, TimeFormatPolicyService
from mpvqc.comments.viewmodels import MpvqcCommentTableTimeFormatViewModel
from mpvqc.services import PlayerService
from mpvqc.shared import Comment

ONE_HOUR_MS = 3_600_000


@pytest.fixture(autouse=True)
def configure_inject(common_bindings_with, fake_player_service):
    def custom_bindings(binder: inject.Binder):
        binder.bind(PlayerService, fake_player_service)
        binder.bind_to_constructor(TimeFormatPolicyService, TimeFormatPolicyService)

    common_bindings_with(custom_bindings)


@pytest.fixture
def comments() -> CommentsService:
    return inject.instance(CommentsService)


@pytest.fixture
def view_model() -> MpvqcCommentTableTimeFormatViewModel:
    # noinspection PyCallingNonCallable
    return MpvqcCommentTableTimeFormatViewModel()


def _comment_at(time: int) -> Comment:
    return Comment(time=time, comment_type="commentType", comment="")


def test_long_comment_flips_to_long_format_without_video(view_model, comments, make_spy):
    spy = make_spy(view_model.useLongFormatChanged)
    assert not view_model.useLongFormat

    comments.import_comments([_comment_at(ONE_HOUR_MS)])

    assert view_model.useLongFormat
    assert spy.count() == 1
    assert spy.at(invocation=0, argument=0) is True


def test_long_comment_with_shorter_video_uses_long_format(view_model, comments, fake_player_service):
    fake_player_service.load_video("/videos/video.mkv")
    fake_player_service.update(duration=125.0)
    assert not view_model.useLongFormat

    comments.import_comments([_comment_at(5_400_000)])

    assert view_model.useLongFormat


def test_undo_returns_to_short_format(view_model, comments):
    comments.import_comments([_comment_at(ONE_HOUR_MS)])
    assert view_model.useLongFormat

    comments.undo()

    assert not view_model.useLongFormat


def test_reset_returns_to_short_format(view_model, comments):
    comments.import_comments([_comment_at(ONE_HOUR_MS)])
    assert view_model.useLongFormat

    comments.reset()

    assert not view_model.useLongFormat


def test_duration_of_exactly_one_hour_uses_long_format(view_model, fake_player_service):
    fake_player_service.update(duration=3600.0)
    assert view_model.useLongFormat

    fake_player_service.update(duration=3599.0)
    assert not view_model.useLongFormat

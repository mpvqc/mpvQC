# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import inject
import pytest

from mpvqc.datamodels import Comment
from mpvqc.services import CommentsService, PlayerService, TimeFormatPolicyService
from mpvqc.viewmodels import MpvqcTableUtilityViewModel

ONE_HOUR_MS = 3_600_000


@pytest.fixture(autouse=True)
def configure_inject(common_bindings_with, player_service_mock):
    def custom_bindings(binder: inject.Binder):
        binder.bind(PlayerService, player_service_mock)
        binder.bind_to_constructor(TimeFormatPolicyService, TimeFormatPolicyService)

    common_bindings_with(custom_bindings)


@pytest.fixture
def comments() -> CommentsService:
    return inject.instance(CommentsService)


@pytest.fixture
def view_model() -> MpvqcTableUtilityViewModel:
    # noinspection PyCallingNonCallable
    return MpvqcTableUtilityViewModel()


def _comment_at(time: int) -> Comment:
    return Comment(time=time, comment_type="commentType", comment="")


def test_long_comment_flips_to_long_format_without_video(view_model, comments, make_spy):
    spy = make_spy(view_model.tableLongFormatChanged)
    assert view_model.tableLongFormat is False

    comments.import_comments([_comment_at(ONE_HOUR_MS)])

    assert view_model.tableLongFormat is True
    assert spy.count() == 1
    assert spy.at(invocation=0, argument=0) is True


def test_long_comment_with_shorter_video_uses_long_format(view_model, comments, player_service_mock):
    player_service_mock.update(video_loaded=True, duration=125.0)
    assert view_model.tableLongFormat is False

    comments.import_comments([_comment_at(5_400_000)])

    assert view_model.tableLongFormat is True


def test_undo_returns_to_short_format(view_model, comments):
    comments.import_comments([_comment_at(ONE_HOUR_MS)])
    assert view_model.tableLongFormat is True

    comments.undo()

    assert view_model.tableLongFormat is False


def test_reset_returns_to_short_format(view_model, comments):
    comments.import_comments([_comment_at(ONE_HOUR_MS)])
    assert view_model.tableLongFormat is True

    comments.reset()

    assert view_model.tableLongFormat is False


def test_duration_of_exactly_one_hour_uses_long_format(view_model, player_service_mock):
    player_service_mock.update(duration=3600.0)
    assert view_model.tableLongFormat is True

    player_service_mock.update(duration=3599.0)
    assert view_model.tableLongFormat is False

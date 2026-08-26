# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import inject
import pytest

from mpvqc.comments.services import CommentsService, TimeFormatPolicyService
from mpvqc.player.services import PlayerService
from mpvqc.shared import Comment

ONE_HOUR_MS = 3_600_000


@pytest.fixture
def comments_service() -> CommentsService:
    return inject.instance(CommentsService)


@pytest.fixture
def replace_comments(comments_service):
    def _replace_comments(*times: int) -> None:
        comments_service.reset()
        if times:
            comments_service.import_comments(
                tuple(Comment(time=time, comment_type="commentType", comment="") for time in times)
            )

    return _replace_comments


@pytest.fixture(autouse=True)
def configure_inject(common_bindings_with, fake_player_service):
    def custom_bindings(binder: inject.Binder):
        binder.bind(PlayerService, fake_player_service)

    common_bindings_with(custom_bindings)


@pytest.fixture(autouse=True)
def qt_app_must_be_running(qt_app):
    pass


@pytest.fixture
def policy() -> TimeFormatPolicyService:
    return TimeFormatPolicyService()


def test_duration_crossing_one_hour_flips_flag(policy, fake_player_service, make_spy):
    spy = make_spy(policy.table_long_format_changed)
    assert not policy.table_long_format

    fake_player_service.update(duration=3600.0)
    assert policy.table_long_format
    assert spy.count() == 1
    assert spy.at(invocation=0, argument=0) is True

    fake_player_service.update(duration=3599.0)
    assert not policy.table_long_format
    assert spy.count() == 2
    assert spy.at(invocation=1, argument=0) is False


def test_long_comment_appearing_and_disappearing_flips_flag(policy, replace_comments):
    replace_comments(0, ONE_HOUR_MS)
    assert policy.table_long_format

    replace_comments(0)
    assert not policy.table_long_format


def test_comment_times_normalize_from_milliseconds(policy, replace_comments):
    replace_comments(ONE_HOUR_MS - 1)
    assert not policy.table_long_format

    replace_comments(ONE_HOUR_MS)
    assert policy.table_long_format


def test_duration_and_comment_times_combine(policy, fake_player_service, replace_comments):
    fake_player_service.update(duration=3600.0)
    replace_comments(1_000)
    assert policy.table_long_format

    fake_player_service.update(duration=10.0)
    assert not policy.table_long_format

    replace_comments(1_000, ONE_HOUR_MS)
    assert policy.table_long_format


def test_reset_returns_flag_to_short(policy, replace_comments):
    replace_comments(ONE_HOUR_MS)
    assert policy.table_long_format

    replace_comments()
    assert not policy.table_long_format


def test_unchanged_flag_does_not_emit(policy, fake_player_service, replace_comments, make_spy):
    spy = make_spy(policy.table_long_format_changed)

    fake_player_service.update(duration=10.0)
    fake_player_service.update(duration=20.0)
    replace_comments(1_000)
    assert spy.count() == 0

    fake_player_service.update(duration=3600.0)
    replace_comments(1_000, ONE_HOUR_MS)
    assert spy.count() == 1


def test_flag_computes_at_construction(fake_player_service):
    fake_player_service.update(duration=7200.0)

    policy = TimeFormatPolicyService()

    assert policy.table_long_format

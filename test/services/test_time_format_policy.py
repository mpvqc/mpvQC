# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import inject
import pytest
from PySide6.QtCore import QObject, Signal

from mpvqc.datamodels import Comment
from mpvqc.services import CommentsService, PlayerService, TimeFormatPolicyService

ONE_HOUR_MS = 3_600_000


class CommentsServiceMock(QObject):
    """Doubles the comments service surface the policy consumes: a real signal, a stubbed accessor."""

    comments_changed = Signal()

    def __init__(self):
        super().__init__()
        assert isinstance(CommentsService.comments_changed, Signal), "mocked surface drifted: not a signal anymore"
        assert isinstance(CommentsService.count, property), "mocked surface drifted: not a property anymore"
        assert callable(CommentsService.comment_at), "mocked surface drifted: not a plain method anymore"
        self._comments: tuple[Comment, ...] = ()

    @property
    def count(self) -> int:
        return len(self._comments)

    def comment_at(self, row: int) -> Comment:
        return self._comments[row]

    def set_comments(self, *times: int) -> None:
        self._comments = tuple(Comment(time=time, comment_type="commentType", comment="") for time in sorted(times))
        self.comments_changed.emit()


@pytest.fixture
def comments_service_mock() -> CommentsServiceMock:
    return CommentsServiceMock()


@pytest.fixture(autouse=True)
def configure_inject(common_bindings_with, player_service_mock, comments_service_mock):
    def custom_bindings(binder: inject.Binder):
        binder.bind(PlayerService, player_service_mock)
        binder.bind(CommentsService, comments_service_mock)

    common_bindings_with(custom_bindings)


@pytest.fixture
def policy() -> TimeFormatPolicyService:
    return TimeFormatPolicyService()


@pytest.mark.parametrize(
    ("duration_seconds", "expected"),
    [
        (0, False),
        (3599, False),
        (3600, True),
        (3601, True),
    ],
)
def test_uses_long_format_is_inclusive_at_one_hour(duration_seconds, expected):
    assert TimeFormatPolicyService.uses_long_format(duration_seconds) is expected


def test_duration_crossing_one_hour_flips_flag(policy, player_service_mock, make_spy):
    spy = make_spy(policy.table_long_format_changed)
    assert policy.table_long_format is False

    player_service_mock.update(duration=3600.0)
    assert policy.table_long_format is True
    assert spy.count() == 1
    assert spy.at(invocation=0, argument=0) is True

    player_service_mock.update(duration=3599.0)
    assert policy.table_long_format is False
    assert spy.count() == 2
    assert spy.at(invocation=1, argument=0) is False


def test_long_comment_appearing_and_disappearing_flips_flag(policy, comments_service_mock):
    comments_service_mock.set_comments(0, ONE_HOUR_MS)
    assert policy.table_long_format is True

    comments_service_mock.set_comments(0)
    assert policy.table_long_format is False


def test_comment_times_normalize_from_milliseconds(policy, comments_service_mock):
    comments_service_mock.set_comments(ONE_HOUR_MS - 1)
    assert policy.table_long_format is False

    comments_service_mock.set_comments(ONE_HOUR_MS)
    assert policy.table_long_format is True


def test_duration_and_comment_times_combine(policy, player_service_mock, comments_service_mock):
    player_service_mock.update(duration=3600.0)
    comments_service_mock.set_comments(1_000)
    assert policy.table_long_format is True

    player_service_mock.update(duration=10.0)
    assert policy.table_long_format is False

    comments_service_mock.set_comments(1_000, ONE_HOUR_MS)
    assert policy.table_long_format is True


def test_reset_returns_flag_to_short(policy, comments_service_mock):
    comments_service_mock.set_comments(ONE_HOUR_MS)
    assert policy.table_long_format is True

    comments_service_mock.set_comments()
    assert policy.table_long_format is False


def test_unchanged_flag_does_not_emit(policy, player_service_mock, comments_service_mock, make_spy):
    spy = make_spy(policy.table_long_format_changed)

    player_service_mock.update(duration=10.0)
    player_service_mock.update(duration=20.0)
    comments_service_mock.set_comments(1_000)
    assert spy.count() == 0

    player_service_mock.update(duration=3600.0)
    comments_service_mock.set_comments(1_000, ONE_HOUR_MS)
    assert spy.count() == 1


def test_flag_computes_at_construction(player_service_mock):
    player_service_mock.update(duration=7200.0)

    policy = TimeFormatPolicyService()

    assert policy.table_long_format is True

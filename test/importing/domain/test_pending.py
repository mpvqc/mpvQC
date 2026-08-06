# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from typing import TYPE_CHECKING, NamedTuple

import pytest

from mpvqc.importing.domain import (
    FinishedPlan,
    PendingImport,
    SessionMerge,
    SubtitlesSkip,
    VideoLoad,
)
from test.importing.pending import record_pending
from test.importing.plans import UNRESOLVED_VIDEO, VIDEO_A, plan_with

if TYPE_CHECKING:
    from collections.abc import Callable

ASKS_ABOUT_VIDEO = plan_with(video=UNRESOLVED_VIDEO)

ANSWERED = FinishedPlan(
    comments=(),
    session=SessionMerge(),
    video=VideoLoad(path=VIDEO_A),
    subtitles=SubtitlesSkip(),
)


def test_finish_resolves_the_plan_and_delivers_it() -> None:
    pending, finished, dismissals = record_pending(ASKS_ABOUT_VIDEO)

    pending.finish(video=VideoLoad(path=VIDEO_A))

    assert finished == [ANSWERED]
    assert dismissals == []


def test_dismiss_delivers_the_dismissal() -> None:
    pending, finished, dismissals = record_pending(ASKS_ABOUT_VIDEO)

    pending.dismiss()

    assert finished == []
    assert dismissals == [True]


def finish(pending: PendingImport) -> None:
    pending.finish(video=VideoLoad(path=VIDEO_A))


def dismiss(pending: PendingImport) -> None:
    pending.dismiss()


class SpendCase(NamedTuple):
    name: str
    first: Callable[[PendingImport], None]
    second: Callable[[PendingImport], None]
    expected_finished: list[FinishedPlan]
    expected_dismissals: list[bool]


SPEND_CASES = [
    SpendCase("finish then dismiss", finish, dismiss, [ANSWERED], []),
    SpendCase("dismiss then finish", dismiss, finish, [], [True]),
    SpendCase("finish then finish", finish, finish, [ANSWERED], []),
    SpendCase("dismiss then dismiss", dismiss, dismiss, [], [True]),
]


@pytest.mark.parametrize("case", SPEND_CASES, ids=lambda c: c.name)
def test_the_first_outcome_decides(case: SpendCase) -> None:
    pending, finished, dismissals = record_pending(ASKS_ABOUT_VIDEO)

    case.first(pending)
    case.second(pending)

    assert finished == case.expected_finished
    assert dismissals == case.expected_dismissals


def test_a_finish_the_plan_rejects_leaves_the_import_dismissible() -> None:
    pending, finished, dismissals = record_pending(ASKS_ABOUT_VIDEO)

    with pytest.raises(RuntimeError):
        pending.finish()

    pending.dismiss()

    assert finished == []
    assert dismissals == [True]

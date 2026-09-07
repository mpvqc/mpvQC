# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from collections.abc import Callable
from typing import NamedTuple

import pytest

from mpvqc.comments.services import CommentsService
from mpvqc.shared import Comment


class MutationCase(NamedTuple):
    name: str
    mutate: Callable[[CommentsService], None]


@pytest.mark.parametrize(
    "case",
    [
        MutationCase(
            name="add",
            mutate=lambda c: c.add_row(25, "commentType"),
        ),
        MutationCase(
            name="update-text",
            mutate=lambda c: c.update_comment(0, "edited text"),
        ),
        MutationCase(
            name="update-type",
            mutate=lambda c: c.update_comment_type(0, "other type"),
        ),
        MutationCase(
            name="update-time",
            mutate=lambda c: c.update_time(0, 99),
        ),
        MutationCase(
            name="remove",
            mutate=lambda c: c.remove_row(0),
        ),
        MutationCase(
            name="import",
            mutate=lambda c: c.import_comments((Comment(time=99, comment_type="commentType", comment="Word 6"),)),
        ),
    ],
    ids=lambda case: case.name,
)
def test_mutation_fires_comments_changed(comments, make_spy, case: MutationCase):
    spy = make_spy(comments.comments_changed)

    case.mutate(comments)

    assert spy.count() == 1


def test_undo_redo_fire_comments_changed(comments, make_spy):
    comments.add_row(99, "commentType")
    spy = make_spy(comments.comments_changed)

    comments.undo()
    assert spy.count() == 1

    spy.reset()
    comments.redo()
    assert spy.count() == 1


def test_reset_fires_comments_changed(comments, make_spy):
    spy = make_spy(comments.comments_changed)

    comments.reset()

    assert spy.count() == 1

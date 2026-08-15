# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import pytest

from mpvqc.shared import Comment


@pytest.mark.parametrize(
    "mutate",
    [
        pytest.param(lambda c: c.add_row(25, "commentType"), id="add"),
        pytest.param(lambda c: c.update_comment(0, "edited text"), id="update-text"),
        pytest.param(lambda c: c.update_comment_type(0, "other type"), id="update-type"),
        pytest.param(lambda c: c.update_time(0, 99), id="update-time"),
        pytest.param(lambda c: c.remove_row(0), id="remove"),
        pytest.param(
            lambda c: c.import_comments((Comment(time=99, comment_type="commentType", comment="Word 6"),)),
            id="import",
        ),
    ],
)
def test_mutation_fires_comments_changed(comments, make_spy, mutate):
    spy = make_spy(comments.comments_changed)

    mutate(comments)

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

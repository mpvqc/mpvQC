# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import pytest

from mpvqc.datamodels import Comment
from mpvqc.models.comments import NoViewAction

DEFAULT_COMMENTS = (
    Comment(time=0, comment_type="commentType", comment="Word 1"),
    Comment(time=5, comment_type="commentType", comment="Word 2"),
    Comment(time=10, comment_type="commentType", comment="Word 3"),
    Comment(time=15, comment_type="commentType", comment="Word 4"),
    Comment(time=20, comment_type="commentType", comment="Word 5"),
)


@pytest.fixture
def model(make_model):
    # noinspection PyArgumentList
    return make_model(set_comments=DEFAULT_COMMENTS)


def test_clear_comments(model):
    model.clear_comments()
    assert model.rowCount() == 0


def test_clear_comments_fires_signals(model, make_spy):
    spy = make_spy(model.view_action)

    model.clear_comments()

    assert spy.count() == 1
    assert spy.at(invocation=0, argument=0) == NoViewAction()


def test_clear_comments_undo_redo(model):
    assert model.rowCount() == 5

    model.clear_comments()
    assert model.rowCount() == 0

    model.undo()
    assert model.rowCount() == 5
    assert [c["comment"] for c in model.comments()] == ["Word 1", "Word 2", "Word 3", "Word 4", "Word 5"]

    model.redo()
    assert model.rowCount() == 0


def test_clear_invalidates_search(model):
    initial = model.search("Word", include_current_row=True, top_down=True)
    assert initial.total == 5

    model.clear_comments()

    after = model.search("Word", include_current_row=True, top_down=True)
    assert after.total == 0


def test_clear_comments_undo_redo_fires_signals(model, make_spy):
    spy = make_spy(model.view_action)

    model.clear_comments()
    assert spy.count() == 1
    assert spy.at(invocation=0, argument=0) == NoViewAction()

    spy.reset()
    model.undo()
    assert spy.count() == 1
    assert spy.at(invocation=0, argument=0) == NoViewAction()

    spy.reset()
    model.redo()
    assert spy.count() == 1
    assert spy.at(invocation=0, argument=0) == NoViewAction()

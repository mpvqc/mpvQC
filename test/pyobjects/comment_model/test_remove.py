# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import pytest

from mpvqc.datamodels import Comment

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
    model, _ = make_model(
        set_comments=DEFAULT_COMMENTS,
        set_player_time=0,
    )
    return model


def test_remove_comment(model):
    assert model.rowCount() == 5
    model.remove_row(0)
    assert model.rowCount() == 4


def test_remove_comment_invalidates_search_results(model):
    model._searcher._hits = ["result"]

    model.remove_row(0)

    assert model._searcher._hits is None


def test_remove_comment_fires_signals(model, make_spy):
    removed_spy = make_spy(model.commentRemoved)

    model.remove_row(0)

    assert removed_spy.count() == 1


def test_remove_comment_undo_redo(model):
    assert model.rowCount() == 5

    model.remove_row(0)
    assert model.rowCount() == 4
    comment = model.comments()[0]
    assert comment["comment"] == "Word 2"

    model.undo()
    assert model.rowCount() == 5
    comment = model.comments()[0]
    assert comment["comment"] == "Word 1"

    model.redo()
    assert model.rowCount() == 4
    comment = model.comments()[0]
    assert comment["comment"] == "Word 2"


def test_remove_comment_undo_sorts_model(model):
    assert model.rowCount() == 5

    model.remove_row(1)
    expected = ["Word 1", "Word 3", "Word 4", "Word 5"]
    assert expected == [c["comment"] for c in model.comments()]

    model.undo()
    expected = ["Word 1", "Word 2", "Word 3", "Word 4", "Word 5"]
    assert expected == [c["comment"] for c in model.comments()]


def test_remove_comment_undo_redo_invalidates_search_results(model):
    model.remove_row(0)

    model._searcher._hits = ["result"]
    model.undo()
    assert model._searcher._hits is None

    model._searcher._hits = ["result"]
    model.redo()
    assert model._searcher._hits is None


def test_remove_comment_undo_redo_fires_signals(model, make_spy):
    removed_spy = make_spy(model.commentRemoved)
    removed_undone_spy = make_spy(model.commentRemovedUndone)

    model.remove_row(3)

    assert removed_spy.count() == 1
    assert removed_undone_spy.count() == 0

    removed_spy.reset()
    removed_undone_spy.reset()

    model.undo()

    assert removed_spy.count() == 0
    assert removed_undone_spy.count() == 1
    assert removed_undone_spy.at(invocation=0, argument=0) == 3

    removed_spy.reset()
    removed_undone_spy.reset()

    model.redo()

    assert removed_spy.count() == 1
    assert removed_undone_spy.count() == 0

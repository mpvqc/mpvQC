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


def test_clear_comments(model):
    model.clear_comments()
    assert model.rowCount() == 0


def test_clear_comments_fires_signals(model, make_spy):
    cleared_spy = make_spy(model.commentsCleared)

    model.clear_comments()

    assert cleared_spy.count() == 1


def test_clear_comments_undo_redo(model):
    assert model.rowCount() == 5

    model.clear_comments()
    assert model.rowCount() == 0

    model.undo()
    assert model.rowCount() == 5
    assert [c["comment"] for c in model.comments()] == ["Word 1", "Word 2", "Word 3", "Word 4", "Word 5"]

    model.redo()
    assert model.rowCount() == 0


def test_clear_comments_undo_redo_invalidates_search_results(model, make_spy):
    spy = make_spy(model.searchInvalidated)

    model.clear_comments()
    assert spy.count() == 1

    model.undo()
    assert spy.count() == 2

    model.redo()
    assert spy.count() == 3


def test_clear_comments_undo_redo_fires_signals(model, make_spy):
    cleared_spy = make_spy(model.commentsCleared)
    cleared_undone_spy = make_spy(model.commentsClearedUndone)

    model.clear_comments()
    assert cleared_spy.count() == 1
    assert cleared_undone_spy.count() == 0

    cleared_spy.reset()
    cleared_undone_spy.reset()

    model.undo()
    assert cleared_spy.count() == 0
    assert cleared_undone_spy.count() == 1

    cleared_spy.reset()
    cleared_undone_spy.reset()

    model.redo()
    assert cleared_spy.count() == 1
    assert cleared_undone_spy.count() == 0


def test_clear_comments_state_changes(model, state_service_mock):
    model.clear_comments()
    assert state_service_mock.change.call_count == 0

    model.undo()
    assert state_service_mock.change.call_count == 1

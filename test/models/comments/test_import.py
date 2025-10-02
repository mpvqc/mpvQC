# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import pytest

from mpvqc.datamodels import Comment

DEFAULT_COMMENTS = [
    Comment(time=0, comment_type="commentType", comment="Word 1"),
    Comment(time=5, comment_type="commentType", comment="Word 2"),
    Comment(time=10, comment_type="commentType", comment="Word 3"),
    Comment(time=15, comment_type="commentType", comment="Word 4"),
    Comment(time=20, comment_type="commentType", comment="Word 5"),
]


@pytest.fixture
def model(make_model):
    # noinspection PyArgumentList
    model, _ = make_model(
        set_comments=DEFAULT_COMMENTS,
        set_player_time=0,
    )
    return model


def test_import_comments(model):
    # noinspection PyTypeChecker
    comment = Comment(time=999.99, comment_type="commentType", comment="Word 1")

    assert model.rowCount() == 5
    model.import_comments([comment])
    assert model.rowCount() == 6

    # Ensure even importing float time properties results in time being stored as int
    assert model.comments()[-1]["time"] == 999


def test_import_sorts_comments(make_model):
    # noinspection PyArgumentList
    model, _ = make_model(
        set_comments=[],
        set_player_time=0,
    )

    comments = [
        Comment(time=1, comment_type="commentType", comment="Word 1"),
        Comment(time=2, comment_type="commentType", comment="Word 2"),
        Comment(time=1, comment_type="commentType", comment="Word 3"),
        Comment(time=2, comment_type="commentType", comment="Word 4"),
    ]

    model.import_comments(comments)
    assert [c["comment"] for c in model.comments()] == ["Word 1", "Word 3", "Word 2", "Word 4"]

    model.undo()
    assert not model.comments()

    model.redo()
    assert [c["comment"] for c in model.comments()] == ["Word 1", "Word 3", "Word 2", "Word 4"]


def test_import_comments_fires_signals(model, make_spy):
    initially_spy = make_spy(model.commentsImportedInitially)

    model.import_comments(DEFAULT_COMMENTS)

    assert initially_spy.count() == 1
    assert initially_spy.at(invocation=0, argument=0) == 9


def test_import_comments_undo_redo(model):
    comments = [
        Comment(time=1, comment_type="commentType", comment="Undo Redo 1"),
        Comment(time=6, comment_type="commentType", comment="Undo Redo 2"),
        Comment(time=11, comment_type="commentType", comment="Undo Redo 3"),
    ]
    assert model.rowCount() == 5

    model.import_comments(comments)
    assert model.rowCount() == 8
    comments = model.comments()
    assert comments[1]["comment"] == "Undo Redo 1"
    assert comments[3]["comment"] == "Undo Redo 2"
    assert comments[5]["comment"] == "Undo Redo 3"

    model.undo()
    assert model.rowCount() == 5
    comments = model.comments()
    assert comments[1]["comment"] == "Word 2"
    assert comments[3]["comment"] == "Word 4"

    model.redo()
    assert model.rowCount() == 8
    comments = model.comments()
    assert comments[1]["comment"] == "Undo Redo 1"
    assert comments[3]["comment"] == "Undo Redo 2"
    assert comments[5]["comment"] == "Undo Redo 3"


def test_import_comments_undo_redo_invalidates_search(model, make_spy):
    spy = make_spy(model.searchInvalidated)

    model.import_comments([(Comment(time=99, comment_type="commentType", comment="Word 1"))])
    assert spy.count() == 1

    model.undo()
    assert spy.count() == 2

    model.redo()
    assert spy.count() == 3


def test_import_comments_undo_redo_fires_signals(model, make_spy):
    initially_spy = make_spy(model.commentsImportedInitially)
    undone_spy = make_spy(model.commentsImportedUndone)
    redone_spy = make_spy(model.commentsImportedRedone)

    model.selectedRow = 3

    comment = Comment(time=99, comment_type="commentType", comment="Word 1")
    model.import_comments([comment])

    assert initially_spy.count() == 1
    assert initially_spy.at(invocation=0, argument=0) == 5
    assert undone_spy.count() == 0
    assert redone_spy.count() == 0

    initially_spy.reset()
    undone_spy.reset()
    redone_spy.reset()

    model.undo()

    assert initially_spy.count() == 0
    assert undone_spy.count() == 1
    assert undone_spy.at(invocation=0, argument=0) == 3
    assert redone_spy.count() == 0

    initially_spy.reset()
    undone_spy.reset()
    redone_spy.reset()

    model.redo()

    assert initially_spy.count() == 0
    assert undone_spy.count() == 0
    assert redone_spy.count() == 1
    assert redone_spy.at(invocation=0, argument=0) == 5


def test_import_comments_state_changes(model, state_service_mock):
    model.import_comments([Comment(time=25, comment_type="type", comment="test")])
    assert state_service_mock.change.call_count == 0

    model.undo()
    assert state_service_mock.change.call_count == 1

    model.redo()
    assert state_service_mock.change.call_count == 2

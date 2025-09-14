# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import pytest

from mpvqc.models import Comment
from mpvqc.pyobjects.comment_model.roles import Role

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


def test_add_comment(model):
    assert model.rowCount() == 5
    model.add_row("comment type")
    assert model.rowCount() == 6


@pytest.mark.parametrize(
    ("expected", "test_input"),
    [
        (0, 0.499999),
        (0, 0.500000),
        (1, 0.500001),
        (1, 1.499999),
        (2, 1.500001),
    ],
)
def test_add_comment_rounds_time(make_model, expected, test_input):
    # noinspection PyArgumentList
    model, _ = make_model(set_comments=[], set_player_time=test_input)

    model.add_row("comment type")

    item = model.item(0, 0)
    actual = item.data(Role.TIME)
    assert expected == actual


def test_add_comment_sorts_model(make_model):
    custom_comment_type = "my custom comment type"
    # noinspection PyArgumentList
    model, _ = make_model(set_comments=DEFAULT_COMMENTS, set_player_time=7)

    model.add_row(custom_comment_type)

    item = model.item(2, 0)
    actual = item.data(Role.TYPE)
    assert custom_comment_type == actual


def test_add_comment_invalidates_search_results(model):
    model._searcher._hits = ["result"]

    model.add_row("comment type")

    assert model._searcher._hits is None


def test_add_comment_fires_signals(model, make_spy):
    added_initially_spy = make_spy(model.newCommentAddedInitially)

    model.add_row("comment type")

    assert added_initially_spy.count() == 1


def test_add_comment_undo_redo(make_model):
    # noinspection PyArgumentList
    model, _ = make_model(set_comments=DEFAULT_COMMENTS, set_player_time=99)
    assert model.rowCount() == 5

    model.add_row("undo redo comment type")
    assert model.rowCount() == 6
    comment = model.comments()[-1]
    assert comment["commentType"] == "undo redo comment type"

    model.undo()
    assert model.rowCount() == 5
    comment = model.comments()[-1]
    assert comment["commentType"] != "undo redo comment type"

    model.redo()
    assert model.rowCount() == 6
    comment = model.comments()[-1]
    assert comment["commentType"] == "undo redo comment type"


def test_add_comment_undo_redo_sorts_model(make_model):
    # noinspection PyArgumentList
    model, _ = make_model(set_comments=DEFAULT_COMMENTS, set_player_time=7)

    model.add_row("undo redo comment type")
    expected = ["commentType", "commentType", "undo redo comment type", "commentType", "commentType", "commentType"]
    assert expected == [ct["commentType"] for ct in model.comments()]

    model.undo()
    expected = ["commentType", "commentType", "commentType", "commentType", "commentType"]
    assert expected == [ct["commentType"] for ct in model.comments()]

    model.redo()
    expected = ["commentType", "commentType", "undo redo comment type", "commentType", "commentType", "commentType"]
    assert expected == [ct["commentType"] for ct in model.comments()]


def test_add_comment_undo_redo_invalidates_search_results(model):
    model.add_row("undo redo comment type")

    model._searcher._hits = ["result"]
    model.undo()
    assert model._searcher._hits is None

    model._searcher._hits = ["result"]
    model.redo()
    assert model._searcher._hits is None


def test_add_comment_undo_redo_fires_signals(make_model, make_spy):
    # noinspection PyArgumentList
    model, _ = make_model(set_comments=DEFAULT_COMMENTS, set_player_time=99)

    new_initially_spy = make_spy(model.newCommentAddedInitially)
    new_undone_spy = make_spy(model.newCommentAddedUndone)
    new_redone_spy = make_spy(model.newCommentAddedRedone)

    model.set_selected_row(3)
    model.add_row("undo redo comment type")

    assert new_initially_spy.count() == 1
    assert new_initially_spy.at(invocation=0, argument=0) == 5
    assert new_undone_spy.count() == 0
    assert new_redone_spy.count() == 0

    new_initially_spy.reset()
    new_undone_spy.reset()
    new_redone_spy.reset()

    model.undo()

    assert new_initially_spy.count() == 0
    assert new_undone_spy.count() == 1
    assert new_undone_spy.at(invocation=0, argument=0) == 3
    assert new_redone_spy.count() == 0

    new_initially_spy.reset()
    new_undone_spy.reset()
    new_redone_spy.reset()

    model.redo()

    assert new_initially_spy.count() == 0
    assert new_undone_spy.count() == 0
    assert new_redone_spy.count() == 1
    assert new_redone_spy.at(invocation=0, argument=0) == 5

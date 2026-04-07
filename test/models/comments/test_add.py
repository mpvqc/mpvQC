# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import pytest

from mpvqc.datamodels import Comment
from mpvqc.models.comments.mutation import QuickSelection, RowAddEdit
from mpvqc.models.comments.roles import Role

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


def test_add_comment_sorts_model(make_model):
    custom_comment_type = "my custom comment type"
    # noinspection PyArgumentList
    model, _ = make_model(set_comments=DEFAULT_COMMENTS, set_player_time=7)

    model.add_row(custom_comment_type)

    item = model.item(2, 0)
    actual = item.data(Role.TYPE)
    assert custom_comment_type == actual


def test_add_comment_fires_signals(model, make_spy):
    spy = make_spy(model.mutated)

    model.add_row("comment type")

    assert spy.count() == 1
    assert isinstance(spy.at(invocation=0, argument=0), RowAddEdit)


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


def test_add_comment_undo_redo_invalidates_search_results(model, make_spy):
    spy = make_spy(model.search_invalidated)

    model.add_row("undo redo comment type")
    assert spy.count() == 1

    model.undo()
    assert spy.count() == 2

    model.redo()
    assert spy.count() == 3


def test_add_comment_undo_redo_fires_signals(make_model, make_spy):
    # noinspection PyArgumentList
    model, _ = make_model(set_comments=DEFAULT_COMMENTS, set_player_time=99)

    spy = make_spy(model.mutated)

    model.selectedRow = 3
    model.add_row("undo redo comment type")

    assert spy.count() == 1
    assert spy.at(invocation=0, argument=0) == RowAddEdit(row=5)

    spy.reset()
    model.undo()

    assert spy.count() == 1
    assert spy.at(invocation=0, argument=0) == QuickSelection(row=3)

    spy.reset()
    model.redo()

    assert spy.count() == 1
    assert spy.at(invocation=0, argument=0) == QuickSelection(row=5)

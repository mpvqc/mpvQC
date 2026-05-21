# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import pytest

from mpvqc.datamodels import Comment
from mpvqc.models.comments import NoViewAction, QuickSelection, QuickSelectionAndEdit

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
    return make_model(set_comments=DEFAULT_COMMENTS)


def test_add_comment(model):
    assert model.rowCount() == 5
    model.add_row(0, "comment type")
    assert model.rowCount() == 6


def test_add_comment_sorts_model(make_model):
    custom_comment_type = "my custom comment type"
    # noinspection PyArgumentList
    model = make_model(set_comments=DEFAULT_COMMENTS)

    model.add_row(7, custom_comment_type)

    actual = model.comment_at(2).comment_type
    assert custom_comment_type == actual


def test_add_comment_fires_signals(model, make_spy):
    spy = make_spy(model.view_action)

    model.add_row(0, "comment type")

    assert spy.count() == 1
    assert isinstance(spy.at(invocation=0, argument=0), QuickSelectionAndEdit)


def test_add_comment_undo_redo(make_model):
    # noinspection PyArgumentList
    model = make_model(set_comments=DEFAULT_COMMENTS)
    assert model.rowCount() == 5

    model.add_row(99, "undo redo comment type")
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
    model = make_model(set_comments=DEFAULT_COMMENTS)

    model.add_row(7, "undo redo comment type")
    expected = ["commentType", "commentType", "undo redo comment type", "commentType", "commentType", "commentType"]
    assert expected == [ct["commentType"] for ct in model.comments()]

    model.undo()
    expected = ["commentType", "commentType", "commentType", "commentType", "commentType"]
    assert expected == [ct["commentType"] for ct in model.comments()]

    model.redo()
    expected = ["commentType", "commentType", "undo redo comment type", "commentType", "commentType", "commentType"]
    assert expected == [ct["commentType"] for ct in model.comments()]


def test_add_row_invalidates_search(model):
    initial = model.search("Word", include_current_row=True, top_down=True)
    assert initial.index == 0
    assert initial.total == 5

    # New row inserts at row 0; existing matches shift to rows 1..5.
    model.add_row(time=-1, comment_type="commentType")

    after = model.search("Word", include_current_row=True, top_down=True)
    assert after.index == 1
    assert after.total == 5


def test_add_comment_undo_redo_fires_signals(make_model, make_spy):
    # noinspection PyArgumentList
    model = make_model(set_comments=DEFAULT_COMMENTS)

    spy = make_spy(model.view_action)

    model.add_row(99, "undo redo comment type")

    assert spy.count() == 1
    assert spy.at(invocation=0, argument=0) == QuickSelectionAndEdit(row=5)

    spy.reset()
    model.undo()

    assert spy.count() == 1
    assert spy.at(invocation=0, argument=0) == NoViewAction()

    spy.reset()
    model.redo()

    assert spy.count() == 1
    assert spy.at(invocation=0, argument=0) == QuickSelection(row=5)

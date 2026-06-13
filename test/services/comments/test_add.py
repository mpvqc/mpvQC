# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from mpvqc.services.comments import NoViewAction, QuickSelection, QuickSelectionAndEdit


def test_add_comment(comments):
    assert comments.count == 5
    comments.add_row(0, "comment type")
    assert comments.count == 6


def test_add_comment_sorts_model(comments):
    custom_comment_type = "my custom comment type"

    comments.add_row(7, custom_comment_type)

    actual = comments.comment_at(2).comment_type
    assert custom_comment_type == actual


def test_add_comment_fires_signals(comments, make_spy):
    spy = make_spy(comments.view_action)

    comments.add_row(0, "comment type")

    assert spy.count() == 1
    assert isinstance(spy.at(invocation=0, argument=0), QuickSelectionAndEdit)


def test_add_comment_undo_redo(comments):
    assert comments.count == 5

    comments.add_row(99, "undo redo comment type")
    assert comments.count == 6
    comment = comments.comments()[-1]
    assert comment.comment_type == "undo redo comment type"

    comments.undo()
    assert comments.count == 5
    comment = comments.comments()[-1]
    assert comment.comment_type != "undo redo comment type"

    comments.redo()
    assert comments.count == 6
    comment = comments.comments()[-1]
    assert comment.comment_type == "undo redo comment type"


def test_add_comment_undo_redo_sorts_model(comments):
    comments.add_row(7, "undo redo comment type")
    expected = ["commentType", "commentType", "undo redo comment type", "commentType", "commentType", "commentType"]
    assert expected == [ct.comment_type for ct in comments.comments()]

    comments.undo()
    expected = ["commentType", "commentType", "commentType", "commentType", "commentType"]
    assert expected == [ct.comment_type for ct in comments.comments()]

    comments.redo()
    expected = ["commentType", "commentType", "undo redo comment type", "commentType", "commentType", "commentType"]
    assert expected == [ct.comment_type for ct in comments.comments()]


def test_add_row_invalidates_search(comments):
    initial = comments.search("Word", include_current_row=True, top_down=True)
    assert initial.index == 0
    assert initial.total == 5

    # New row inserts at row 0; existing matches shift to rows 1..5.
    comments.add_row(time=-1, comment_type="commentType")

    after = comments.search("Word", include_current_row=True, top_down=True)
    assert after.index == 1
    assert after.total == 5


def test_add_comment_undo_redo_fires_signals(comments, make_spy):
    spy = make_spy(comments.view_action)

    comments.add_row(99, "undo redo comment type")

    assert spy.count() == 1
    assert spy.at(invocation=0, argument=0) == QuickSelectionAndEdit(row=5)

    spy.reset()
    comments.undo()

    assert spy.count() == 1
    assert spy.at(invocation=0, argument=0) == NoViewAction()

    spy.reset()
    comments.redo()

    assert spy.count() == 1
    assert spy.at(invocation=0, argument=0) == QuickSelection(row=5)

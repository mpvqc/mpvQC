# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from mpvqc.models.comments import NoViewAction, QuickSelection


def test_remove_comment(comments):
    assert comments.rowCount() == 5
    comments.remove_row(0)
    assert comments.rowCount() == 4


def test_remove_comment_fires_signals(comments, make_spy):
    spy = make_spy(comments.view_action)

    comments.remove_row(0)

    assert spy.count() == 1
    assert spy.at(invocation=0, argument=0) == NoViewAction()


def test_remove_comment_undo_redo(comments):
    assert comments.rowCount() == 5

    comments.remove_row(0)
    assert comments.rowCount() == 4
    comment = comments.comments()[0]
    assert comment["comment"] == "Word 2"

    comments.undo()
    assert comments.rowCount() == 5
    comment = comments.comments()[0]
    assert comment["comment"] == "Word 1"

    comments.redo()
    assert comments.rowCount() == 4
    comment = comments.comments()[0]
    assert comment["comment"] == "Word 2"


def test_remove_comment_undo_sorts_model(comments):
    assert comments.rowCount() == 5

    comments.remove_row(1)
    expected = ["Word 1", "Word 3", "Word 4", "Word 5"]
    assert expected == [c["comment"] for c in comments.comments()]

    comments.undo()
    expected = ["Word 1", "Word 2", "Word 3", "Word 4", "Word 5"]
    assert expected == [c["comment"] for c in comments.comments()]


def test_remove_invalidates_search(comments):
    initial = comments.search("Word", include_current_row=True, top_down=True)
    assert initial.total == 5

    comments.remove_row(0)

    after = comments.search("Word", include_current_row=True, top_down=True)
    assert after.total == 4


def test_remove_comment_undo_redo_fires_signals(comments, make_spy):
    spy = make_spy(comments.view_action)

    comments.remove_row(3)

    assert spy.count() == 1
    assert spy.at(invocation=0, argument=0) == NoViewAction()

    spy.reset()
    comments.undo()

    assert spy.count() == 1
    assert spy.at(invocation=0, argument=0) == QuickSelection(row=3)

    spy.reset()
    comments.redo()

    assert spy.count() == 1
    assert spy.at(invocation=0, argument=0) == NoViewAction()

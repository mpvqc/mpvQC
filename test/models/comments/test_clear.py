# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from mpvqc.models.comments import NoViewAction


def test_clear_comments(comments):
    comments.clear_comments()
    assert comments.rowCount() == 0


def test_clear_comments_fires_signals(comments, make_spy):
    spy = make_spy(comments.view_action)

    comments.clear_comments()

    assert spy.count() == 1
    assert spy.at(invocation=0, argument=0) == NoViewAction()


def test_clear_comments_undo_redo(comments):
    assert comments.rowCount() == 5

    comments.clear_comments()
    assert comments.rowCount() == 0

    comments.undo()
    assert comments.rowCount() == 5
    assert [c["comment"] for c in comments.comments()] == ["Word 1", "Word 2", "Word 3", "Word 4", "Word 5"]

    comments.redo()
    assert comments.rowCount() == 0


def test_clear_invalidates_search(comments):
    initial = comments.search("Word", include_current_row=True, top_down=True)
    assert initial.total == 5

    comments.clear_comments()

    after = comments.search("Word", include_current_row=True, top_down=True)
    assert after.total == 0


def test_clear_comments_undo_redo_fires_signals(comments, make_spy):
    spy = make_spy(comments.view_action)

    comments.clear_comments()
    assert spy.count() == 1
    assert spy.at(invocation=0, argument=0) == NoViewAction()

    spy.reset()
    comments.undo()
    assert spy.count() == 1
    assert spy.at(invocation=0, argument=0) == NoViewAction()

    spy.reset()
    comments.redo()
    assert spy.count() == 1
    assert spy.at(invocation=0, argument=0) == NoViewAction()

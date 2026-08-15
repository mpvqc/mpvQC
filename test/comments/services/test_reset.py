# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from mpvqc.comments.services import Found, NoMatches


def test_reset_empties_store(comments):
    comments.reset()

    assert comments.count == 0


def test_reset_clears_undo_history(comments):
    comments.remove_row(0)

    comments.reset()
    comments.undo()
    comments.undo()

    assert comments.count == 0


def test_reset_clears_redo_history(comments):
    comments.add_row(25, "commentType")
    comments.selection.set_row_visible(True)
    comments.undo()

    comments.reset()
    comments.redo()

    assert comments.count == 0


def test_reset_clears_selection(comments):
    comments.selection.select(3)

    comments.reset()

    assert comments.selection.row == -1


def test_reset_invalidates_search(comments):
    outcome = comments.search("Word", include_current_row=True, top_down=True)
    assert isinstance(outcome, Found)
    assert outcome.total == 5

    comments.reset()

    assert comments.search("Word", include_current_row=True, top_down=True) == NoMatches()


def test_reset_does_not_mark_dirty(comments, make_spy):
    spy = make_spy(comments.dirty)

    comments.reset()

    assert spy.count() == 0

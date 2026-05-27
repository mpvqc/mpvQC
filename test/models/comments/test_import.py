# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from mpvqc.datamodels import Comment
from mpvqc.models.comments import QuickSelection


def test_import_comments(comments):
    comment = Comment(time=999, comment_type="commentType", comment="Word 1")

    assert comments.rowCount() == 5
    comments.import_comments((comment,))
    assert comments.rowCount() == 6
    assert comments.comments()[-1]["time"] == 999


def test_import_sorts_comments(make_facade):
    comments = make_facade(set_comments=[])

    to_import = (
        Comment(time=1, comment_type="commentType", comment="Word 1"),
        Comment(time=2, comment_type="commentType", comment="Word 2"),
        Comment(time=1, comment_type="commentType", comment="Word 3"),
        Comment(time=2, comment_type="commentType", comment="Word 4"),
    )

    comments.import_comments(to_import)
    assert [c["comment"] for c in comments.comments()] == ["Word 1", "Word 3", "Word 2", "Word 4"]

    comments.undo()
    assert not comments.comments()

    comments.redo()
    assert [c["comment"] for c in comments.comments()] == ["Word 1", "Word 3", "Word 2", "Word 4"]


def test_import_unsorted_focuses_time_maximum(make_facade, make_spy):
    comments = make_facade(set_comments=[])
    spy = make_spy(comments.view_action)

    comments.import_comments(
        (
            Comment(time=100, comment_type="commentType", comment="latest"),
            Comment(time=10, comment_type="commentType", comment="earliest"),
            Comment(time=50, comment_type="commentType", comment="middle"),
        )
    )

    assert spy.at(invocation=0, argument=0) == QuickSelection(row=2)


def test_import_comments_fires_signals(comments, make_spy, default_comments):
    spy = make_spy(comments.view_action)

    comments.import_comments(default_comments)

    assert spy.count() == 1
    assert spy.at(invocation=0, argument=0) == QuickSelection(row=9)


def test_import_comments_emits_about_to_be_imported(comments, make_spy, default_comments):
    spy = make_spy(comments.about_to_import)

    comments.import_comments(default_comments)

    assert spy.count() == 1


def test_import_comments_empty_does_not_emit_about_to_be_imported(comments, make_spy):
    spy = make_spy(comments.about_to_import)

    comments.import_comments([])

    assert spy.count() == 0


def test_import_comments_undo_redo(comments):
    to_import = (
        Comment(time=1, comment_type="commentType", comment="Undo Redo 1"),
        Comment(time=6, comment_type="commentType", comment="Undo Redo 2"),
        Comment(time=11, comment_type="commentType", comment="Undo Redo 3"),
    )
    assert comments.rowCount() == 5

    comments.import_comments(to_import)
    assert comments.rowCount() == 8
    rows = comments.comments()
    assert rows[1]["comment"] == "Undo Redo 1"
    assert rows[3]["comment"] == "Undo Redo 2"
    assert rows[5]["comment"] == "Undo Redo 3"

    comments.undo()
    assert comments.rowCount() == 5
    rows = comments.comments()
    assert rows[1]["comment"] == "Word 2"
    assert rows[3]["comment"] == "Word 4"

    comments.redo()
    assert comments.rowCount() == 8
    rows = comments.comments()
    assert rows[1]["comment"] == "Undo Redo 1"
    assert rows[3]["comment"] == "Undo Redo 2"
    assert rows[5]["comment"] == "Undo Redo 3"


def test_import_invalidates_search(comments):
    initial = comments.search("Word", include_current_row=True, top_down=True)
    assert initial.total == 5

    comments.import_comments((Comment(time=99, comment_type="commentType", comment="Word New"),))

    after = comments.search("Word", include_current_row=True, top_down=True)
    assert after.total == 6


def test_import_comments_undo_redo_fires_signals(comments, make_spy):
    spy = make_spy(comments.view_action)

    comments.selection.selectedRow = 3

    comment = Comment(time=99, comment_type="commentType", comment="Word 1")
    comments.import_comments((comment,))

    assert spy.count() == 1
    assert spy.at(invocation=0, argument=0) == QuickSelection(row=5)

    spy.reset()
    comments.undo()

    assert spy.count() == 1
    assert spy.at(invocation=0, argument=0) == QuickSelection(row=3)

    spy.reset()
    comments.redo()

    assert spy.count() == 1
    assert spy.at(invocation=0, argument=0) == QuickSelection(row=5)

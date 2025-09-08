# mpvQC
#
# Copyright (C) 2024 mpvQC developers
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import pytest

from mpvqc.models import Comment

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


def test_import_comments_invalidates_search_results(model):
    model._searcher._hits = ["result"]

    model.import_comments(DEFAULT_COMMENTS)

    assert model._searcher._hits is None


def test_import_comments_fires_signals(model, signal_helper):
    model.commentsImportedInitially.connect(lambda val: signal_helper.log("commentsImportedInitially", val))

    model.import_comments(DEFAULT_COMMENTS)

    assert signal_helper.has_logged("commentsImportedInitially")
    assert signal_helper.logged_value("commentsImportedInitially") == 9


def test_import_comments_undo_redo(model):
    # noinspection PyTypeChecker
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


def test_import_comments_undo_redo_invalidates_search(model):
    comment = Comment(time=99, comment_type="commentType", comment="Word 1")
    model.import_comments([comment])

    model._searcher._hits = ["result"]
    model.undo()
    assert model._searcher._hits is None

    model._searcher._hits = ["result"]
    model.redo()
    assert model._searcher._hits is None


def test_import_comments_undo_redo_fires_signals(model, signal_helper):
    model.commentsImportedInitially.connect(lambda val: signal_helper.log("commentsImportedInitially", val))
    model.commentsImportedUndone.connect(lambda val: signal_helper.log("commentsImportedUndone", val))
    model.commentsImportedRedone.connect(lambda val: signal_helper.log("commentsImportedRedone", val))
    model.set_selected_row(3)

    comment = Comment(time=99, comment_type="commentType", comment="Word 1")
    model.import_comments([comment])

    assert signal_helper.has_logged("commentsImportedInitially")
    assert signal_helper.logged_value("commentsImportedInitially") == 5
    assert not signal_helper.has_logged("commentsImportedUndone")
    assert not signal_helper.has_logged("commentsImportedRedone")

    signal_helper.reset()
    model.undo()

    assert not signal_helper.has_logged("commentsImportedInitially")
    assert signal_helper.has_logged("commentsImportedUndone")
    assert signal_helper.logged_value("commentsImportedUndone") == 3
    assert not signal_helper.has_logged("commentsImportedRedone")

    signal_helper.reset()
    model.redo()

    assert not signal_helper.has_logged("commentsImportedInitially")
    assert not signal_helper.has_logged("commentsImportedUndone")
    assert signal_helper.has_logged("commentsImportedRedone")
    assert signal_helper.logged_value("commentsImportedRedone") == 5

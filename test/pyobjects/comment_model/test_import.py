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


@pytest.fixture()
def model(make_model):
    # noinspection PyArgumentList
    return make_model(
        set_comments=DEFAULT_COMMENTS,
        set_player_time=0,
    )


def test_import_comments(model):
    # noinspection PyTypeChecker
    comment = Comment(time=999.99, comment_type="commentType", comment="Word 1")

    assert model.rowCount() == 5
    model.import_comments([comment])
    assert model.rowCount() == 6

    # Ensure even importing float time properties results in time being stored as int
    assert 999 == model.comments()[-1]["time"]


def test_import_comments_invalidates_search_results(model):
    model._searcher._hits = ["result"]

    model.import_comments(DEFAULT_COMMENTS)

    assert model._searcher._hits is None


def test_import_comments_fires_signals(model, signal_helper):
    model.commentsImported.connect(lambda: signal_helper.log("commentsImported"))

    model.import_comments(DEFAULT_COMMENTS)

    assert signal_helper.has_logged("commentsImported")


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


# todo
#   - fix selecting the last imported comment (also fix the signal to send an index up through the qml layer)
#      extend the test cases that check these signals are fired (in python) including the index
#   - introduce a signal that fires after an import has been undone,
#      the index param must be the row that has been selected before importing
#      add test that confirms this signal is fired on undo action
#   - within this test also check that the 'commentsImported' signal fires again after redo action

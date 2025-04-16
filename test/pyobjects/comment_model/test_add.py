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


def test_add_comment_fires_signals(model, signal_helper):
    model.newCommentAddedInitially.connect(lambda idx: signal_helper.log("newCommentAddedInitially", idx))

    model.add_row("comment type")

    assert signal_helper.has_logged("newCommentAddedInitially")


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


def test_add_comment_undo_redo_fires_signals(make_model, signal_helper):
    # noinspection PyArgumentList
    model, _ = make_model(set_comments=DEFAULT_COMMENTS, set_player_time=99)
    model.newCommentAddedInitially.connect(lambda val: signal_helper.log("newCommentAddedInitially", val))
    model.newCommentAddedRedone.connect(lambda val: signal_helper.log("newCommentAddedRedone", val))
    model.newCommentAddedUndone.connect(lambda val: signal_helper.log("newCommentAddedUndone", val))
    model.set_selected_row(3)

    model.add_row("undo redo comment type")
    assert signal_helper.has_logged("newCommentAddedInitially")
    assert not signal_helper.has_logged("newCommentAddedUndone")
    assert not signal_helper.has_logged("newCommentAddedRedone")
    assert signal_helper.logged_value("newCommentAddedInitially") == 5

    signal_helper.reset()
    model.undo()

    assert not signal_helper.has_logged("newCommentAddedInitially")
    assert signal_helper.has_logged("newCommentAddedUndone")
    assert not signal_helper.has_logged("newCommentAddedRedone")
    assert signal_helper.logged_value("newCommentAddedUndone") == 3

    signal_helper.reset()
    model.redo()

    assert not signal_helper.has_logged("newCommentAddedInitially")
    assert not signal_helper.has_logged("newCommentAddedUndone")
    assert signal_helper.has_logged("newCommentAddedRedone")
    assert signal_helper.logged_value("newCommentAddedRedone") == 5

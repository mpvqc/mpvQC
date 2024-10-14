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
from mpvqc.pyobjects.comment_model import Role

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


def test_add_comment(model):
    assert model.rowCount() == 5
    model.add_row("comment type")
    assert model.rowCount() == 6


@pytest.mark.parametrize(
    "expected,test_input",
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
    model = make_model(set_comments=[], set_player_time=test_input)

    model.add_row("comment type")

    item = model.item(0, 0)
    actual = item.data(Role.TIME)
    assert expected == actual


def test_add_comment_sorts_model(make_model):
    custom_comment_type = "my custom comment type"
    # noinspection PyArgumentList
    model = make_model(set_comments=DEFAULT_COMMENTS, set_player_time=7)

    model.add_row(custom_comment_type)

    item = model.item(2, 0)
    actual = item.data(Role.TYPE)
    assert custom_comment_type == actual


def test_add_comment_invalidates_search_results(model):
    model._searcher._hits = ["result"]

    model.add_row("comment type")

    assert model._searcher._hits is None


def test_add_comment_fires_signals(model, signal_helper):
    model.commentsChanged.connect(lambda: signal_helper.log("commentsChanged"))
    model.newItemAdded.connect(lambda idx: signal_helper.log("newItemAdded", idx))

    model.add_row("comment type")

    assert signal_helper.has_logged("commentsChanged")
    assert signal_helper.has_logged("newItemAdded")

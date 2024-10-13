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

DEFAULT_COMMENTS = (
    Comment(time=0, comment_type="commentType", comment="Word 1"),
    Comment(time=5, comment_type="commentType", comment="Word 2"),
    Comment(time=10, comment_type="commentType", comment="Word 3"),
    Comment(time=15, comment_type="commentType", comment="Word 4"),
    Comment(time=20, comment_type="commentType", comment="Word 5"),
)


@pytest.fixture()
def model(make_model):
    # noinspection PyArgumentList
    return make_model(
        set_comments=DEFAULT_COMMENTS,
        set_player_time=0,
    )


def test_update_time_sorts_model_again(model):
    model.update_time(row=0, time=7)

    item = model.item(1, 0)
    actual = item.data(Role.COMMENT)

    assert actual == "Word 1"


def test_update_time_invalidates_search_results(model):
    model._searcher._hits = ["result"]

    model.update_time(row=0, time=7)

    assert model._searcher._hits is None


def test_update_time_fires_signals(model, signal_helper):
    model.timeUpdated.connect(lambda: signal_helper.log("timeUpdated"))

    model.update_time(row=0, time=7)

    assert signal_helper.has_logged("timeUpdated")


def test_update_comment_invalidates_search_results(model):
    model._searcher._hits = ["result"]

    model.update_comment(index=0, comment="new")

    assert model._searcher._hits is None

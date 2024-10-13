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


def test_remove_comment(model):
    assert model.rowCount() == 5
    model.remove_row(0)
    assert model.rowCount() == 4


def test_remove_comment_invalidates_search_results(model):
    model._searcher._hits = ["result"]

    model.remove_row(0)

    assert model._searcher._hits is None


def test_remove_comment_fires_signals(model, signal_helper):
    model.commentsChanged.connect(lambda: signal_helper.log("commentsChanged"))

    model.remove_row(0)

    assert signal_helper.has_logged("commentsChanged")

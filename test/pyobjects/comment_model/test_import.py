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

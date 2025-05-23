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

DEFAULT_COMMENTS = (
    Comment(time=0, comment_type="commentType", comment="Word 1"),
    Comment(time=5, comment_type="commentType", comment="Word 2"),
    Comment(time=10, comment_type="commentType", comment="Word 3"),
    Comment(time=15, comment_type="commentType", comment="Word 4"),
    Comment(time=20, comment_type="commentType", comment="Word 5"),
)


@pytest.fixture
def model(make_model):
    # noinspection PyArgumentList
    model, _ = make_model(
        set_comments=DEFAULT_COMMENTS,
        set_player_time=0,
    )
    return model


def test_update_time_sorts_model_again(model):
    model.update_time(row=0, new_time=7)
    assert model.item(0, 0).data(Role.COMMENT) == "Word 2"
    assert model.item(1, 0).data(Role.COMMENT) == "Word 1"

    model.undo()
    assert model.item(0, 0).data(Role.COMMENT) == "Word 1"
    assert model.item(1, 0).data(Role.COMMENT) == "Word 2"

    model.redo()
    assert model.item(0, 0).data(Role.COMMENT) == "Word 2"
    assert model.item(1, 0).data(Role.COMMENT) == "Word 1"


def test_update_time_invalidates_search_results(model):
    model._searcher._hits = ["result"]
    model.update_time(row=0, new_time=7)
    assert model._searcher._hits is None

    model._searcher._hits = ["result"]
    model.undo()
    assert model._searcher._hits is None

    model._searcher._hits = ["result"]
    model.redo()
    assert model._searcher._hits is None


def test_update_time_fires_signals(model, signal_helper):
    model.timeUpdatedInitially.connect(lambda idx: signal_helper.log("timeUpdatedInitially", idx))
    model.timeUpdatedUndone.connect(lambda idx: signal_helper.log("timeUpdatedUndone", idx))
    model.timeUpdatedRedone.connect(lambda idx: signal_helper.log("timeUpdatedRedone", idx))

    model.update_time(row=0, new_time=7)
    assert signal_helper.has_logged("timeUpdatedInitially")
    assert not signal_helper.has_logged("timeUpdatedUndone")
    assert not signal_helper.has_logged("timeUpdatedRedone")
    assert signal_helper.logged_value("timeUpdatedInitially") == 1

    signal_helper.reset()
    model.undo()

    assert not signal_helper.has_logged("timeUpdatedInitially")
    assert signal_helper.has_logged("timeUpdatedUndone")
    assert not signal_helper.has_logged("timeUpdatedRedone")

    signal_helper.reset()
    model.redo()

    assert not signal_helper.has_logged("timeUpdatedInitially")
    assert not signal_helper.has_logged("timeUpdatedUndone")
    assert signal_helper.has_logged("timeUpdatedRedone")
    assert signal_helper.logged_value("timeUpdatedRedone") == 1


def test_update_comment_type(model):
    model.update_comment_type(row=0, comment_type="updated comment type")
    assert model.item(0, 0).data(Role.TYPE) == "updated comment type"

    model.undo()
    assert model.item(0, 0).data(Role.TYPE) == "commentType"

    model.redo()
    assert model.item(0, 0).data(Role.TYPE) == "updated comment type"


def test_update_comment_type_fires_signals(model, signal_helper):
    model.commentTypeUpdated.connect(lambda idx: signal_helper.log("commentTypeUpdated", idx))
    model.commentTypeUpdatedUndone.connect(lambda idx: signal_helper.log("commentTypeUpdatedUndone", idx))

    model.update_comment_type(row=0, comment_type="updated comment type")
    assert signal_helper.has_logged("commentTypeUpdated")
    assert not signal_helper.has_logged("commentTypeUpdatedUndone")
    assert signal_helper.logged_value("commentTypeUpdated") == 0

    signal_helper.reset()
    model.undo()
    model.set_selected_row(3)

    assert not signal_helper.has_logged("commentTypeUpdated")
    assert signal_helper.has_logged("commentTypeUpdatedUndone")
    assert signal_helper.logged_value("commentTypeUpdatedUndone") == 0

    signal_helper.reset()
    model.redo()
    model.set_selected_row(2)

    assert signal_helper.has_logged("commentTypeUpdated")
    assert not signal_helper.has_logged("commentTypeUpdatedUndone")
    assert signal_helper.logged_value("commentTypeUpdated") == 0


def test_update_comment(model):
    model.update_comment(row=0, comment="new comment")
    assert model.item(0, 0).data(Role.COMMENT) == "new comment"

    model.undo()
    assert model.item(0, 0).data(Role.COMMENT) == "Word 1"

    model.redo()
    assert model.item(0, 0).data(Role.COMMENT) == "new comment"


def test_update_comment_invalidates_search_results(model):
    model._searcher._hits = ["result"]
    model.update_comment(row=0, comment="new")
    assert model._searcher._hits is None

    model._searcher._hits = ["result"]
    model.undo()
    assert model._searcher._hits is None

    model._searcher._hits = ["result"]
    model.redo()
    assert model._searcher._hits is None


def test_update_comment_fires_signals(model, signal_helper):
    model.commentUpdated.connect(lambda idx: signal_helper.log("commentUpdated", idx))
    model.commentUpdatedUndone.connect(lambda idx: signal_helper.log("commentUpdatedUndone", idx))

    model.update_comment(row=0, comment="new")
    assert signal_helper.has_logged("commentUpdated")
    assert not signal_helper.has_logged("commentUpdatedUndone")
    assert signal_helper.logged_value("commentUpdated") == 0

    signal_helper.reset()
    model.undo()
    model.set_selected_row(3)

    assert not signal_helper.has_logged("commentUpdated")
    assert signal_helper.has_logged("commentUpdatedUndone")
    assert signal_helper.logged_value("commentUpdatedUndone") == 0

    signal_helper.reset()
    model.redo()

    assert signal_helper.has_logged("commentUpdated")
    assert not signal_helper.has_logged("commentUpdatedUndone")
    assert signal_helper.logged_value("commentUpdated") == 0


def test_update_comments_consecutively_undo_redo(make_model):
    model, set_time = make_model(DEFAULT_COMMENTS, 999)
    model.add_row("comment-type")

    model.update_comment(row=5, comment="First")
    model.update_comment(row=5, comment="First - Second")
    model.undo()

    assert model.item(5, 0).data(Role.COMMENT) == "First"

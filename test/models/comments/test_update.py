# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import pytest

from mpvqc.datamodels import Comment
from mpvqc.models.comments.roles import Role

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


def test_update_time_invalidates_search_results(model, make_spy):
    spy = make_spy(model.searchInvalidated)

    model.update_time(row=0, new_time=7)
    assert spy.count() == 1

    model.undo()
    assert spy.count() == 2

    model.redo()
    assert spy.count() == 3


def test_update_time_fires_signals(model, make_spy):
    initially_spy = make_spy(model.timeUpdatedInitially)
    undone_spy = make_spy(model.timeUpdatedUndone)
    redone_spy = make_spy(model.timeUpdatedRedone)

    model.update_time(row=0, new_time=7)
    assert initially_spy.count() == 1
    assert undone_spy.count() == 0
    assert redone_spy.count() == 0
    assert initially_spy.at(invocation=0, argument=0) == 1

    initially_spy.reset()
    undone_spy.reset()
    redone_spy.reset()

    model.undo()

    assert initially_spy.count() == 0
    assert undone_spy.count() == 1
    assert redone_spy.count() == 0

    initially_spy.reset()
    undone_spy.reset()
    redone_spy.reset()

    model.redo()

    assert initially_spy.count() == 0
    assert undone_spy.count() == 0
    assert redone_spy.count() == 1
    assert redone_spy.at(invocation=0, argument=0) == 1


def test_update_comment_type(model):
    model.update_comment_type(row=0, comment_type="updated comment type")
    assert model.item(0, 0).data(Role.TYPE) == "updated comment type"

    model.undo()
    assert model.item(0, 0).data(Role.TYPE) == "commentType"

    model.redo()
    assert model.item(0, 0).data(Role.TYPE) == "updated comment type"


def test_update_comment_type_fires_signals(model, make_spy):
    updated_spy = make_spy(model.commentTypeUpdated)
    undone_spy = make_spy(model.commentTypeUpdatedUndone)

    model.update_comment_type(row=0, comment_type="updated comment type")
    assert updated_spy.count() == 1
    assert updated_spy.at(invocation=0, argument=0) == 0
    assert undone_spy.count() == 0

    updated_spy.reset()
    undone_spy.reset()

    model.undo()
    model.selectedRow = 3

    assert updated_spy.count() == 0
    assert undone_spy.count() == 1
    assert undone_spy.at(invocation=0, argument=0) == 0

    updated_spy.reset()
    undone_spy.reset()

    model.redo()
    model.selectedRow = 3

    assert updated_spy.count() == 1
    assert undone_spy.count() == 0
    assert updated_spy.at(invocation=0, argument=0) == 0


def test_update_comment(model):
    model.update_comment(row=0, comment="new comment")
    assert model.item(0, 0).data(Role.COMMENT) == "new comment"

    model.undo()
    assert model.item(0, 0).data(Role.COMMENT) == "Word 1"

    model.redo()
    assert model.item(0, 0).data(Role.COMMENT) == "new comment"


def test_update_comment_invalidates_search_results(model, make_spy):
    spy = make_spy(model.searchInvalidated)

    model.update_comment(row=0, comment="new")
    assert spy.count() == 1

    model.undo()
    assert spy.count() == 2

    model.redo()
    assert spy.count() == 3


def test_update_comment_fires_signals(model, make_spy):
    updated_spy = make_spy(model.commentUpdated)
    undone_spy = make_spy(model.commentUpdatedUndone)

    model.update_comment(row=0, comment="new")
    assert updated_spy.count() == 1
    assert updated_spy.at(invocation=0, argument=0) == 0
    assert undone_spy.count() == 0

    updated_spy.reset()
    undone_spy.reset()

    model.undo()
    model.selectedRow = 3

    assert updated_spy.count() == 0
    assert undone_spy.count() == 1
    assert undone_spy.at(invocation=0, argument=0) == 0

    updated_spy.reset()
    undone_spy.reset()

    model.redo()

    assert updated_spy.count() == 1
    assert undone_spy.count() == 0
    assert updated_spy.at(invocation=0, argument=0) == 0


def test_update_comments_consecutively_undo_redo(make_model):
    model, set_time = make_model(DEFAULT_COMMENTS, 999)
    model.add_row("comment-type")

    model.update_comment(row=5, comment="First")
    model.update_comment(row=5, comment="First - Second")
    model.undo()

    assert model.item(5, 0).data(Role.COMMENT) == "First"

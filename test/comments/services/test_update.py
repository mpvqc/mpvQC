# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import NamedTuple

import pytest

from mpvqc.comments.services import AnimatedSelection, QuickSelection, Role
from mpvqc.shared import Comment


def _data_at(store, row, role):
    return store.data(store.index(row), role)


def test_update_time_sorts_model_again(comments, store):
    comments.update_time(row=0, new_time=7)
    assert _data_at(store, 0, Role.COMMENT) == "Word 2"
    assert _data_at(store, 1, Role.COMMENT) == "Word 1"

    comments.undo()
    assert _data_at(store, 0, Role.COMMENT) == "Word 1"
    assert _data_at(store, 1, Role.COMMENT) == "Word 2"

    comments.redo()
    assert _data_at(store, 0, Role.COMMENT) == "Word 2"
    assert _data_at(store, 1, Role.COMMENT) == "Word 1"


def test_update_time_fires_signals(comments, make_spy):
    spy = make_spy(comments.view_action)

    comments.update_time(row=0, new_time=7)
    assert spy.count() == 1
    assert spy.at(invocation=0, argument=0) == AnimatedSelection(row=1)

    spy.reset()
    comments.undo()
    assert spy.count() == 1
    assert spy.at(invocation=0, argument=0) == AnimatedSelection(row=0)

    spy.reset()
    comments.redo()
    assert spy.count() == 1
    assert spy.at(invocation=0, argument=0) == AnimatedSelection(row=1)


class _RetimeCase(NamedTuple):
    name: str
    src_row: int
    new_time: int
    expected_dst_row: int
    expected_order: list[str]


_RETIME_CASES = [
    _RetimeCase(
        name="no reorder",
        src_row=1,
        new_time=4,
        expected_dst_row=1,
        expected_order=["Word 1", "Word 2", "Word 3", "Word 4", "Word 5"],
    ),
    _RetimeCase(
        name="same time",
        src_row=2,
        new_time=10,
        expected_dst_row=2,
        expected_order=["Word 1", "Word 2", "Word 3", "Word 4", "Word 5"],
    ),
    _RetimeCase(
        name="move to head",
        src_row=3,
        new_time=-5,
        expected_dst_row=0,
        expected_order=["Word 4", "Word 1", "Word 2", "Word 3", "Word 5"],
    ),
    _RetimeCase(
        name="move to tail",
        src_row=1,
        new_time=999,
        expected_dst_row=4,
        expected_order=["Word 1", "Word 3", "Word 4", "Word 5", "Word 2"],
    ),
]


@pytest.mark.parametrize("case", _RETIME_CASES, ids=lambda case: case.name)
def test_update_time_reorders(comments, store, make_spy, case: _RetimeCase):
    spy = make_spy(comments.view_action)

    comments.update_time(row=case.src_row, new_time=case.new_time)

    assert spy.at(invocation=0, argument=0) == AnimatedSelection(row=case.expected_dst_row)
    assert [_data_at(store, i, Role.COMMENT) for i in range(comments.count)] == case.expected_order


def test_update_time_into_tied_group_respects_seq_order(make_comments, store):
    comments = make_comments(
        set_comments=(
            Comment(time=0, comment_type="t", comment="A"),
            Comment(time=5, comment_type="t", comment="B"),
            Comment(time=5, comment_type="t", comment="C"),
            Comment(time=10, comment_type="t", comment="D"),
        ),
    )

    comments.update_time(row=3, new_time=0)

    assert [_data_at(store, i, Role.COMMENT) for i in range(4)] == ["A", "D", "B", "C"]


def test_update_comment_type(comments, store):
    comments.update_comment_type(row=0, comment_type="updated comment type")
    assert _data_at(store, 0, Role.TYPE) == "updated comment type"

    comments.undo()
    assert _data_at(store, 0, Role.TYPE) == "commentType"

    comments.redo()
    assert _data_at(store, 0, Role.TYPE) == "updated comment type"


def test_update_comment_type_fires_signals(comments, make_spy):
    spy = make_spy(comments.view_action)

    comments.update_comment_type(row=0, comment_type="updated comment type")
    assert spy.count() == 1
    assert spy.at(invocation=0, argument=0) == QuickSelection(row=0)

    spy.reset()
    comments.undo()
    assert spy.count() == 1
    assert spy.at(invocation=0, argument=0) == AnimatedSelection(row=0)

    spy.reset()
    comments.redo()
    assert spy.count() == 1
    assert spy.at(invocation=0, argument=0) == AnimatedSelection(row=0)


def test_update_comment(comments, store):
    comments.update_comment(row=0, comment="new comment")
    assert _data_at(store, 0, Role.COMMENT) == "new comment"

    comments.undo()
    assert _data_at(store, 0, Role.COMMENT) == "Word 1"

    comments.redo()
    assert _data_at(store, 0, Role.COMMENT) == "new comment"


def test_update_comment_fires_signals(comments, make_spy):
    spy = make_spy(comments.view_action)

    comments.update_comment(row=1, comment="new")
    assert spy.count() == 1
    assert spy.at(invocation=0, argument=0) == QuickSelection(row=1)

    spy.reset()
    comments.undo()
    assert spy.count() == 1
    assert spy.at(invocation=0, argument=0) == AnimatedSelection(row=1)

    spy.reset()
    comments.redo()
    assert spy.count() == 1
    assert spy.at(invocation=0, argument=0) == AnimatedSelection(row=1)


def test_update_comments_consecutively_undo_redo(comments, store):
    comments.add_row(999, "comment-type")

    comments.update_comment(row=5, comment="First")
    comments.update_comment(row=5, comment="First - Second")
    comments.undo()

    assert _data_at(store, 5, Role.COMMENT) == "First"

# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import NamedTuple

import pytest

from mpvqc.datamodels import Comment
from mpvqc.models.comments import AnimatedSelection, QuickSelection
from mpvqc.models.comments.roles import Role


def _data_at(comments, row, role):
    store = comments.store
    return store.data(store.index(row), role)


def test_update_time_sorts_model_again(comments):
    comments.update_time(row=0, new_time=7)
    assert _data_at(comments, 0, Role.COMMENT) == "Word 2"
    assert _data_at(comments, 1, Role.COMMENT) == "Word 1"

    comments.undo()
    assert _data_at(comments, 0, Role.COMMENT) == "Word 1"
    assert _data_at(comments, 1, Role.COMMENT) == "Word 2"

    comments.redo()
    assert _data_at(comments, 0, Role.COMMENT) == "Word 2"
    assert _data_at(comments, 1, Role.COMMENT) == "Word 1"


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
    src_row: int
    new_time: int
    expected_dst_row: int
    expected_order: list[str]


_RETIME_CASES = {
    "no_reorder": _RetimeCase(
        src_row=1,
        new_time=4,
        expected_dst_row=1,
        expected_order=["Word 1", "Word 2", "Word 3", "Word 4", "Word 5"],
    ),
    "same_time": _RetimeCase(
        src_row=2,
        new_time=10,
        expected_dst_row=2,
        expected_order=["Word 1", "Word 2", "Word 3", "Word 4", "Word 5"],
    ),
    "move_to_head": _RetimeCase(
        src_row=3,
        new_time=-5,
        expected_dst_row=0,
        expected_order=["Word 4", "Word 1", "Word 2", "Word 3", "Word 5"],
    ),
    "move_to_tail": _RetimeCase(
        src_row=1,
        new_time=999,
        expected_dst_row=4,
        expected_order=["Word 1", "Word 3", "Word 4", "Word 5", "Word 2"],
    ),
}


@pytest.mark.parametrize("case", _RETIME_CASES.values(), ids=_RETIME_CASES.keys())
def test_update_time_reorders(comments, make_spy, case: _RetimeCase):
    spy = make_spy(comments.view_action)

    comments.update_time(row=case.src_row, new_time=case.new_time)

    assert spy.at(invocation=0, argument=0) == AnimatedSelection(row=case.expected_dst_row)
    assert [_data_at(comments, i, Role.COMMENT) for i in range(comments.rowCount())] == case.expected_order


def test_update_time_into_tied_group_respects_seq_order(make_facade):
    comments = make_facade(
        set_comments=(
            Comment(time=0, comment_type="t", comment="A"),
            Comment(time=5, comment_type="t", comment="B"),
            Comment(time=5, comment_type="t", comment="C"),
            Comment(time=10, comment_type="t", comment="D"),
        ),
    )

    comments.update_time(row=3, new_time=0)

    assert [_data_at(comments, i, Role.COMMENT) for i in range(4)] == ["A", "D", "B", "C"]


def test_update_comment_type(comments):
    comments.update_comment_type(row=0, comment_type="updated comment type")
    assert _data_at(comments, 0, Role.TYPE) == "updated comment type"

    comments.undo()
    assert _data_at(comments, 0, Role.TYPE) == "commentType"

    comments.redo()
    assert _data_at(comments, 0, Role.TYPE) == "updated comment type"


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


def test_update_comment_type_does_not_invalidate_search(comments, monkeypatch):
    comments.search("Word", include_current_row=True, top_down=True)

    def fail(*_args, **_kwargs):
        pytest.fail("UpdateType must not trigger a fresh scan")

    monkeypatch.setattr(comments.store, "find_rows_containing", fail)
    comments.update_comment_type(row=0, comment_type="other")

    after = comments.search("Word", include_current_row=True, top_down=True)
    assert after.total == 5


def test_update_comment(comments):
    comments.update_comment(row=0, comment="new comment")
    assert _data_at(comments, 0, Role.COMMENT) == "new comment"

    comments.undo()
    assert _data_at(comments, 0, Role.COMMENT) == "Word 1"

    comments.redo()
    assert _data_at(comments, 0, Role.COMMENT) == "new comment"


def test_update_comment_invalidates_search(comments):
    initial = comments.search("Word", include_current_row=True, top_down=True)
    assert initial.total == 5

    comments.update_comment(row=0, comment="other")

    after = comments.search("Word", include_current_row=True, top_down=True)
    assert after.total == 4


def test_update_time_invalidates_search(make_facade):
    comments = make_facade(
        set_comments=(
            Comment(time=0, comment_type="commentType", comment="Word 1"),
            Comment(time=5, comment_type="commentType", comment="Other"),
            Comment(time=10, comment_type="commentType", comment="Word 2"),
        ),
    )

    initial = comments.search("Word", include_current_row=True, top_down=True)
    assert initial.index == 0

    # Move "Word 1" past "Other"; first match now lives at row 1.
    comments.update_time(row=0, new_time=7)

    after = comments.search("Word", include_current_row=True, top_down=True)
    assert after.index == 1


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


def test_update_comments_consecutively_undo_redo(comments):
    comments.add_row(999, "comment-type")

    comments.update_comment(row=5, comment="First")
    comments.update_comment(row=5, comment="First - Second")
    comments.undo()

    assert _data_at(comments, 5, Role.COMMENT) == "First"

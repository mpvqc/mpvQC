# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Any

from mpvqc.models import Comment


def assert_comments(expected: list[list[Any]], actual: list[dict[str, Any]]):
    assert len(expected) == len(actual)
    for c_e, c_a in zip(expected, actual):
        print(f"{c_e[0]} == {c_a['time']}, ", end="")
        print(f"{c_e[1]} == {c_a['commentType']}, ", end="")
        print(f"{c_e[2]} == {c_a['comment']}")
        assert c_e[0] == c_a["time"]
        assert c_e[1] == c_a["commentType"]
        assert c_e[2] == c_a["comment"]
    print("---")


def test_undo_redo_combination(make_model):
    # noinspection PyArgumentList
    model, set_time = make_model(set_comments=[], set_player_time=0)
    model.import_comments(
        [
            Comment(time=10, comment_type="type 1", comment="Word 1"),
            Comment(time=20, comment_type="type 2", comment="Word 2"),
            Comment(time=30, comment_type="type 3", comment="Word 3"),
            Comment(time=40, comment_type="type 4", comment="Word 4"),
            Comment(time=50, comment_type="type 5", comment="Word 5"),
        ]
    )

    assert_comments(
        actual=model.comments(),
        expected=[
            [10, "type 1", "Word 1"],
            [20, "type 2", "Word 2"],
            [30, "type 3", "Word 3"],
            [40, "type 4", "Word 4"],
            [50, "type 5", "Word 5"],
        ],
    )

    set_time(25)
    model.add_row("added 1")
    assert_comments(
        actual=model.comments(),
        expected=[
            [10, "type 1", "Word 1"],
            [20, "type 2", "Word 2"],
            [25, "added 1", ""],
            [30, "type 3", "Word 3"],
            [40, "type 4", "Word 4"],
            [50, "type 5", "Word 5"],
        ],
    )

    model.update_comment(2, "Word Edited 1")
    assert_comments(
        actual=model.comments(),
        expected=[
            [10, "type 1", "Word 1"],
            [20, "type 2", "Word 2"],
            [25, "added 1", "Word Edited 1"],
            [30, "type 3", "Word 3"],
            [40, "type 4", "Word 4"],
            [50, "type 5", "Word 5"],
        ],
    )

    model.update_time(2, 35)
    assert_comments(
        actual=model.comments(),
        expected=[
            [10, "type 1", "Word 1"],
            [20, "type 2", "Word 2"],
            [30, "type 3", "Word 3"],
            [35, "added 1", "Word Edited 1"],
            [40, "type 4", "Word 4"],
            [50, "type 5", "Word 5"],
        ],
    )

    model.update_comment_type(3, "edited")
    assert_comments(
        actual=model.comments(),
        expected=[
            [10, "type 1", "Word 1"],
            [20, "type 2", "Word 2"],
            [30, "type 3", "Word 3"],
            [35, "edited", "Word Edited 1"],
            [40, "type 4", "Word 4"],
            [50, "type 5", "Word 5"],
        ],
    )

    model.undo()
    model.undo()
    model.undo()
    assert_comments(
        actual=model.comments(),
        expected=[
            [10, "type 1", "Word 1"],
            [20, "type 2", "Word 2"],
            [30, "type 3", "Word 3"],
            [40, "type 4", "Word 4"],
            [50, "type 5", "Word 5"],
        ],
    )

    model.redo()
    model.redo()
    assert_comments(
        actual=model.comments(),
        expected=[
            [10, "type 1", "Word 1"],
            [20, "type 2", "Word 2"],
            [30, "type 3", "Word 3"],
            [35, "added 1", "Word Edited 1"],
            [40, "type 4", "Word 4"],
            [50, "type 5", "Word 5"],
        ],
    )

    model.update_comment_type(3, "edited 2")
    assert_comments(
        actual=model.comments(),
        expected=[
            [10, "type 1", "Word 1"],
            [20, "type 2", "Word 2"],
            [30, "type 3", "Word 3"],
            [35, "edited 2", "Word Edited 1"],
            [40, "type 4", "Word 4"],
            [50, "type 5", "Word 5"],
        ],
    )

    model.clear_comments()
    assert_comments(
        actual=model.comments(),
        expected=[],
    )

    model.undo()
    assert_comments(
        actual=model.comments(),
        expected=[
            [10, "type 1", "Word 1"],
            [20, "type 2", "Word 2"],
            [30, "type 3", "Word 3"],
            [35, "edited 2", "Word Edited 1"],
            [40, "type 4", "Word 4"],
            [50, "type 5", "Word 5"],
        ],
    )

    model.update_comment(3, "Word Edited 2")
    assert_comments(
        actual=model.comments(),
        expected=[
            [10, "type 1", "Word 1"],
            [20, "type 2", "Word 2"],
            [30, "type 3", "Word 3"],
            [35, "edited 2", "Word Edited 2"],
            [40, "type 4", "Word 4"],
            [50, "type 5", "Word 5"],
        ],
    )

    set_time(55)
    model.add_row("added 2")
    assert_comments(
        actual=model.comments(),
        expected=[
            [10, "type 1", "Word 1"],
            [20, "type 2", "Word 2"],
            [30, "type 3", "Word 3"],
            [35, "edited 2", "Word Edited 2"],
            [40, "type 4", "Word 4"],
            [50, "type 5", "Word 5"],
            [55, "added 2", ""],
        ],
    )

    model.undo()
    model.redo()

    assert_comments(
        actual=model.comments(),
        expected=[
            [10, "type 1", "Word 1"],
            [20, "type 2", "Word 2"],
            [30, "type 3", "Word 3"],
            [35, "edited 2", "Word Edited 2"],
            [40, "type 4", "Word 4"],
            [50, "type 5", "Word 5"],
            [55, "added 2", ""],
        ],
    )

    for _ in range(50):
        model.undo()

    assert_comments(
        actual=model.comments(),
        expected=[],
    )

    for _ in range(50):
        model.redo()

    assert_comments(
        actual=model.comments(),
        expected=[
            [10, "type 1", "Word 1"],
            [20, "type 2", "Word 2"],
            [30, "type 3", "Word 3"],
            [35, "edited 2", "Word Edited 2"],
            [40, "type 4", "Word 4"],
            [50, "type 5", "Word 5"],
            [55, "added 2", ""],
        ],
    )


def test_merge_add_and_update(make_model):
    # noinspection PyArgumentList
    model, _ = make_model(set_comments=[], set_player_time=25)
    model.import_comments(
        [
            Comment(time=10, comment_type="type 1", comment="Word 1"),
        ]
    )

    assert_comments(
        actual=model.comments(),
        expected=[
            [10, "type 1", "Word 1"],
        ],
    )

    model.add_row("added 1")
    assert_comments(
        actual=model.comments(),
        expected=[
            [10, "type 1", "Word 1"],
            [25, "added 1", ""],
        ],
    )

    model.update_comment(1, "Word Added 1")
    assert_comments(
        actual=model.comments(),
        expected=[
            [10, "type 1", "Word 1"],
            [25, "added 1", "Word Added 1"],
        ],
    )

    model.undo()
    assert_comments(
        actual=model.comments(),
        expected=[
            [10, "type 1", "Word 1"],
        ],
    )

    model.redo()
    assert_comments(
        actual=model.comments(),
        expected=[
            [10, "type 1", "Word 1"],
            [25, "added 1", "Word Added 1"],
        ],
    )


def test_merge_add_and_update_declined_because_of_other_command(make_model):
    # noinspection PyArgumentList
    model, _ = make_model(set_comments=[], set_player_time=25)
    model.import_comments(
        [
            Comment(time=10, comment_type="type 1", comment="Word 1"),
        ]
    )

    assert_comments(
        actual=model.comments(),
        expected=[
            [10, "type 1", "Word 1"],
        ],
    )

    model.add_row("added 1")
    assert_comments(
        actual=model.comments(),
        expected=[
            [10, "type 1", "Word 1"],
            [25, "added 1", ""],
        ],
    )

    model.update_time(1, new_time=24)
    model.update_comment(1, "Word Added 1")
    assert_comments(
        actual=model.comments(),
        expected=[
            [10, "type 1", "Word 1"],
            [24, "added 1", "Word Added 1"],
        ],
    )

    model.undo()
    assert_comments(
        actual=model.comments(),
        expected=[
            [10, "type 1", "Word 1"],
            [24, "added 1", ""],
        ],
    )

    model.undo()
    assert_comments(
        actual=model.comments(),
        expected=[
            [10, "type 1", "Word 1"],
            [25, "added 1", ""],
        ],
    )

    model.redo()
    assert_comments(
        actual=model.comments(),
        expected=[
            [10, "type 1", "Word 1"],
            [24, "added 1", ""],
        ],
    )

    model.redo()
    assert_comments(
        actual=model.comments(),
        expected=[
            [10, "type 1", "Word 1"],
            [24, "added 1", "Word Added 1"],
        ],
    )


def test_merge_add_and_update_declined_on_selection_of_other_comment(make_model):
    # noinspection PyArgumentList
    model, _ = make_model(set_comments=[], set_player_time=25)
    model.import_comments(
        [
            Comment(time=10, comment_type="type 1", comment="Word 1"),
        ]
    )

    assert_comments(
        actual=model.comments(),
        expected=[
            [10, "type 1", "Word 1"],
        ],
    )

    model.add_row("added 1")
    assert_comments(
        actual=model.comments(),
        expected=[
            [10, "type 1", "Word 1"],
            [25, "added 1", ""],
        ],
    )

    model.set_selected_row(0)
    model.update_comment(1, "Word Added 1")
    assert_comments(
        actual=model.comments(),
        expected=[
            [10, "type 1", "Word 1"],
            [25, "added 1", "Word Added 1"],
        ],
    )

    model.undo()
    assert_comments(
        actual=model.comments(),
        expected=[
            [10, "type 1", "Word 1"],
            [25, "added 1", ""],
        ],
    )

    model.undo()
    assert_comments(
        actual=model.comments(),
        expected=[
            [10, "type 1", "Word 1"],
        ],
    )

    model.redo()
    assert_comments(
        actual=model.comments(),
        expected=[
            [10, "type 1", "Word 1"],
            [25, "added 1", ""],
        ],
    )

    model.redo()
    assert_comments(
        actual=model.comments(),
        expected=[
            [10, "type 1", "Word 1"],
            [25, "added 1", "Word Added 1"],
        ],
    )

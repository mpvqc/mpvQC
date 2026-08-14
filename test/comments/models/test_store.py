# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from typing import NamedTuple

import pytest
from PySide6.QtTest import QAbstractItemModelTester

from mpvqc.comments.models import CommentStore
from mpvqc.comments.services import Role
from mpvqc.shared import Comment


def _comment(label: str, time: int = 0) -> Comment:
    return Comment(time=time, comment_type="commentType", comment=label)


def _seed(store: CommentStore, labels: list[str]) -> None:
    for row, label in enumerate(labels):
        store.insert(row, store.mint(_comment(label, time=row)))


def _comments_in(store: CommentStore) -> list[str]:
    return [c.comment for c in store.comments()]


@pytest.fixture
def store() -> CommentStore:
    return CommentStore()


def test_insert_emits_the_custom_signal_before_qts_begin_signal(store):
    _seed(store, ["A", "B"])
    events: list[tuple[str, int]] = []
    store.aboutToInsertRow.connect(lambda row: events.append(("custom", row)))
    store.rowsAboutToBeInserted.connect(lambda _parent, first, _last: events.append(("qt", first)))

    store.insert(1, store.mint(_comment("C")))

    assert events == [("custom", 1), ("qt", 1)]


def test_remove_emits_the_custom_signal_before_qts_begin_signal(store):
    _seed(store, ["A", "B", "C"])
    events: list[tuple[str, int]] = []
    store.aboutToRemoveRow.connect(lambda row: events.append(("custom", row)))
    store.rowsAboutToBeRemoved.connect(lambda _parent, first, _last: events.append(("qt", first)))

    store.remove(2)

    assert events == [("custom", 2), ("qt", 2)]


@pytest.mark.parametrize("role", list(Role), ids=lambda role: role.name)
def test_replace_data_changed_carries_exactly_the_mutated_role(store, make_spy, role):
    _seed(store, ["A", "B", "C"])
    data_changed_spy = make_spy(store.dataChanged)
    insert_spy = make_spy(store.aboutToInsertRow)
    remove_spy = make_spy(store.aboutToRemoveRow)

    store.replace(1, _comment("B2"), role)

    assert data_changed_spy.count() == 1
    assert data_changed_spy.at(0, 0).row() == 1
    assert data_changed_spy.at(0, 1).row() == 1
    assert data_changed_spy.at(0, 2) == [role]
    assert insert_spy.count() == 0
    assert remove_spy.count() == 0
    assert _comments_in(store) == ["A", "B2", "C"]


def test_move_replace_when_source_equals_destination_only_changes_data(store, make_spy):
    _seed(store, ["C0", "C1", "C2"])
    moved_spy = make_spy(store.rowsMoved)
    data_changed_spy = make_spy(store.dataChanged)
    insert_spy = make_spy(store.aboutToInsertRow)
    remove_spy = make_spy(store.aboutToRemoveRow)

    store.move_replace(1, 1, _comment("NEW"), Role.TYPE)

    assert moved_spy.count() == 0
    assert insert_spy.count() == 0
    assert remove_spy.count() == 0
    assert data_changed_spy.count() == 1
    assert data_changed_spy.at(0, 0).row() == 1
    assert data_changed_spy.at(0, 1).row() == 1
    assert data_changed_spy.at(0, 2) == [Role.TYPE]
    assert _comments_in(store) == ["C0", "NEW", "C2"]


class _MoveReplaceCase(NamedTuple):
    name: str
    src: int
    dst: int
    destination_child: int
    order: list[str]


_MOVE_REPLACE_CASES = [
    _MoveReplaceCase(
        name="up",
        src=3,
        dst=0,
        destination_child=0,
        order=["NEW", "C0", "C1", "C2", "C4"],
    ),
    _MoveReplaceCase(
        name="down",
        src=1,
        dst=4,
        destination_child=5,
        order=["C0", "C2", "C3", "C4", "NEW"],
    ),
    _MoveReplaceCase(
        name="adjacent up",
        src=2,
        dst=1,
        destination_child=1,
        order=["C0", "NEW", "C1", "C3", "C4"],
    ),
    _MoveReplaceCase(
        name="adjacent down",
        src=1,
        dst=2,
        destination_child=3,
        order=["C0", "C2", "NEW", "C3", "C4"],
    ),
]


@pytest.mark.parametrize("case", _MOVE_REPLACE_CASES, ids=lambda case: case.name)
def test_move_replace_moves_across_rows(store, make_spy, case: _MoveReplaceCase):
    _seed(store, ["C0", "C1", "C2", "C3", "C4"])
    moved_spy = make_spy(store.rowsMoved)
    data_changed_spy = make_spy(store.dataChanged)
    insert_spy = make_spy(store.aboutToInsertRow)
    remove_spy = make_spy(store.aboutToRemoveRow)

    store.move_replace(case.src, case.dst, _comment("NEW"), Role.COMMENT)

    assert moved_spy.count() == 1
    assert not moved_spy.at(0, 0).isValid()
    assert moved_spy.at(0, 1) == case.src
    assert moved_spy.at(0, 2) == case.src
    assert not moved_spy.at(0, 3).isValid()
    assert moved_spy.at(0, 4) == case.destination_child

    assert data_changed_spy.count() == 1
    assert data_changed_spy.at(0, 0).row() == case.dst
    assert data_changed_spy.at(0, 1).row() == case.dst
    assert data_changed_spy.at(0, 2) == [Role.COMMENT]

    assert insert_spy.count() == 0
    assert remove_spy.count() == 0
    assert _comments_in(store) == case.order


def test_reset_emits_a_single_model_reset_with_no_per_row_signals(store, make_spy):
    _seed(store, ["A", "B", "C"])
    about_to_reset_spy = make_spy(store.modelAboutToBeReset)
    reset_spy = make_spy(store.modelReset)
    inserted_spy = make_spy(store.rowsInserted)
    removed_spy = make_spy(store.rowsRemoved)
    data_changed_spy = make_spy(store.dataChanged)
    insert_spy = make_spy(store.aboutToInsertRow)
    remove_spy = make_spy(store.aboutToRemoveRow)

    store.reset([store.mint(_comment("X")), store.mint(_comment("Y"))])

    assert about_to_reset_spy.count() == 1
    assert reset_spy.count() == 1
    assert inserted_spy.count() == 0
    assert removed_spy.count() == 0
    assert data_changed_spy.count() == 0
    assert insert_spy.count() == 0
    assert remove_spy.count() == 0
    assert _comments_in(store) == ["X", "Y"]


def test_mutation_sequence_satisfies_the_item_model_protocol(store):
    QAbstractItemModelTester(store, QAbstractItemModelTester.FailureReportingMode.Fatal, store)

    store.insert(0, store.mint(_comment("A", time=0)))
    store.insert(1, store.mint(_comment("B", time=5)))
    store.insert(0, store.mint(_comment("C", time=-5)))
    store.replace(1, _comment("A2", time=0), Role.COMMENT)
    store.move_replace(0, 2, _comment("C2", time=99), Role.COMMENT)
    store.move_replace(1, 1, _comment("B2", time=5), Role.TYPE)
    store.remove(0)
    store.reset([store.mint(_comment("Z"))])
    store.remove(0)

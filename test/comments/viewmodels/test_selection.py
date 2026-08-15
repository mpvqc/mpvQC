# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import pytest

from mpvqc.comments.services import SelectionCell
from mpvqc.comments.viewmodels import MpvqcCommentSelectionViewModel


@pytest.fixture
def cell() -> SelectionCell:
    return SelectionCell()


@pytest.fixture
def announced(cell) -> list[int]:
    rows: list[int] = []
    cell.row_selected.connect(rows.append)
    return rows


@pytest.fixture
def view_model(cell) -> MpvqcCommentSelectionViewModel:
    return MpvqcCommentSelectionViewModel(cell)


def test_row_write_takes_the_user_path(view_model, cell, announced):
    view_model.setProperty("selectedRow", 3)

    assert cell.row == 3
    assert announced == [3]


def test_visibility_write_stays_silent(view_model, cell, announced):
    view_model.setProperty("selectedRowVisible", False)

    assert not cell.row_visible
    assert announced == []


def test_reads_answer_from_the_cell(view_model, cell):
    cell.set_row(7)
    cell.set_row_visible(False)

    assert view_model.selectedRow == 7
    assert view_model.selectedRowVisible is False

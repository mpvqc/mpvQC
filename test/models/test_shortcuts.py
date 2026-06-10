# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from itertools import groupby
from typing import NamedTuple

import pytest

from mpvqc.models.shortcuts import MpvqcShortcutsModel, MpvqcShortcutsModelBackend


def _labels(model: MpvqcShortcutsModel) -> list[str]:
    return [model.data(model.index(row, 0), MpvqcShortcutsModelBackend.LabelRole) for row in range(model.rowCount())]


class FilterCase(NamedTuple):
    name: str
    query: str
    expected: list[str]


FILTER_CASES = (
    FilterCase(
        name="label match is case insensitive",
        query="FULLscreen",
        expected=["Toggle Fullscreen"],
    ),
    FilterCase(
        name="category match includes all rows of the category",
        query="comments",
        expected=[
            "Edit Comment",
            "Copy Comment to Clipboard",
            "Delete Comment",
            "Previous Comment",
            "Next Comment",
        ],
    ),
    FilterCase(
        name="chord match joins keys with plus",
        query="ctrl+n",
        expected=["New QC Document"],
    ),
    FilterCase(
        name="chord match works on chord suffix",
        query="shift+z",
        expected=["Redo Previous Action"],
    ),
    FilterCase(
        name="chord match works with three keys",
        query="ctrl+alt+o",
        expected=["Open Video"],
    ),
    FilterCase(
        name="alternative sequences match individually",
        query="delete",
        expected=["Delete Comment"],
    ),
    FilterCase(
        name="icon keys are not searchable by their token",
        query="backspace",
        expected=[],
    ),
    FilterCase(
        name="surrounding whitespace is ignored",
        query="  ctrl+n  ",
        expected=["New QC Document"],
    ),
    FilterCase(
        name="no match yields empty model",
        query="does not exist",
        expected=[],
    ),
)


@pytest.mark.parametrize("case", FILTER_CASES, ids=lambda case: case.name)
def test_filter(qt_app, case: FilterCase) -> None:
    model = MpvqcShortcutsModel()
    # pyrefly: ignore [bad-assignment]
    model.query = case.query
    assert _labels(model) == case.expected


@pytest.mark.parametrize("query", ["", "   "], ids=["empty", "blank"])
def test_empty_query_shows_all_shortcuts(qt_app, query: str) -> None:
    model = MpvqcShortcutsModel()
    # pyrefly: ignore [bad-assignment]
    model.query = query
    assert model.rowCount() == 38


def test_sequences_role_exposes_text_and_icon_keys(qt_app) -> None:
    model = MpvqcShortcutsModel()
    # pyrefly: ignore [bad-assignment]
    model.query = "delete comment"
    sequences = model.data(model.index(0, 0), MpvqcShortcutsModelBackend.SequencesRole)
    assert sequences == [[{"icon": "backspace"}], [{"text": "Delete"}]]


def test_categories_form_contiguous_blocks(qt_app) -> None:
    model = MpvqcShortcutsModel()
    categories = [
        model.data(model.index(row, 0), MpvqcShortcutsModelBackend.CategoryRole) for row in range(model.rowCount())
    ]
    blocks = [category for category, _ in groupby(categories)]
    assert len(blocks) == len(set(blocks)), "non-contiguous category would render a duplicate section header"


def test_note_role_set_only_for_subtitle_seeking(qt_app) -> None:
    model = MpvqcShortcutsModel()
    # pyrefly: ignore [bad-assignment]
    model.query = "seek to previous subtitle"
    assert "embedded subtitle tracks" in model.data(model.index(0, 0), MpvqcShortcutsModelBackend.NoteRole)

    # pyrefly: ignore [bad-assignment]
    model.query = "toggle mute"
    assert not model.data(model.index(0, 0), MpvqcShortcutsModelBackend.NoteRole)

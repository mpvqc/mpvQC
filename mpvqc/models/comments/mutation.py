# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from dataclasses import dataclass


@dataclass(frozen=True)
class QuickSelection:
    """Jump to row without animation."""

    row: int
    marks_unsaved: bool = True


@dataclass(frozen=True)
class AnimatedSelection:
    """Jump to row with animation."""

    row: int
    marks_unsaved: bool = True


@dataclass(frozen=True)
class RowAddEdit:
    """Jump to row without animation and open the comment editor for a newly added row."""

    row: int
    marks_unsaved: bool = True


@dataclass(frozen=True)
class LastRowSelection:
    """Jump to the last row without animation."""

    row: int
    marks_unsaved: bool = True


@dataclass(frozen=True)
class NoViewAction:
    """No view navigation."""

    marks_unsaved: bool


type ModelMutation = QuickSelection | AnimatedSelection | RowAddEdit | LastRowSelection | NoViewAction

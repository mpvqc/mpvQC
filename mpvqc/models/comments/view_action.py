# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class AnimatedSelection:
    """Jump to row with animation."""

    row: int


@dataclass(frozen=True)
class QuickSelection:
    """Jump to row without animation."""

    row: int


@dataclass(frozen=True)
class QuickSelectionAndEdit:
    """Jump to row without animation and open the comment editor."""

    row: int


@dataclass(frozen=True)
class NoViewAction:
    """No extra instruction. Qt's model/view signals handle the update."""


type ViewAction = AnimatedSelection | QuickSelection | QuickSelectionAndEdit | NoViewAction

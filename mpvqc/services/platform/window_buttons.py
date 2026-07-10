# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, ClassVar, Protocol

from PySide6.QtCore import QObject, Signal

if TYPE_CHECKING:
    from typing import Final


@dataclass(frozen=True)
class WindowButtonPreference:
    minimize: bool
    maximize: bool
    close: bool


DEFAULT_WINDOW_BUTTON_PREFERENCE: Final = WindowButtonPreference(minimize=True, maximize=True, close=True)


class WindowButtonSource(Protocol):
    preference_changed: ClassVar[Signal]

    @property
    def preference(self) -> WindowButtonPreference: ...


class StaticWindowButtons(QObject):
    """For platforms without a detectable window button preference."""

    preference_changed = Signal(WindowButtonPreference)

    @property
    def preference(self) -> WindowButtonPreference:
        return DEFAULT_WINDOW_BUTTON_PREFERENCE

# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from collections.abc import Callable
    from typing import Final


@dataclass(frozen=True)
class WindowButtonPreference:
    minimize: bool
    maximize: bool
    close: bool


DEFAULT_WINDOW_BUTTON_PREFERENCE: Final = WindowButtonPreference(minimize=True, maximize=True, close=True)


class WindowButtonSource(Protocol):
    @property
    def preference(self) -> WindowButtonPreference: ...

    def on_preference_changed(self, callback: Callable[[WindowButtonPreference], None]) -> None: ...


class StaticWindowButtons:
    """For platforms without a detectable window button preference."""

    @property
    def preference(self) -> WindowButtonPreference:
        return DEFAULT_WINDOW_BUTTON_PREFERENCE

    def on_preference_changed(self, callback: Callable[[WindowButtonPreference], None]) -> None:
        """The preference never changes here."""

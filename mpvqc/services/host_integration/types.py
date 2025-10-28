# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True)
class WindowButtonPreference:
    minimize: bool
    maximize: bool
    close: bool


DEFAULT_WINDOW_BUTTON_PREFERENCE = WindowButtonPreference(
    minimize=True,
    maximize=True,
    close=True,
)


class OsBackend(ABC):
    @abstractmethod
    def get_display_zoom_factor(self) -> float:
        pass

    @abstractmethod
    def get_window_button_preference(self) -> WindowButtonPreference:
        pass

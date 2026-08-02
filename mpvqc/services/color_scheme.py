# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from typing import TYPE_CHECKING, Protocol, assert_never

import inject
from PySide6.QtCore import QObject, Qt, Signal, Slot

from mpvqc.appearance import Dark, FollowSystem, Light, Unknown, resolve_color_scheme

from .settings import SettingsService

if TYPE_CHECKING:
    from collections.abc import Callable

    from PySide6.QtGui import QStyleHints

    from mpvqc.appearance import ColorScheme, ColorSchemePreference, SystemColorScheme


class StyleHints(Protocol):
    """The color scheme slice of the application's style hints."""

    @property
    def color_scheme(self) -> SystemColorScheme: ...

    def set_color_scheme(self, color_scheme: ColorScheme) -> None: ...

    def unset_color_scheme(self) -> None: ...

    def on_color_scheme_changed(self, callback: Callable[[], None]) -> None: ...


class QtStyleHints:
    """Reads the system's color scheme from Qt and pushes explicit preferences back into it.

    The only place Qt's color scheme enum meets the domain's."""

    def __init__(self, style_hints: QStyleHints) -> None:
        self._style_hints = style_hints

    @property
    def color_scheme(self) -> SystemColorScheme:
        scheme = self._style_hints.colorScheme()
        match scheme:
            case Qt.ColorScheme.Light:
                return Light()
            case Qt.ColorScheme.Dark:
                return Dark()
            case Qt.ColorScheme.Unknown:
                return Unknown()

    def set_color_scheme(self, color_scheme: ColorScheme) -> None:
        match color_scheme:
            case Light():
                self._style_hints.setColorScheme(Qt.ColorScheme.Light)
            case Dark():
                self._style_hints.setColorScheme(Qt.ColorScheme.Dark)
            case _:
                assert_never(color_scheme)

    def unset_color_scheme(self) -> None:
        self._style_hints.unsetColorScheme()

    def on_color_scheme_changed(self, callback: Callable[[], None]) -> None:
        self._style_hints.colorSchemeChanged.connect(callback)


class ColorSchemeService(QObject):
    _settings = inject.attr(SettingsService)

    color_scheme_changed = Signal(object)  # ColorScheme union; Qt sigs can't carry type aliases

    def __init__(self, style_hints: StyleHints, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self._style_hints = style_hints
        self._preference = self._settings.color_scheme_preference
        self._push_preference()
        self._color_scheme = self._resolve()
        style_hints.on_color_scheme_changed(self._on_system_color_scheme_changed)
        self._settings.color_scheme_preference_changed.connect(self._on_preference_changed)

    @property
    def color_scheme(self) -> ColorScheme:
        return self._color_scheme

    def _resolve(self) -> ColorScheme:
        return resolve_color_scheme(self._preference, self._style_hints.color_scheme)

    def _push_preference(self) -> None:
        # An explicit scheme also makes Qt ignore the system from here on
        preference = self._preference
        match preference:
            case FollowSystem():
                self._style_hints.unset_color_scheme()
            case Light() | Dark():
                self._style_hints.set_color_scheme(preference)
            case _:
                assert_never(preference)

    @Slot(object)
    def _on_preference_changed(self, preference: ColorSchemePreference) -> None:
        self._preference = preference
        self._push_preference()
        self._publish()

    def _on_system_color_scheme_changed(self) -> None:
        self._publish()

    def _publish(self) -> None:
        color_scheme = self._resolve()
        if color_scheme == self._color_scheme:
            return
        self._color_scheme = color_scheme
        self.color_scheme_changed.emit(color_scheme)

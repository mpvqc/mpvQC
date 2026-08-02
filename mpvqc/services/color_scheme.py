# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from typing import TYPE_CHECKING, Protocol

import inject
from PySide6.QtCore import QObject, Qt, Signal, Slot

from mpvqc.appearance import ColorSchemePreference, resolve_color_scheme

from .settings import SettingsService

if TYPE_CHECKING:
    from collections.abc import Callable

    from PySide6.QtGui import QStyleHints

    from mpvqc.appearance import ColorScheme


class StyleHints(Protocol):
    """The color scheme slice of the application's style hints."""

    @property
    def color_scheme(self) -> Qt.ColorScheme: ...

    def set_color_scheme(self, color_scheme: Qt.ColorScheme) -> None: ...

    def unset_color_scheme(self) -> None: ...

    def on_color_scheme_changed(self, callback: Callable[[], None]) -> None: ...


class QtStyleHints:
    """Reads the system's color scheme from Qt and pushes explicit preferences back into it."""

    def __init__(self, style_hints: QStyleHints) -> None:
        self._style_hints = style_hints

    @property
    def color_scheme(self) -> Qt.ColorScheme:
        return self._style_hints.colorScheme()

    def set_color_scheme(self, color_scheme: Qt.ColorScheme) -> None:
        self._style_hints.setColorScheme(color_scheme)

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
        if self._preference is ColorSchemePreference.LIGHT:
            self._style_hints.set_color_scheme(Qt.ColorScheme.Light)
        elif self._preference is ColorSchemePreference.DARK:
            self._style_hints.set_color_scheme(Qt.ColorScheme.Dark)
        else:
            self._style_hints.unset_color_scheme()

    @Slot(ColorSchemePreference)
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

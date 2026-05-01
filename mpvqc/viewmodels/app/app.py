# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import inject
from PySide6.QtCore import Property, QObject, Qt, Signal, Slot
from PySide6.QtQml import QmlElement

from mpvqc.services import (
    HostIntegrationService,
    KeyCommandGeneratorService,
    PlayerService,
    SettingsService,
    WindowPropertiesService,
)

QML_IMPORT_NAME = "pyobjects"
QML_IMPORT_MAJOR_VERSION = 1


# noinspection PyPep8Naming,PyTypeChecker
@QmlElement
class MpvqcAppViewModel(QObject):
    _host_integration = inject.attr(HostIntegrationService)
    _window_properties = inject.attr(WindowPropertiesService)
    _settings = inject.attr(SettingsService)
    _player = inject.attr(PlayerService)
    _command_generator = inject.attr(KeyCommandGeneratorService)

    windowBorderChanged = Signal(int)
    layoutOrientationChanged = Signal(int)

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self._window_border = self._compute_window_border()
        self._window_properties.is_fullscreen_changed.connect(lambda _: self._update_window_border())
        self._window_properties.is_maximized_changed.connect(lambda _: self._update_window_border())
        self._settings.layoutOrientationChanged.connect(self.layoutOrientationChanged)

    def _compute_window_border(self) -> int:
        if self._host_integration.is_tiling_window_manager:
            return 0
        if self._window_properties.is_fullscreen or self._window_properties.is_maximized:
            return 0
        return 1

    def _update_window_border(self) -> None:
        new_value = self._compute_window_border()
        if new_value != self._window_border:
            self._window_border = new_value
            self.windowBorderChanged.emit(new_value)

    @Property(int, notify=windowBorderChanged)
    def windowBorder(self) -> int:
        return self._window_border

    @Property(int, notify=layoutOrientationChanged)
    def layoutOrientation(self) -> int:
        return self._settings.layout_orientation

    @Slot(Qt.Key, Qt.KeyboardModifier)
    def forwardKeyToPlayer(self, key: Qt.Key, modifiers: Qt.KeyboardModifier) -> None:
        if command := self._command_generator.generate_command(key, modifiers):
            self._player.press_key(command)

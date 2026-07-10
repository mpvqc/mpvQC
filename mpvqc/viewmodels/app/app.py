# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import inject
from PySide6.QtCore import Property, QObject, Qt, Signal, Slot
from PySide6.QtQml import QmlElement

from mpvqc.services import (
    KeyCommandGeneratorService,
    MainWindowService,
    PlayerService,
    SettingsService,
)

QML_IMPORT_NAME = "io.github.mpvqc.mpvQC.Python"
QML_IMPORT_MAJOR_VERSION = 1


@QmlElement
class MpvqcAppViewModel(QObject):
    _main_window = inject.attr(MainWindowService)
    _settings = inject.attr(SettingsService)
    _player = inject.attr(PlayerService)
    _command_generator = inject.attr(KeyCommandGeneratorService)

    shadowMarginChanged = Signal(int)
    layoutOrientationChanged = Signal(int)

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self._main_window.shadow_margin_changed.connect(self.shadowMarginChanged)
        self._settings.layout_orientation_changed.connect(self.layoutOrientationChanged)

    @Property(int, notify=shadowMarginChanged)
    def shadowMargin(self) -> int:
        return self._main_window.shadow_margin

    @Property(int, notify=layoutOrientationChanged)
    def layoutOrientation(self) -> int:
        return self._settings.layout_orientation

    @Slot(Qt.Key, Qt.KeyboardModifier)
    def forwardKeyToPlayer(self, key: Qt.Key, modifiers: Qt.KeyboardModifier) -> None:
        if command := self._command_generator.generate_command(key, modifiers):
            self._player.press_key(command)

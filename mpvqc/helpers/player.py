# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import inject
from PySide6.QtCore import QObject, Slot
from PySide6.QtQml import QmlElement

from mpvqc.services import KeyCommandGeneratorService, PlayerService

QML_IMPORT_NAME = "pyobjects"
QML_IMPORT_MAJOR_VERSION = 1


@QmlElement
class MpvqcMpvPlayerPyObject(QObject):
    _player: PlayerService = inject.attr(PlayerService)
    _command_generator: KeyCommandGeneratorService = inject.attr(KeyCommandGeneratorService)

    @Slot()
    def pause(self) -> None:
        self._player.pause()

    @Slot(int, int)
    def handle_key_event(self, key: int, modifiers: int):
        if command := self._command_generator.generate_command(key, modifiers):
            self._player.execute(command)

    @Slot(int)
    def jump_to(self, seconds: int) -> None:
        self._player.jump_to(seconds)

    @Slot()
    def terminate(self) -> None:
        self._player.terminate()

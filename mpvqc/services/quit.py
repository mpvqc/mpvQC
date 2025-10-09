# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import platform

import inject
from PySide6.QtCore import QCoreApplication, QObject, QTimer, Signal

from .player import PlayerService
from .state import StateService


class QuitService(QObject):
    _state: StateService = inject.attr(StateService)
    _player: PlayerService = inject.attr(PlayerService)

    confirmQuit = Signal()

    def __init__(self, /):
        super().__init__()
        self._quit_despite_unsaved_changes = False

    def can_quit(self) -> bool:
        # noinspection PyTypeChecker
        return self._state.saved or self._quit_despite_unsaved_changes

    def request_quit(self) -> None:
        self.confirmQuit.emit()

    def confirm_quit_despite_unsaved_changes(self) -> None:
        self._quit_despite_unsaved_changes = True

    def shutdown(self) -> None:
        if platform.system() == "Windows":
            # Required to shut down explicitly due to nested window for player
            self._player.terminate()

        QTimer.singleShot(0, QCoreApplication.quit)

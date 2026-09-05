# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import override

import inject
from PySide6.QtCore import QEvent, QObject, QTimer, Signal
from PySide6.QtGui import QWindow

from mpvqc.player.services import PlayerService
from mpvqc.services import StateService


class QuitService(QObject):
    _player = inject.attr(PlayerService)
    _state = inject.attr(StateService)

    confirmation_needed = Signal()

    def __init__(self, /) -> None:
        super().__init__()
        self._window: QWindow | None = None
        self._quit_despite_unsaved_changes = False

    def attach(self, window: QWindow) -> None:
        self._window = window
        window.installEventFilter(self)

    def quit_despite_unsaved_changes(self) -> None:
        if self._window is None:
            msg = "QuitService.attach() has not been called yet"
            raise RuntimeError(msg)
        self._quit_despite_unsaved_changes = True
        QTimer.singleShot(0, self._window.close)

    @override
    def eventFilter(self, obj: QObject, event: QEvent) -> bool:
        if event.type() == QEvent.Type.Close:
            if self._state.saved or self._quit_despite_unsaved_changes:
                self._player.terminate()
                event.accept()
                return False

            self.confirmation_needed.emit()
            event.ignore()
            return True

        return super().eventFilter(obj, event)

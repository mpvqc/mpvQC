# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import inject
from PySide6.QtQml import QmlElement
from PySide6.QtQuick import QQuickWindow

from mpvqc.services import FramelessWindowService, PlayerService

QML_IMPORT_NAME = "pyobjects"
QML_IMPORT_MAJOR_VERSION = 1


# noinspection PyUnresolvedReferences
@QmlElement
class MpvWindowPyObject(QQuickWindow):
    _player: PlayerService = inject.attr(PlayerService)
    _frameless_window: FramelessWindowService = inject.attr(FramelessWindowService)

    def __init__(self):
        super().__init__()
        win_id = self.winId()
        self._player.init(win_id=win_id)
        self._frameless_window.set_embedded_player_hwnd(win_id)

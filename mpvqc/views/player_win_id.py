# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import inject
from PySide6.QtCore import Qt
from PySide6.QtGui import QWindow
from PySide6.QtQml import QmlElement

from mpvqc.services import PlatformService, PlayerService

QML_IMPORT_NAME = "io.github.mpvqc.mpvQC.Python"
QML_IMPORT_MAJOR_VERSION = 1


@QmlElement
class MpvWindowPyObject(QWindow):
    _player = inject.attr(PlayerService)
    _platform = inject.attr(PlatformService)

    def __init__(self) -> None:
        super().__init__()
        self.setFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowTransparentForInput)
        win_id = self.winId()
        self._player.init(win_id=win_id)
        self._platform.track_embedded_player(win_id)

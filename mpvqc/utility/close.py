# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import inject
from PySide6.QtCore import QEvent, QObject

from mpvqc.services import QuitService


class CloseEventFilter(QObject):
    _quit: QuitService = inject.attr(QuitService)

    def eventFilter(self, obj, event):
        match event.type():
            case QEvent.Type.Close if self._quit.can_quit():
                self._quit.shutdown()
                event.accept()
                return True

            case QEvent.Type.Close:
                self._quit.request_quit()
                event.ignore()
                return True

            case _:
                return super().eventFilter(obj, event)

# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import override

import inject
from PySide6.QtCore import QEvent, QObject

from mpvqc.services import QuitService


class CloseEventFilter(QObject):
    _quit = inject.attr(QuitService)

    @override
    def eventFilter(self, obj: QObject, event: QEvent) -> bool:
        match event.type():
            case QEvent.Type.Close if self._quit.can_quit():
                self._quit.shutdown()
                event.accept()
                return True

            case QEvent.Type.Close:
                self._quit.request_quit()
                event.ignore()
                return True

        return super().eventFilter(obj, event)

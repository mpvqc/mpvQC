# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import inject
from PySide6.QtCore import Property, QObject, QRunnable, QThreadPool, Signal
from PySide6.QtQml import QmlElement

from mpvqc.services import WindowButtonsService

QML_IMPORT_NAME = "pyobjects"
QML_IMPORT_MAJOR_VERSION = 1


# noinspection PyPep8Naming,PyTypeChecker
@QmlElement
class MpvqcWindowButtons(QObject):
    _buttons: WindowButtonsService = inject.attr(WindowButtonsService)

    showMinimizeButtonChanged = Signal(bool)
    showMaximizeButtonChanged = Signal(bool)
    showCloseButtonChanged = Signal(bool)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._preferences = self._buttons.defaults()

        def _detection_job():
            preferences = self._buttons.detect()
            self._on_detection_complete(preferences)

        job = QRunnable.create(_detection_job)
        QThreadPool.globalInstance().start(job)

    @Property(bool, notify=showMinimizeButtonChanged)
    def showMinimizeButton(self) -> bool:
        return self._preferences.minimize

    @Property(bool, notify=showMaximizeButtonChanged)
    def showMaximizeButton(self) -> bool:
        return self._preferences.maximize

    @Property(bool, notify=showCloseButtonChanged)
    def showCloseButton(self) -> bool:
        return self._preferences.close

    def _on_detection_complete(self, preferences):
        if self._preferences.minimize != preferences.minimize:
            self._preferences.minimize = preferences.minimize
            self.showMinimizeButtonChanged.emit(preferences.minimize)

        if self._preferences.maximize != preferences.maximize:
            self._preferences.maximize = preferences.maximize
            self.showMaximizeButtonChanged.emit(preferences.maximize)

        if self._preferences.close != preferences.close:
            self._preferences.close = preferences.close
            self.showCloseButtonChanged.emit(preferences.close)

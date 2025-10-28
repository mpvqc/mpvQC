# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import inject
from PySide6.QtCore import Property, QObject, QRunnable, QThreadPool, Signal
from PySide6.QtQml import QmlElement

from mpvqc.services import HostIntegrationService, WindowButtonPreference

QML_IMPORT_NAME = "pyobjects"
QML_IMPORT_MAJOR_VERSION = 1


# noinspection PyPep8Naming,PyTypeChecker
@QmlElement
class MpvqcWindowButtons(QObject):
    _host_integration: HostIntegrationService = inject.attr(HostIntegrationService)

    showMinimizeButtonChanged = Signal(bool)
    showMaximizeButtonChanged = Signal(bool)
    showCloseButtonChanged = Signal(bool)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._preference: WindowButtonPreference = self._host_integration.DEFAULT_WINDOW_BUTTON_PREFERENCE

        def _detection_job():
            preferences = self._host_integration.get_window_button_preference()
            self._on_detection_complete(preferences)

        job = QRunnable.create(_detection_job)
        QThreadPool.globalInstance().start(job)

    @Property(bool, notify=showMinimizeButtonChanged)
    def showMinimizeButton(self) -> bool:
        return self._preference.minimize

    @Property(bool, notify=showMaximizeButtonChanged)
    def showMaximizeButton(self) -> bool:
        return self._preference.maximize

    @Property(bool, notify=showCloseButtonChanged)
    def showCloseButton(self) -> bool:
        return self._preference.close

    def _on_detection_complete(self, new_preference: WindowButtonPreference):
        old_preference = self._preference
        self._preference = new_preference

        if old_preference.minimize != new_preference.minimize:
            self.showMinimizeButtonChanged.emit(new_preference.minimize)

        if old_preference.maximize != new_preference.maximize:
            self.showMaximizeButtonChanged.emit(new_preference.maximize)

        if old_preference.close != new_preference.close:
            self.showCloseButtonChanged.emit(new_preference.close)

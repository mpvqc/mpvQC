# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import inject
from PySide6.QtCore import Property, QObject, Signal, Slot
from PySide6.QtQml import QmlElement

from mpvqc.services import HostIntegrationService, WindowButtonPreference

QML_IMPORT_NAME = "io.github.mpvqc.mpvQC.Python"
QML_IMPORT_MAJOR_VERSION = 1


# noinspection PyPep8Naming,PyTypeChecker
@QmlElement
class MpvqcWindowButtonsViewModel(QObject):
    _host_integration = inject.attr(HostIntegrationService)

    showMinimizeButtonChanged = Signal(bool)
    showMaximizeButtonChanged = Signal(bool)
    showCloseButtonChanged = Signal(bool)

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self._preference = self._host_integration.window_button_preference
        self._host_integration.window_button_preference_changed.connect(self._on_preference_changed)

    @Property(bool, notify=showMinimizeButtonChanged)
    def showMinimizeButton(self) -> bool:
        return self._preference.minimize

    @Property(bool, notify=showMaximizeButtonChanged)
    def showMaximizeButton(self) -> bool:
        return self._preference.maximize

    @Property(bool, notify=showCloseButtonChanged)
    def showCloseButton(self) -> bool:
        return self._preference.close

    @Slot(object)
    def _on_preference_changed(self, preference: WindowButtonPreference) -> None:
        old = self._preference
        self._preference = preference

        if old.minimize != preference.minimize:
            self.showMinimizeButtonChanged.emit(preference.minimize)
        if old.maximize != preference.maximize:
            self.showMaximizeButtonChanged.emit(preference.maximize)
        if old.close != preference.close:
            self.showCloseButtonChanged.emit(preference.close)

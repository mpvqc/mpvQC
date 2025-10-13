# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import inject
from PySide6.QtCore import Property, QObject, Signal
from PySide6.QtQml import QmlElement

from mpvqc.services import SettingsService

QML_IMPORT_NAME = "pyobjects"
QML_IMPORT_MAJOR_VERSION = 1


# noinspection PyTypeChecker,PyPep8Naming
@QmlElement
class MpvqcPlaceholderViewModel(QObject):
    _settings: SettingsService = inject.attr(SettingsService)

    layoutOrientationChanged = Signal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._settings.layoutOrientationChanged.connect(self.layoutOrientationChanged)

    @Property(int, notify=layoutOrientationChanged)
    def layoutOrientation(self) -> int:
        return self._settings.layout_orientation

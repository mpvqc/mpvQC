# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import inject
from PySide6.QtCore import Property, QObject, Signal
from PySide6.QtQml import QmlElement

from mpvqc.services import SettingsService

QML_IMPORT_NAME = "io.github.mpvqc.mpvQC.Python"
QML_IMPORT_MAJOR_VERSION = 1


@QmlElement
class MpvqcPlaceholderViewModel(QObject):
    _settings = inject.attr(SettingsService)

    layoutOrientationChanged = Signal(int)

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self._settings.layout_orientation_changed.connect(self.layoutOrientationChanged)

    @Property(int, notify=layoutOrientationChanged)
    def layoutOrientation(self) -> int:
        return self._settings.layout_orientation

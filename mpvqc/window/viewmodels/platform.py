# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import inject
from PySide6.QtCore import Property, QObject
from PySide6.QtQml import QmlElement

from mpvqc.window.services import PlatformService

QML_IMPORT_NAME = "io.github.mpvqc.mpvQC.Python"
QML_IMPORT_MAJOR_VERSION = 1


@QmlElement
class MpvqcPlatformViewModel(QObject):
    _platform = inject.attr(PlatformService)

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        platform = self._platform
        self._keeps_native_frame = platform.keeps_native_frame
        self._draws_drop_shadow = platform.draws_drop_shadow

    @Property(bool, constant=True)
    def keepsNativeFrame(self) -> bool:
        return self._keeps_native_frame

    @Property(bool, constant=True)
    def drawsDropShadow(self) -> bool:
        return self._draws_drop_shadow

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
        self._capabilities = self._platform.capabilities

    @Property(bool, constant=True)
    def keepsNativeFrame(self) -> bool:
        return self._capabilities.keeps_native_frame

    @Property(bool, constant=True)
    def canDrawOwnFrame(self) -> bool:
        return self._capabilities.can_draw_own_frame

    @Property(bool, constant=True)
    def embedsNativePlayer(self) -> bool:
        return self._capabilities.embeds_native_player

    @Property(bool, constant=True)
    def popupsNeedSeparateWindows(self) -> bool:
        return self._capabilities.popups_need_separate_windows

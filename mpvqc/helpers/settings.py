# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from enum import IntEnum

import inject
from PySide6.QtCore import Property, QEnum, QObject, Signal
from PySide6.QtQml import QmlElement

from mpvqc.decorators import QmlSingletonInProductionOnly
from mpvqc.services import SettingsService

QML_IMPORT_NAME = "pyobjects"
QML_IMPORT_MAJOR_VERSION = 1


# noinspection PyPep8Naming,PyTypeChecker
@QmlElement
@QmlSingletonInProductionOnly
class MpvqcSettings(QObject):
    _settings: SettingsService = inject.attr(SettingsService)

    @QEnum
    class WindowTitleFormat(IntEnum):
        DEFAULT = 0
        FILE_NAME = 1
        FILE_PATH = 2

    # Common
    commentTypesChanged = Signal(list)

    # SplitView
    layoutOrientationChanged = Signal(int)

    def __init__(self, parent=None):
        super().__init__(parent)

        self._settings.commentTypesChanged.connect(self.commentTypesChanged)
        self._settings.layoutOrientationChanged.connect(self.layoutOrientationChanged)

    @Property(list, notify=commentTypesChanged)
    def commentTypes(self) -> list[str]:
        return self._settings.comment_types

    @commentTypes.setter
    def commentTypes(self, value: list[str]):
        self._settings.comment_types = value

    @Property(int, notify=layoutOrientationChanged)
    def layoutOrientation(self) -> int:
        return self._settings.layout_orientation

    @layoutOrientation.setter
    def layoutOrientation(self, value: int):
        self._settings.layout_orientation = value

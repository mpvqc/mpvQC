# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import inject
from PySide6.QtCore import Property, QObject, Signal
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

    commentTypesChanged = Signal(list)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._settings.commentTypesChanged.connect(self.commentTypesChanged)

    @Property(list, notify=commentTypesChanged)
    def commentTypes(self) -> list[str]:
        return self._settings.comment_types

    @commentTypes.setter
    def commentTypes(self, value: list[str]):
        self._settings.comment_types = value

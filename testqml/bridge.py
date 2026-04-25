# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import inject
from PySide6.QtCore import Property, QObject, Slot
from PySide6.QtQml import QmlElement

from mpvqc.services import StateService
from testqml.injections import configure_injections

QML_IMPORT_NAME = "pyobjects"
QML_IMPORT_MAJOR_VERSION = 1


@QmlElement
class MpvqcTestBridge(QObject):
    @Slot()
    def resetState(self) -> None:
        configure_injections()

    @Property(bool)
    def saved(self) -> bool:
        return bool(inject.instance(StateService).saved)

    @Slot()
    def markUnsaved(self) -> None:
        inject.instance(StateService).change()

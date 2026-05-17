# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from enum import IntEnum, auto

from PySide6.QtCore import QEnum, QObject
from PySide6.QtQml import QmlElement

QML_IMPORT_NAME = "io.github.mpvqc.mpvQC.Python"
QML_IMPORT_MAJOR_VERSION = 1


@QmlElement
class MpvqcImportWizardStepKind(QObject):
    class StepKind(IntEnum):
        ERRORS = auto()
        SESSION = auto()
        VIDEO = auto()
        SUBTITLES = auto()

    QEnum(StepKind)


StepKind = MpvqcImportWizardStepKind.StepKind

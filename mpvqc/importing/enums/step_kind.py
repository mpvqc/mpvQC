# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from enum import IntEnum

from PySide6.QtCore import QEnum, QObject
from PySide6.QtQml import QmlElement

from mpvqc.importing import domain

QML_IMPORT_NAME = "io.github.mpvqc.mpvQC.Python"
QML_IMPORT_MAJOR_VERSION = 1


@QmlElement
class MpvqcImportWizardStepKind(QObject):
    @QEnum
    class StepKind(IntEnum):
        ERRORS = domain.StepKind.ERRORS
        SESSION = domain.StepKind.SESSION
        VIDEO = domain.StepKind.VIDEO
        SUBTITLES = domain.StepKind.SUBTITLES

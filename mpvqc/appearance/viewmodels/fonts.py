# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from PySide6.QtCore import Property, QObject
from PySide6.QtGui import QFont
from PySide6.QtQml import QmlElement

from mpvqc.appearance.services import application_font, monospace_font

QML_IMPORT_NAME = "io.github.mpvqc.mpvQC.Python"
QML_IMPORT_MAJOR_VERSION = 1


@QmlElement
class MpvqcFontsViewModel(QObject):
    @Property(QFont, constant=True)
    def applicationFont(self) -> QFont:
        return application_font()

    @Property(QFont, constant=True)
    def monospaceFont(self) -> QFont:
        return monospace_font()

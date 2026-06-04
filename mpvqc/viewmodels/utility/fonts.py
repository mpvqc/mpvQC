# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import inject
from PySide6.QtCore import Property, QObject
from PySide6.QtGui import QFont
from PySide6.QtQml import QmlElement

from mpvqc.services import FontLoaderService

QML_IMPORT_NAME = "io.github.mpvqc.mpvQC.Python"
QML_IMPORT_MAJOR_VERSION = 1


@QmlElement
class MpvqcFontsViewModel(QObject):
    _font_loader = inject.attr(FontLoaderService)

    @Property(QFont, constant=True)
    def applicationFont(self) -> QFont:
        return self._font_loader.application_font()

    @Property(QFont, constant=True)
    def monospaceFont(self) -> QFont:
        return self._font_loader.monospace_font()

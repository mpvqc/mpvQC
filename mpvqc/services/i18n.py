# mpvQC
#
# Copyright (C) 2025 mpvQC developers
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from PySide6.QtCore import QLibraryInfo, QLocale, QTranslator
from PySide6.QtGui import QGuiApplication


class InternationalizationService:
    def __init__(self):
        self._translator_mpvqc = QTranslator()
        self._translator_qt = QTranslator()

    def retranslate(self, app: QGuiApplication, language_code: str) -> None:
        app.removeTranslator(self._translator_qt)
        app.removeTranslator(self._translator_mpvqc)

        locale = QLocale(language_code)

        self._translator_qt.load(
            locale, "qtbase", "_", QLibraryInfo.location(QLibraryInfo.LibraryPath.TranslationsPath)
        )
        self._translator_mpvqc.load(f":/i18n/{language_code}.qm")

        app.installTranslator(self._translator_qt)
        app.installTranslator(self._translator_mpvqc)

        app.setLayoutDirection(locale.textDirection())

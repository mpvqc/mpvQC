#  mpvQC
#
#  Copyright (C) 2022 mpvQC developers
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.


from typing import Optional

from PySide6.QtCore import QTranslator, QObject, QLocale
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine


class TranslationService(QObject):

    def __init__(self):
        super().__init__()
        self._application: Optional[QGuiApplication] = None
        self._engine: Optional[QQmlApplicationEngine] = None
        self._translator = QTranslator()

    def initialize_with(self, application: QGuiApplication, engine: QQmlApplicationEngine):
        self._application = application
        self._engine = engine

    def load(self, language: str) -> None:
        self._load_translator_for(language)
        self._update_layout_direction_for(language)
        self._retranslate()

    def _load_translator_for(self, language: str):
        resource = self._translation_path_for(language)
        self._application.removeTranslator(self._translator)
        self._translator.load(resource)
        self._application.installTranslator(self._translator)

    def _update_layout_direction_for(self, language: str) -> None:
        self._application.setLayoutDirection(QLocale(language).textDirection())

    def _retranslate(self):
        self._engine.retranslate()

    @staticmethod
    def _translation_path_for(locale: str):
        return f':/qm/{locale}.qm'

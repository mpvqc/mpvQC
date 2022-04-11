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


import inject
from PySide6.QtCore import Property, Signal, Slot, QObject
from PySide6.QtQml import QmlElement, QmlSingleton

from mpvqc.services import TranslationService

QML_IMPORT_NAME = "pyobjects"
QML_IMPORT_MAJOR_VERSION = 1


@QmlElement
@QmlSingleton
class TranslationPyObject(QObject):
    _translator = inject.attr(TranslationService)

    def get_rtl_enabled(self) -> bool:
        return self._translator.rtl_enabled

    rtl_enabled_changed = Signal(bool)
    rtl_enabled = Property(bool, get_rtl_enabled, notify=rtl_enabled_changed)

    @Slot(str)
    def load_translation(self, language: str):
        rtl_enable_before = self.get_rtl_enabled()
        self._translator.set_language(language)
        rtl_enabled_after = self.get_rtl_enabled()

        if rtl_enable_before != rtl_enabled_after:
            self.rtl_enabled_changed.emit(rtl_enabled_after)

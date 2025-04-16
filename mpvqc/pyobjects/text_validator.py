# mpvQC
#
# Copyright (C) 2022 mpvQC developers
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

from PySide6.QtCore import Slot
from PySide6.QtGui import QValidator
from PySide6.QtQml import QmlElement

QML_IMPORT_NAME = "pyobjects"
QML_IMPORT_MAJOR_VERSION = 1


@QmlElement
class MpvqcDefaultTextValidatorPyObject(QValidator):
    def validate(self, user_input: str, position: int):
        return QValidator.State.Acceptable, self.replace_special_characters(user_input), position

    @Slot(str, result=str)
    def replace_special_characters(self, string_to_replace) -> str:
        # fmt: off
        return string_to_replace \
            .replace("\xad", "") \
            .replace("\r", "") \
            .replace("\n", "")
        # fmt: on

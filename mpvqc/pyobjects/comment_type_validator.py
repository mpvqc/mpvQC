# mpvQC
#
# Copyright (C) 2024 mpvQC developers
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

import inject
from PySide6.QtCore import Slot, QObject
from PySide6.QtQml import QmlElement

from mpvqc.services import CommentTypeValidatorService

QML_IMPORT_NAME = "pyobjects"
QML_IMPORT_MAJOR_VERSION = 1


@QmlElement
class MpvqcCommentTypeValidatorPyObject(QObject):
    _validator: CommentTypeValidatorService = inject.attr(CommentTypeValidatorService)

    @Slot(str, list, result=str or None)
    def validate_new_comment_type(self, new_comment_type: str, existing_comment_types: list[str]) -> str or None:
        return self._validator.validate_new_comment_type(new_comment_type, existing_comment_types)

    @Slot(str, str, list, result=str or None)
    def validate_editing_of_comment_type(
        self, new_comment_type: str, comment_type_being_edited: str, existing_comment_types: list[str]
    ) -> str or None:
        return self._validator.validate_editing_of_comment_type(
            new_comment_type, comment_type_being_edited, existing_comment_types
        )

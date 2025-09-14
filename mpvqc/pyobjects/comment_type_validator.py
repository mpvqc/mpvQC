# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import inject
from PySide6.QtCore import QObject, Slot
from PySide6.QtQml import QmlElement

from mpvqc.services import CommentTypeValidatorService

QML_IMPORT_NAME = "pyobjects"
QML_IMPORT_MAJOR_VERSION = 1


@QmlElement
class MpvqcCommentTypeValidatorPyObject(QObject):
    _validator: CommentTypeValidatorService = inject.attr(CommentTypeValidatorService)

    @Slot(str, list, result=str)
    def validate_new_comment_type(self, new_comment_type: str, existing_comment_types: list[str]) -> str | None:
        return self._validator.validate_new_comment_type(new_comment_type, existing_comment_types)

    @Slot(str, str, list, result=str)
    def validate_editing_of_comment_type(
        self, new_comment_type: str, comment_type_being_edited: str, existing_comment_types: list[str]
    ) -> str | None:
        return self._validator.validate_editing_of_comment_type(
            new_comment_type, comment_type_being_edited, existing_comment_types
        )

/*
mpvQC

Copyright (C) 2022 mpvQC developers

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/

import QtQuick
import QtQuick.Layouts
import models

QtObject {
    required property var reverseTranslator
    required property MpvqcCommentTypesModel model

    readonly property var forbiddenCharactors: /[,[\]]/

    function validateNewCommentType(commentType: string): string {
        if (_isEmpty(commentType)) {
            return qsTranslate('CommentTypesDialog', 'A comment type must not be blank')
        }
        if (_forbiddenCharatersIn(commentType)) {
            return qsTranslate('CommentTypesDialog', 'Characters \',[]\' not allowed')
        }
        const items = _getAllItems()
        if (_alreadyExistsIn(items, commentType)) {
            return qsTranslate('CommentTypesDialog', 'Comment type already exists')
        }
        return null
    }

    function _isEmpty(commentType: string): bool {
        return commentType === null || commentType.trim() === ''
    }

    function _forbiddenCharatersIn(commentType: string): bool {
        return forbiddenCharactors.test(commentType)
    }

    function _getAllItems(): Array<string> {
        return model.items()
    }

    function _alreadyExistsIn(englishCommentTypes: Array<string>, newCommentType: string): bool {
        return englishCommentTypes.includes(newCommentType)
            || englishCommentTypes.includes(reverseTranslator.lookup(newCommentType))
    }

    function validateEditingOf(commentTypeToEdit: string, commentType: string): string {
        if (_isEmpty(commentType)) {
            return qsTranslate('CommentTypesDialog', 'A comment type must not be blank')
        }
        if (_forbiddenCharatersIn(commentType)) {
            return qsTranslate('CommentTypesDialog', 'Characters \',[]\' not allowed')
        }
        const items = _getAllItemsExcept(commentTypeToEdit)
        if (_alreadyExistsIn(items, commentType)) {
            return qsTranslate('CommentTypesDialog', 'Comment type already exists')
        }
        return null
    }

    function _getAllItemsExcept(item: string): Array<string> {
        const lookup = reverseTranslator.lookup(item)
        const items = _getAllItems()
        _remove(lookup, items)
        return items
    }

    function _remove(item: string, array: Array<string>): void {
        const index = array.indexOf(item)
        if (index !== -1) {
            array.splice(index, 1)
        }
    }

}

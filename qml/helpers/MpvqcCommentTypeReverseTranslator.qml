/*
mpvQC

Copyright (C) 2022 mpvQC developers

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/


pragma Singleton
import QtQuick
import models


QtObject {
    readonly property string language: Qt.uiLanguage
    readonly property var commentTypeModel: MpvqcCommentTypesModel {}
    property var translations: ({})

    onLanguageChanged: {
        const mapping = new Map()
        for (let i = 0, count = commentTypeModel.count; i < count; i++) {
            const commentType = commentTypeModel.get(i)
            const english = commentType.type
            const currentLanguage = qsTranslate("CommentTypes", english)
            mapping[currentLanguage] = english
        }
        translations = mapping
    }

    function lookup(commentTypeCurrentLanguage) {
        return translations[commentTypeCurrentLanguage] || commentTypeCurrentLanguage
    }

}

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

import models


QtObject {
    id: root

    readonly property string language: Qt.uiLanguage
    readonly property var commentTypes: MpvqcCommentTypesModel {}

    property var translations: ({})

    property var timer: Timer {
        interval: 500

        onTriggered: {
            _recreateLookupTable()
        }

        function _recreateLookupTable(): void {
            const mapping = new Map()
            for (let i = 0, count = root.commentTypes.count; i < count; i++) {
                const commentType = root.commentTypes.get(i)
                const english = commentType.type
                const currentLanguage = qsTranslate("CommentTypes", english)
                mapping[currentLanguage] = english
            }
            root.translations = mapping
        }
    }

    function lookup(translated): string {
        return translations[translated] || translated
    }

    function _scheduleLookupTableReset(): void {
        timer.start()
    }

    onLanguageChanged: {
        _scheduleLookupTableReset()
    }

}

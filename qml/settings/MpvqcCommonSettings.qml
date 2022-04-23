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


import QtQuick
import Qt.labs.settings
import models
import "MpvqcDefaultLanguage.js" as MpvqcLanguage


Item {
    id: current
    required property var settingsFile
    property string language: settings.language
    property var commentTypes: MpvqcCommentTypes {}

    Settings {
        id: settings
        fileName: current.settingsFile
        category: "Common"
        property string language: MpvqcLanguage.getDefault(current)
    }

    function store() {
        settings.language = current.language
        _storeCommentTypesInSettings()
    }

    function _storeCommentTypesInSettings() {
        const model = current.commentTypes
        const marshalled = []
        for (let i = 0, count = model.count; i < count; i++) {
            marshalled.push(model.get(i))
        }
        settings.setValue("commentTypes", JSON.stringify(marshalled))
    }

    function restore() {
        _loadCommentTypesFromSettings()
    }

    function _loadCommentTypesFromSettings() {
        const fromSettings = settings.value("commentTypes")
        if (fromSettings) {
            _replaceDefaultCommentTypesWithThose(JSON.parse(fromSettings))
        }
    }

    function _replaceDefaultCommentTypesWithThose(fromSettings) {
        commentTypes.clear()
        for (const commentType of fromSettings) {
            commentTypes.append(commentType)
        }
    }

}

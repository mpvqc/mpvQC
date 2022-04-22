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
import helpers
import pyobjects


QtObject {
    id: object

    readonly property var commentTypesDefined: SettingsPyObject.comment_types
    readonly property var commentTypesImported: ["Hallo", "helloHello"]
    property int widthCommentTypesDefined: 0
    property int widthCommentTypesImported: 0
    property int width: Math.max(widthCommentTypesDefined, widthCommentTypesImported)

    Component.onCompleted: {
        MpvqcSettings.onLanguageChanged.connect(() => {
            object.widthCommentTypesDefined = calculateMaxWidthOf(commentTypesDefined)
        })
    }

    onCommentTypesDefinedChanged: {
        object.widthCommentTypesDefined = calculateMaxWidthOf(commentTypesDefined)
    }

    onCommentTypesImportedChanged: {
        object.widthCommentTypesImported = calculateMaxWidthOf(commentTypesImported)
    }

    function calculateMaxWidthOf(elements) {
        const metric = Qt.createQmlObject('import QtQuick; TextMetrics { font.pixelSize: 16 }', object)
        let width = 0
        for (let element of elements) {
            metric.text = qsTranslate("CommentTypes", element)
            width = Math.max(width, metric.tightBoundingRect.width)
        }
        metric.destroy()
        return width + 6
    }

}

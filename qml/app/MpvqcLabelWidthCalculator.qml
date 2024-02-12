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


Item {
    id: root

    required property var mpvqcApplication

    readonly property var mpvqcSettings: mpvqcApplication.mpvqcSettings

    property int commentTypesWidth

    function _recalculateCommentTypesWidth(): void {
        const commentTypes = mpvqcSettings.commentTypes.items().map(english => qsTranslate("CommentTypes", english))
        root.commentTypesWidth = calculateWidthFor(commentTypes, root)
    }

    /**
     * @param texts {Array<string>}
     * @param parent {QtObject}
     */
    function calculateWidthFor(texts, parent): real {
        const textMetric = Qt.createQmlObject('import QtQuick; TextMetrics { font.family: "Noto Sans"; font.pointSize: 10 }', parent)
        let width = 0
        for (const text of texts) {
            textMetric.text = text
            width = Math.max(width, textMetric.tightBoundingRect.width)
        }
        textMetric.destroy()
        return width
    }

    Connections {
        target: root.mpvqcSettings

        function onCommentTypesChanged() { root._recalculateCommentTypesWidth() }
        function onLanguageChanged() { root._recalculateCommentTypesWidth() }
    }

    Component.onCompleted: {
        _recalculateCommentTypesWidth()
    }

}

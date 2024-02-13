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
    readonly property var mpvqcTimeFormatUtils: mpvqcApplication.mpvqcTimeFormatUtils
    readonly property real duration: mpvqcApplication.mpvqcMpvPlayerPropertiesPyObject.duration

    property int commentTypesLabelWidth
    property int timeLabelWidth

    function calculateWidthFor(texts, parent): int {
        const textMetric = Qt.createQmlObject('import QtQuick; TextMetrics { font.family: "Noto Sans"; font.pointSize: 10 }', parent)
        let width = 0
        for (const text of texts) {
            textMetric.text = text
            width = Math.max(width, textMetric.tightBoundingRect.width)
        }
        textMetric.destroy()
        return width
    }

    function _recalculateCommentTypesLabelWidth(): void {
        const commentTypes = mpvqcSettings.commentTypes.items()
            .map(english => qsTranslate("CommentTypes", english))
        root.commentTypesLabelWidth = calculateWidthFor(commentTypes, root)
    }

    function _recalculateTimeLabelWidth(): void {
        const hour = 60 * 60
        const texts = []
        for (let i = 0; i <= 9; i++) {
            texts.push(duration >= hour ? `${i}${i}:${i}${i}:${i}${i}` : `${i}${i}:${i}${i}`)
        }
        root.timeLabelWidth = calculateWidthFor(texts, root)
    }

    onDurationChanged: {
        _recalculateTimeLabelWidth()
    }

    Connections {
        target: root.mpvqcSettings

        function onCommentTypesChanged() { root._recalculateCommentTypesLabelWidth() }
        function onLanguageChanged() { root._recalculateCommentTypesLabelWidth() }
    }

    Component.onCompleted: {
        _recalculateCommentTypesLabelWidth()
        _recalculateTimeLabelWidth()
    }

}

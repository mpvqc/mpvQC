// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

import QtQuick

Item {
    id: root

    required property var mpvqcApplication

    readonly property var mpvqcSettings: mpvqcApplication.mpvqcSettings
    readonly property real duration: mpvqcApplication.mpvqcMpvPlayerPropertiesPyObject.duration

    property int commentTypesLabelWidth
    property int timeLabelWidth

    function calculateWidthFor(texts, parent): int {
        const textMetric = Qt.createQmlObject("import QtQuick; TextMetrics { font.family: 'Noto Sans'; font.pointSize: 10 }", parent);
        let width = 0;
        for (const text of texts) {
            textMetric.text = text;
            width = Math.max(width, textMetric.tightBoundingRect.width);
        }
        textMetric.destroy();
        return width;
    }

    function _recalculateCommentTypesLabelWidth(): void {
        const commentTypes = mpvqcSettings.commentTypes.map(english => qsTranslate("CommentTypes", english));
        root.commentTypesLabelWidth = calculateWidthFor(commentTypes, root);
    }

    function _recalculateTimeLabelWidth(): void {
        const hour = 60 * 60;
        const texts = [];
        for (let i = 0; i <= 9; i++) {
            texts.push(duration >= hour ? `${i}${i}:${i}${i}:${i}${i}` : `${i}${i}:${i}${i}`);
        }
        root.timeLabelWidth = calculateWidthFor(texts, root);
    }

    onDurationChanged: {
        _recalculateTimeLabelWidth();
    }

    Connections {
        target: root.mpvqcSettings

        function onCommentTypesChanged(): void {
            root._recalculateCommentTypesLabelWidth();
        }

        function onLanguageChanged(): void {
            root._recalculateCommentTypesLabelWidth();
        }
    }

    Component.onCompleted: {
        _recalculateCommentTypesLabelWidth();
        _recalculateTimeLabelWidth();
    }
}

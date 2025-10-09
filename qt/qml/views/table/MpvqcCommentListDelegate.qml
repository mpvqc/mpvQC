// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

import QtQuick
import QtQuick.Controls.Material

import "MpvqcCommentHighlighter.js" as CommentHighlighter

Item {
    id: root

    required property int index             // from model
    required property int time              // from model
    required property string commentType    // from model
    required property string comment        // from model

    required property int timeLabelWidth
    required property int commentTypeLabelWidth

    required property var timeFormatFunc

    required property color backgroundColor
    required property color foregroundColor

    required property ListView listView
    required property string searchQuery

    readonly property alias commentLabel: _commentLabel

    property alias scrollBarWidth: _scrollBarSpacer.width
    property alias scrollBarBackgroundColor: _scrollBarSpacer.color

    readonly property int horizontalItemPadding: 14
    readonly property int verticalItemPadding: 13

    signal playButtonPressed

    signal timeLabelPressed(coordinates: point)
    signal commentTypeLabelPressed(coordinates: point)
    signal commentLabelPressed

    signal rightMouseButtonPressed(coordinates: point)

    height: Math.max(_commentLabel.height, _commentLabel.editorHeight, _playButton.height)

    Material.background: root.backgroundColor
    Material.foreground: root.foregroundColor

    Rectangle {
        y: root.y
        width: root.width
        height: root.height
        parent: root.parent
        color: root.backgroundColor
        z: -2
    }

    MouseArea {
        acceptedButtons: Qt.LeftButton | Qt.RightButton

        anchors {
            fill: parent
        }

        onPressed: event => {
            const coordinates = root.mapToItem(root.listView, mouseX, mouseY);

            if (event.button === Qt.RightButton) {
                root.rightMouseButtonPressed(coordinates);
                return;
            }

            const itemPressed = _row.childAt(mouseX, mouseY);

            switch (itemPressed) {
            case _timeLabel:
                root.timeLabelPressed(coordinates);
                break;
            case _commentTypeLabel:
                root.commentTypeLabelPressed(coordinates);
                break;
            case _commentLabel:
                root.commentLabelPressed();
                break;
            }
        }
    }

    Row {
        id: _row

        width: root.width

        ToolButton {
            id: _playButton

            focusPolicy: Qt.NoFocus
            icon.source: "qrc:/data/icons/play_arrow_24dp_1F1F1F_FILL0_wght400_GRAD0_opsz24.svg"

            onPressed: root.playButtonPressed()
        }

        Label {
            id: _timeLabel

            text: root.timeFormatFunc(root.time) // qmllint disable
            horizontalAlignment: Text.AlignHCenter

            width: root.timeLabelWidth + leftPadding + rightPadding
            height: root.height

            leftPadding: LayoutMirroring.enabled ? root.horizontalItemPadding : root.horizontalItemPadding * (2 / 3)
            rightPadding: LayoutMirroring.enabled ? root.horizontalItemPadding * (2 / 3) : root.horizontalItemPadding
            topPadding: root.verticalItemPadding
            bottomPadding: root.verticalItemPadding
        }

        Label {
            id: _commentTypeLabel

            text: qsTranslate("CommentTypes", root.commentType)
            horizontalAlignment: Text.AlignLeft

            width: root.commentTypeLabelWidth + leftPadding + rightPadding
            height: root.height

            leftPadding: root.horizontalItemPadding
            rightPadding: root.horizontalItemPadding
            topPadding: root.verticalItemPadding
            bottomPadding: root.verticalItemPadding
        }

        Label {
            id: _commentLabel

            property int editorHeight: -1 // will be manipulated from the popup above while editing

            text: root.searchQuery ? CommentHighlighter.highlightComment(root.comment, root.searchQuery) : root.comment
            textFormat: root.searchQuery ? Text.StyledText : Text.PlainText

            horizontalAlignment: Text.AlignLeft
            wrapMode: Text.WordWrap

            width: root.width - _playButton.width - _timeLabel.width - _commentTypeLabel.width - _scrollBarSpacer.width

            leftPadding: root.horizontalItemPadding
            rightPadding: root.horizontalItemPadding
            topPadding: root.verticalItemPadding
            bottomPadding: root.verticalItemPadding
        }

        Rectangle {
            id: _scrollBarSpacer
            height: root.height
        }
    }

    Behavior on foregroundColor {
        ColorAnimation {
            duration: 75
        }
    }
}

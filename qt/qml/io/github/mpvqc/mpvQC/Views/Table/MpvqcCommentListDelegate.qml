// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

import QtQuick
import QtQuick.Controls
import QtQuick.Controls.Material as M

import io.github.mpvqc.mpvQC.Utility

Item {
    id: root

    required property int index             // from model
    required property int time              // from model
    required property string commentType    // from model
    required property string comment        // from model

    required property string searchQuery

    readonly property alias commentLabel: _commentLabel
    property alias scrollBarWidth: _scrollBarSpacer.width

    readonly property color backgroundColor: MpvqcAppearance.palette.rowBackground(index)
    readonly property color foregroundColor: ListView.isCurrentItem ? MpvqcAppearance.palette.rowSelectedText : MpvqcAppearance.palette.rowForeground(index)

    readonly property int horizontalItemPadding: 14
    readonly property int verticalItemPadding: 13

    property color _foregroundColor: foregroundColor // mutable for animation
    property bool _isPooled: false

    signal playButtonPressed
    signal rowPressed
    signal rightMouseButtonPressed(coordinates: point)

    signal timeLabelDoubleClicked(coordinates: point)
    signal commentTypeLabelDoubleClicked(coordinates: point)
    signal commentLabelDoubleClicked

    signal heightChangedWhileEditing

    height: Math.max(_commentLabel.height, _commentLabel.editorHeight, _playButton.height)

    M.Material.background: root.backgroundColor
    M.Material.foreground: root._foregroundColor

    onHeightChanged: {
        if (ListView.isCurrentItem && _commentLabel.editorHeight > 0) {
            root.heightChangedWhileEditing();
        }
    }

    ListView.onPooled: root._isPooled = true
    ListView.onReused: root._isPooled = false

    // Background is reparented to ListView parent to sit behind the highlight rectangle.
    // This enables proper layering: backgrounds → highlight → delegate content,
    // which is essential for alternating row colors with a moving highlight animation.
    Rectangle {
        y: root.y
        width: root.width
        height: root.height
        parent: root.parent
        color: root.backgroundColor
        z: -2
        visible: !root._isPooled
    }

    MouseArea {
        acceptedButtons: Qt.LeftButton | Qt.RightButton
        anchors.fill: parent

        onPressed: event => {
            if (event.button === Qt.RightButton) {
                const coordinates = root.mapToItem(root.ListView.view, mouseX, mouseY);
                root.rightMouseButtonPressed(coordinates);
                return;
            }
            root.rowPressed();
        }

        onDoubleClicked: event => {
            if (event.button !== Qt.LeftButton) {
                return;
            }

            const coordinates = root.mapToItem(root.ListView.view, mouseX, mouseY);
            const itemPressed = _row.childAt(mouseX, mouseY);

            switch (itemPressed) {
            case _timeLabel:
                root.timeLabelDoubleClicked(coordinates);
                break;
            case _commentTypeLabel:
                root.commentTypeLabelDoubleClicked(coordinates);
                break;
            case _commentLabel:
                root.commentLabelDoubleClicked();
                break;
            }
        }
    }

    Row {
        id: _row

        width: root.width

        ToolButton {
            id: _playButton
            objectName: "playButton"

            // Painted bounds in play_arrow_rounded.svg; the rounded tip stops short of the path's x = 18.
            readonly property real arrowPaintedLeft: 8
            readonly property real arrowPaintedRight: 17.181

            readonly property real whitespaceTowardsTime: (width - icon.width) / 2 + (mirrored ? arrowPaintedLeft : icon.width - arrowPaintedRight)

            focusPolicy: Qt.NoFocus
            icon.source: MpvqcIcons.playArrow

            onPressed: root.playButtonPressed()
        }

        Label {
            id: _timeLabel
            objectName: "timeLabel"

            readonly property real paddingTowardsPlayButton: 2 * root.horizontalItemPadding - _playButton.whitespaceTowardsTime

            text: MpvqcTableUtility.formatTime(root.time)
            horizontalAlignment: Text.AlignHCenter

            width: MpvqcLabelWidthCalculator.timeLabelWidth + leftPadding + rightPadding
            height: root.height

            leftPadding: LayoutMirroring.enabled ? root.horizontalItemPadding : paddingTowardsPlayButton
            rightPadding: LayoutMirroring.enabled ? paddingTowardsPlayButton : root.horizontalItemPadding
            topPadding: root.verticalItemPadding
            bottomPadding: root.verticalItemPadding
        }

        Label {
            id: _commentTypeLabel
            objectName: "commentTypeLabel"

            text: qsTranslate("CommentTypes", root.commentType)
            textFormat: Text.PlainText
            horizontalAlignment: Text.AlignLeft
            elide: Text.ElideRight

            width: Math.min(MpvqcLabelWidthCalculator.commentTypesLabelWidth + leftPadding + rightPadding, root.width / 3)
            height: root.height

            leftPadding: root.horizontalItemPadding
            rightPadding: root.horizontalItemPadding
            topPadding: root.verticalItemPadding
            bottomPadding: root.verticalItemPadding
        }

        Label {
            id: _commentLabel
            objectName: "commentLabel"

            // Set by MpvqcEditCommentPopup via Binding while the inline editor is open; -1 otherwise.
            property int editorHeight: -1

            text: `<span style="white-space: pre-wrap">${MpvqcTableUtility.highlightComment(root.comment, root.searchQuery)}</span>`
            textFormat: Text.RichText

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
            color: MpvqcAppearance.palette.background
        }
    }

    Behavior on _foregroundColor {
        ColorAnimation {
            duration: root.ListView.view.highlightMoveDuration
            easing.type: Easing.Linear
        }
    }
}

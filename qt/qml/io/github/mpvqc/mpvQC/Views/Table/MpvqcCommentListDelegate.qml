// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

import QtQuick
import QtQuick.Controls.Material

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

    readonly property color backgroundColor: MpvqcTheme.palette.rowBackground(index)
    readonly property color foregroundColor: ListView.isCurrentItem ? MpvqcTheme.palette.rowHighlightText : MpvqcTheme.palette.rowForeground(index)

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

    // Emitted when the delegate's height changes while its inline editor is
    // open. The list handles this by scrolling to keep the delegate in view if
    // needed (shrinks naturally no-op there).
    signal heightChangedWhileEditing

    height: Math.max(_commentLabel.height, _commentLabel.editorHeight, _playButton.height)

    Material.background: root.backgroundColor
    Material.foreground: root._foregroundColor

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

            focusPolicy: Qt.NoFocus
            icon.source: MpvqcIcons.playArrow

            onPressed: root.playButtonPressed()
        }

        Label {
            id: _timeLabel
            objectName: "timeLabel"

            text: MpvqcTableUtility.formatTime(root.time)
            horizontalAlignment: Text.AlignHCenter

            width: MpvqcLabelWidthCalculator.timeLabelWidth + leftPadding + rightPadding
            height: root.height

            leftPadding: LayoutMirroring.enabled ? root.horizontalItemPadding : root.horizontalItemPadding * (2 / 3)
            rightPadding: LayoutMirroring.enabled ? root.horizontalItemPadding * (2 / 3) : root.horizontalItemPadding
            topPadding: root.verticalItemPadding
            bottomPadding: root.verticalItemPadding
        }

        Label {
            id: _commentTypeLabel
            objectName: "commentTypeLabel"

            text: qsTranslate("CommentTypes", root.commentType)
            horizontalAlignment: Text.AlignLeft

            width: MpvqcLabelWidthCalculator.commentTypesLabelWidth + leftPadding + rightPadding
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

            text: root.searchQuery ? MpvqcTableUtility.highlightComment(root.comment, root.searchQuery) : root.comment
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
            color: MpvqcTheme.palette.background
        }
    }

    Behavior on _foregroundColor {
        ColorAnimation {
            duration: root.ListView.view.highlightMoveDuration
            easing.type: Easing.Linear
        }
    }
}

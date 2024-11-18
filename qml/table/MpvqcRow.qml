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
import QtQuick.Controls.Material


Item {
    id: root

    required property var mpvqcApplication
    required property bool rowSelected
    required property bool tableInEditMode
    required property string searchQuery

    required property color selectionColor
    required property color backgroundColor
    required property color selectedTextColor

    required property int index             // from model
    required property int time              // from model
    required property string commentType    // from model
    required property string comment        // from model

    readonly property var mpvqcLabelWidthCalculator: mpvqcApplication.mpvqcLabelWidthCalculator
    readonly property var mpvqcUtilityPyObject: mpvqcApplication.mpvqcUtilityPyObject

    property alias playButton: _playButton
    property alias timeLabel: _timeLabel
    property alias commentTypeLabel: _commentTypeLabel
    property alias commentLabel: _commentLabel

    property alias scrollBarWidth: _spacerScrollBar.width
    property alias scrollBarBackgroundColor: _spacerScrollBar.color

    readonly property var contextMenuFactory: Component
    {
        MpvqcRowContextMenu {
            onCopyCommentClicked: root.copyCommentClicked()

            onDeleteCommentClicked: root.deleteCommentClicked()

            onEditCommentClicked: root.startEditing()
        }
    }

    readonly property int leftAndRightPadding: 14
    readonly property int topAndBottomPadding: 13

    signal pressed()
    signal copyCommentClicked()
    signal deleteCommentClicked()
    signal playPressed()

    signal editingStarted()
    signal editingStopped()

    signal timeEdited(int newTime)
    signal commentTypeEdited(string newCommentType)
    signal commentEdited(string newComment)

    height: Math.max(_commentLabel.height, _playButton.height)

    function startEditing(): void {
        _commentLabel.startEditing()
    }

    function createContextMenu() {
        const contextMenu = contextMenuFactory.createObject(root)
        contextMenu.closed.connect(contextMenu.destroy)
        return contextMenu
    }

    function toClipboardContent(): string {
        const time = mpvqcUtilityPyObject.formatTimeToStringLong(root.time)
        const type = qsTranslate("CommentTypes", commentType)
        return `[${time}] [${type}] ${comment}`.trim()
    }

    Rectangle {
        y: root.y
        width: root.width
        height: root.height
        parent: root.parent
        color: root.backgroundColor
        z: -2
    }

    MouseArea {
        anchors.fill: parent
        enabled: !root.rowSelected
        z: -1

        onPressed: root.pressed()
    }

    MouseArea {
        anchors.fill: parent
        enabled: !root.tableInEditMode
        acceptedButtons: Qt.RightButton
        z: -1

        onPressed: {
            root.pressed()

            const mirrored = LayoutMirroring.enabled
            const contextMenu = root.createContextMenu()
            contextMenu.transformOrigin = mirrored ? Popup.TopRight : Popup.TopLeft
            contextMenu.x = mirrored ? mouseX - contextMenu.width : mouseX
            contextMenu.y = mouseY
            contextMenu.open()
        }
    }

    Row {
        width: root.width

        MpvqcRowPlayButton {
            id: _playButton

            tableInEditMode: root.tableInEditMode

            onButtonPressed: root.pressed()

            onPlayPressed: root.playPressed()
        }

        MpvqcRowTimeLabel {
            id: _timeLabel

            width: root.mpvqcLabelWidthCalculator.timeLabelWidth + leftPadding + rightPadding
            height: root.height
            leftPadding: LayoutMirroring.enabled ? root.leftAndRightPadding : root.leftAndRightPadding * (2 / 3)
            rightPadding: LayoutMirroring.enabled ? root.leftAndRightPadding * (2 / 3) : root.leftAndRightPadding
            topPadding: root.topAndBottomPadding
            bottomPadding: root.topAndBottomPadding

            mpvqcApplication: root.mpvqcApplication
            time: root.time
            rowSelected: root.rowSelected
            tableInEditMode: root.tableInEditMode

            onEdited: (newTime) => root.timeEdited(newTime)

            onEditingStarted: root.editingStarted()

            onEditingStopped: root.editingStopped()
        }

        MpvqcRowCommentTypeLabel {
            id: _commentTypeLabel

            width: root.mpvqcLabelWidthCalculator.commentTypesLabelWidth + leftPadding + rightPadding
            height: root.height
            leftPadding: root.leftAndRightPadding
            rightPadding: root.leftAndRightPadding
            topPadding: root.topAndBottomPadding
            bottomPadding: root.topAndBottomPadding

            mpvqcApplication: root.mpvqcApplication
            commentType: root.commentType
            rowSelected: root.rowSelected
            tableInEditMode: root.tableInEditMode

            onEdited: (newCommentType) => root.commentTypeEdited(newCommentType)

            onEditingStarted: root.editingStarted()

            onEditingStopped: root.editingStopped()
        }

        MpvqcRowCommentLabel {
            id: _commentLabel

            width: root.width
                - _playButton.width
                - _timeLabel.width
                - _commentTypeLabel.width
                - _spacerScrollBar.width
            leftPadding: root.leftAndRightPadding
            rightPadding: root.leftAndRightPadding
            topPadding: root.topAndBottomPadding
            bottomPadding: root.topAndBottomPadding

            mpvqcApplication: root.mpvqcApplication
            comment: root.comment
            searchQuery: root.searchQuery
            rowSelected: root.rowSelected
            tableInEditMode: root.tableInEditMode
            backgroundColor: root.backgroundColor
            selectionColor: root.selectionColor
            selectedTextColor: root.selectedTextColor

            onEdited: (newComment) => root.commentEdited(newComment)

            onEditingStarted: root.editingStarted()

            onEditingStopped: root.editingStopped()
        }

        Rectangle {
            id: _spacerScrollBar
            height: root.height
        }
    }

}

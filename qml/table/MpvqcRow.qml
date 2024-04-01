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


Rectangle {
    id: root

    required property var mpvqcApplication
    required property bool rowSelected
    required property bool tableInEditMode
    required property int index             // from model
    required property int time              // from model
    required property string commentType    // from model
    required property string comment        // from model
    required property string searchQuery

    readonly property var mpvqcLabelWidthCalculator: mpvqcApplication.mpvqcLabelWidthCalculator
    readonly property var mpvqcUtilityPyObject: mpvqcApplication.mpvqcUtilityPyObject

    readonly property var backgroundColorSelected: Material.primary
    readonly property var backgroundColorUnselected: Material.background
    readonly property var backgroundColorUnselectedAlt: Material.theme === Material.Dark
        ? Qt.lighter(Material.background, 1.30)
        : Qt.darker(Material.background, 1.10)
    readonly property var backgroundColorUnselectedActive: index % 2 === 1
        ? backgroundColorUnselected
        : backgroundColorUnselectedAlt

    property alias widthScrollBar: _spacerScrollBar.width
    property alias playButton: _playButton
    property alias timeLabel: _timeLabel
    property alias commentTypeLabel: _commentTypeLabel
    property alias commentLabel: _commentLabel
    property alias moreButton: _moreButton

    readonly property var contextMenuFactory: Component
    {
        MpvqcMenuMore {
            onCopyCommentClicked: root.copyCommentClicked()

            onDeleteCommentClicked: root.deleteCommentClicked()

            onEditCommentClicked: root.startEditing()
        }
    }

    readonly property int leftAndRightPadding: 14
    readonly property int topAndBottomPadding: 13

    signal clicked()
    signal copyCommentClicked()
    signal deleteCommentClicked()
    signal playClicked()

    signal upPressed()
    signal downPressed()

    signal editingStarted()
    signal editingStopped()

    signal timeEdited(int newTime)
    signal commentTypeEdited(string newCommentType)
    signal commentEdited(string newComment)

    height: Math.max(_commentLabel.height, _playButton.height)

    color: rowSelected ? backgroundColorSelected : backgroundColorUnselectedActive

    function startEditing(): void {
        _commentLabel.startEditing()
    }

    function createContextMenu(): Component {
        const contextMenu = contextMenuFactory.createObject(root)
        contextMenu.closed.connect(contextMenu.destroy)
        return contextMenu
    }

    function toClipboardContent(): string {
        const time = mpvqcUtilityPyObject.formatTimeToStringLong(root.time)
        const type = qsTranslate("CommentTypes", commentType)
        return `[${time}] [${type}] ${comment}`.trim()
    }

    MouseArea {
        anchors.fill: parent
        enabled: !rowSelected
        z: -1

        onClicked: root.clicked()
    }

    MouseArea {
        anchors.fill: parent
        enabled: !root.tableInEditMode
        acceptedButtons: Qt.RightButton
        z: -1

        onClicked: {
            root.clicked()

            const contextMenu = root.createContextMenu()
            const pos = root.mapFromGlobal(root.mpvqcUtilityPyObject.cursorPosition)
            contextMenu.x = LayoutMirroring.enabled ? pos.x - contextMenu.width : pos.x
            contextMenu.y = pos.y
            contextMenu.open()
        }
    }

    Row {
        width: root.width

        MpvqcRowPlayButton {
            id: _playButton

            tableInEditMode: root.tableInEditMode

            onButtonClicked: root.clicked()

            onPlayClicked: root.playClicked()
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
                - _moreButton.width
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
            backgroundColor: root.backgroundColorUnselectedActive

            onEdited: (newComment) => root.commentEdited(newComment)

            onEditingStarted: root.editingStarted()

            onEditingStopped: root.editingStopped()
        }

        ToolButton {
            id: _moreButton

            readonly property int additionalMenuPadding: 7

            width: _playButton.width
            visible: root.rowSelected
            focusPolicy: Qt.NoFocus
            icon.source: "qrc:/data/icons/more_vert_black_24dp.svg"
            icon.width: 18
            icon.height: 18

            function _grabFocus(): void {
                focus = true
            }

            function _openMenu(): void {
                const contextMenu = root.createContextMenu()
                contextMenu.x = mirrored ? additionalMenuPadding : x + _moreButton.width - contextMenu.width - additionalMenuPadding
                contextMenu.y = additionalMenuPadding
                contextMenu.transformOrigin = mirrored ? Popup.TopLeft : Popup.TopRight
                contextMenu.open()
            }

            onClicked: {
                if (root.tableInEditMode) {
                    _moreButton._grabFocus()
                } else {
                    _moreButton._openMenu()
                }
            }
        }

        Rectangle {
            height: root.height
            width: _playButton.width
            visible: !root.rowSelected
            color: 'transparent'
        }

        Rectangle {
            id: _spacerScrollBar
            height: root.height
            width: root.widthScrollBar
            color: Material.background
        }
    }

}

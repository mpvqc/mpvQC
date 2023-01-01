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

    readonly property var mpvqcWidthCalculatorCommentTypes: mpvqcApplication.mpvqcWidthCalculatorCommentTypes
    readonly property var mpvqcTimeFormatUtils: mpvqcApplication.mpvqcTimeFormatUtils

    property alias widthScrollBar: _spacerScrollBar.width
    property alias playButton: _playButton
    property alias timeLabel: _timeLabel
    property alias commentTypeLabel: _commentTypeLabel
    property alias commentLabel: _commentLabel
    property alias moreButton: _moreButton

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

    height: Math.max(40, _playButton.height)

    color: {
        if (rowSelected) {
            return Material.accent
        } if (index % 2 === 0) {
            return 'transparent'
        } else if (Material.theme === Material.Dark) {
            return Qt.lighter(Material.background, 1.12)
        } else {
            return Qt.darker(Material.background, 1.04)
        }
    }

    function startEditing(): void {
        _commentLabel.startEditing()
    }

    function toClipboardContent(): string {
        const time = mpvqcTimeFormatUtils.formatTimeToString(root.time)
        const type = qsTranslate("CommentTypes", commentType)
        return `[${time}] [${type}] ${comment}`.trim()
    }

    Row {
        width: root.width

        MpvqcRowPlayButton {
            id: _playButton

            anchors.verticalCenter: parent.verticalCenter
            tableInEditMode: root.tableInEditMode

            onButtonClicked: root.clicked()

            onPlayClicked: root.playClicked()
        }

        MpvqcRowTimeLabel {
            id: _timeLabel

            width: 90
            height: root.height
            mpvqcApplication: root.mpvqcApplication
            time: root.time
            rowSelected: root.rowSelected
            tableInEditMode: root.tableInEditMode

            onClicked: root.clicked()

            onEdited: (newTime) => root.timeEdited(newTime)

            onEditingStarted: root.editingStarted()

            onEditingStopped: root.editingStopped()
        }

        MpvqcRowCommentTypeLabel {
            id: _commentTypeLabel

            width: root.mpvqcWidthCalculatorCommentTypes.maxWidth
            height: root.height
            mpvqcApplication: root.mpvqcApplication
            commentType: root.commentType
            rowSelected: root.rowSelected
            tableInEditMode: root.tableInEditMode

            onClicked: root.clicked()

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
            height: root.height
            mpvqcApplication: root.mpvqcApplication
            comment: root.comment
            rowSelected: root.rowSelected
            tableInEditMode: root.tableInEditMode

            onClicked: root.clicked()

            onEdited: (newComment) => root.commentEdited(newComment)

            onEditingStarted: root.editingStarted()

            onEditingStopped: root.editingStopped()

            onUpPressed: root.upPressed()

            onDownPressed: root.downPressed()
        }

        MpvqcRowMoreButton {
            id: _moreButton

            width: visible ? implicitWidth : 0
            visible: root.rowSelected
            anchors.verticalCenter: parent.verticalCenter
            tableInEditMode: root.tableInEditMode

            onCopyCommentClicked: root.copyCommentClicked()

            onDeleteCommentClicked: root.deleteCommentClicked()
        }

        Rectangle {
            id: _spacerScrollBar
            height: root.height
            color: Material.background
        }

    }

}

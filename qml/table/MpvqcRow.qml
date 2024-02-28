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
    readonly property var mpvqcTimeFormatUtils: mpvqcApplication.mpvqcTimeFormatUtils

    readonly property var backgroundColorSelected: Material.primary
    readonly property var backgroundColorUnselected: Material.background
    readonly property var backgroundColorUnselectedAlt: Material.theme === Material.Dark
        ? Qt.lighter(Material.background, 1.12)
        : Qt.darker(Material.background, 1.04)
    readonly property var backgroundColorUnselectedActive: index % 2 === 1
        ? backgroundColorUnselected
        : backgroundColorUnselectedAlt

    property alias widthScrollBar: _spacerScrollBar.width
    property alias playButton: _playButton
    property alias timeLabel: _timeLabel
    property alias commentTypeLabel: _commentTypeLabel
    property alias commentLabel: _commentLabel
    property alias moreButton: _moreButton

    property int labelPadding: 14

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

    color: rowSelected ? backgroundColorSelected : backgroundColorUnselectedActive

    function startEditing(): void {
        _commentLabel.startEditing()
    }

    function toClipboardContent(): string {
        const time = mpvqcTimeFormatUtils.formatTimeToStringLong(root.time)
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

            width: root.mpvqcLabelWidthCalculator.timeLabelWidth + leftPadding + rightPadding
            height: root.height
            leftPadding: LayoutMirroring.enabled ? root.labelPadding : root.labelPadding * (2/3)
            rightPadding: LayoutMirroring.enabled ? root.labelPadding * (2/3) : root.labelPadding

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

            width: root.mpvqcLabelWidthCalculator.commentTypesLabelWidth + leftPadding + rightPadding
            height: root.height
            leftPadding: root.labelPadding
            rightPadding: root.labelPadding

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
            leftPadding: root.labelPadding
            rightPadding: root.labelPadding

            mpvqcApplication: root.mpvqcApplication
            comment: root.comment
            searchQuery: root.searchQuery
            rowSelected: root.rowSelected
            tableInEditMode: root.tableInEditMode
            backgroundColor: root.backgroundColorUnselectedActive

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

            onEditCommentClicked: root.startEditing()
        }

        Rectangle {
            id: _spacerScrollBar
            height: root.height
            color: Material.background
        }

    }

}

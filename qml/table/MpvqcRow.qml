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

    function toClipboardContent(): string {
        const time = mpvqcUtilityPyObject.formatTimeToStringLong(root.time)
        const type = qsTranslate("CommentTypes", commentType)
        return `[${time}] [${type}] ${comment}`.trim()
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

        MpvqcRowMoreButton {
            id: _moreButton

            width: _playButton.width
            visible: root.rowSelected
            tableInEditMode: root.tableInEditMode

            onCopyCommentClicked: root.copyCommentClicked()

            onDeleteCommentClicked: root.deleteCommentClicked()

            onEditCommentClicked: root.startEditing()
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

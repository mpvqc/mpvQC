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
import QtQuick.Controls
import components
import helpers


Rectangle {
    id: row
    width: parent ? parent.width : 0
    height: playButton.height

    property var modelItem
    property bool currentlySelected
    property bool listViewCurrentlyBeingEdited

    signal clicked()
    signal playClicked()
    signal deleteClicked()
    signal timeEdited(int time)
    signal commentTypeEdited(string commentType)
    signal commentEdited(string comment)
    signal editingStarted()
    signal editingStopped()

    Row {
        width: parent.width

        MpvqcDisplayPlayButton {
            id: playButton

            onClicked: {
                row.triggerClicked()
                row.triggerPlayClicked()
            }
        }

        MpvqcDisplayTimeLabel {
            id: timeLabel
            width: 100
            height: row.height
            time: modelItem.time

            onClicked: {
                if (row.currentlySelected && listViewCurrentlyBeingEdited) {
                    timeLabel.grabFocus()
                } else if (row.currentlySelected) {
                    timeLabel.startEditing()
                } else {
                    row.triggerClicked()
                }
            }

            onEdited: (time) => {
                row.triggerTimeEdited(time)
            }

            onEditingStarted: {
                row.triggerEditingStarted()
            }

            onEditingStopped: {
                row.triggerEditingStopped()
            }
        }

        MpvqcDisplayCommentTypeLabel {
            id: typeLabel
            width: MpvqcCommentTypeWidthCalculator.width
            height: row.height
            commentType: modelItem.commentType

            onClicked: {
                if (row.currentlySelected && listViewCurrentlyBeingEdited) {
                    typeLabel.grabFocus()
                } else if (row.currentlySelected) {
                    typeLabel.startEditing()
                } else {
                    row.triggerClicked()
                }
            }

            onEdited: (commentType) => {
                row.triggerCommentTypeEdited(commentType)
            }

            onEditingStarted: {
                row.triggerEditingStarted()
            }

            onEditingStopped: {
                row.triggerEditingStopped()
            }
        }

        MpvqcEditableLabel {
            id: commentLabel
            width: row.width
                    - playButton.width
                    - timeLabel.width
                    - typeLabel.width
                    - (moreButton.visible ? moreButton.width : 0)
                    - spacerScrollBar.width
            height: row.height
            text: modelItem.comment

            onClicked: {
                if (row.currentlySelected && listViewCurrentlyBeingEdited) {
                    commentLabel.grabFocus()
                } else if (row.currentlySelected) {
                    commentLabel.startEditing()
                } else {
                    row.triggerClicked()
                }
            }

            onEdited: (comment) => {
                row.triggerCommentEdited(comment)
            }

            onEditingStarted: {
                row.triggerEditingStarted()
            }

            onEditingStopped: {
                row.triggerEditingStopped()
            }
        }

        MpvqcDisplayMoreButton {
            id: moreButton
            visible: row.currentlySelected

            onClicked: {
                row.triggerClicked()
                row.triggerDeleteClicked()
            }
        }

        Item {
            id: spacerScrollBar
            width: 16
            height: row.height
        }

    }

    function startEditing() {
        commentLabel.startEditing()
    }

    function triggerClicked() {
        if (!row.currentlySelected) {
            row.clicked()
        }
    }

    function triggerPlayClicked() {
        row.playClicked()
    }

    function triggerDeleteClicked() {
        row.deleteClicked()
    }

    function triggerTimeEdited(time) {
        row.timeEdited(time)
    }

    function triggerCommentEdited(comment) {
        row.commentEdited(comment)
    }

    function triggerCommentTypeEdited(commentType) {
        row.commentTypeEdited(commentType)
    }

    function triggerEditingStarted() {
        row.editingStarted()
    }

    function triggerEditingStopped() {
        row.editingStopped()
    }

}

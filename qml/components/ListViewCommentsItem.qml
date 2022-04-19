/*
mpvQC

Copyright (C) 2022 mpvQC developers

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/


import QtQuick
import QtQuick.Controls
import helpers
import pyobjects


Rectangle {
    id: row

    property var modelItem
    property bool selected

    signal clicked()
    signal deleteClicked()
    signal typeEdited(string type)
    signal commentEdited(string comment)

    width: parent ? parent.width : 0
    height: playButton.height

    Row {
        width: parent.width

        ButtonPlay {
            id: playButton

            onClicked: {
                row.triggerClicked()
                eventRegistry.produce(eventRegistry.EventJumpToVideoPosition, modelItem.timeInt)
            }
        }

        LabelTime {
            id: timeLabel
            time: modelItem.timeStr
            rowSelected: row.selected
            width: 100
            height: row.height

            onClicked: { row.triggerClicked() }
        }

        LabelType {
            id: typeLabel
            type: modelItem.type
            width: CommentTypeWidthCalculator.width
            height: row.height
            rowSelected: row.selected

            onClicked: { row.triggerClicked() }

            onEdited: (type) => { row.triggerCommentTypeEdited(type) }
        }

        LabelComment {
            id: commentLabel
            comment: modelItem.comment
            rowSelected: row.selected
            height: row.height
            width: row.width
                    - playButton.width
                    - timeLabel.width
                    - typeLabel.width
                    - moreButton.width
                    - spacerScrollBar.width

            onClicked: { row.triggerClicked() }

            onEdited: (comment) => { row.triggerCommentEdited(comment) }
        }

        ButtonMore {
            id: moreButton

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
        if (!row.selected) { row.clicked() }
    }

    function triggerDeleteClicked() {
        row.deleteClicked()
    }

    function triggerCommentEdited(comment) {
        row.commentEdited(comment)
    }

    function triggerCommentTypeEdited(type) {
        row.typeEdited(type)
    }

}

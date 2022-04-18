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

    signal clicked()
    signal deleteClicked()
    signal commentEdited(string comment)

    width: parent ? parent.width : 0
    height: playButton.height

    Row {
        width: parent.width

        ButtonPlay {
            id: playButton

            onClicked: {
                row.triggerClickSignal()
                eventRegistry.produce(eventRegistry.EventJumpToVideoPosition, modelItem.timeInt)
            }
        }

        LabelTime {
            id: timeLabel
            time: modelItem.timeStr
            width: 100
            height: row.height
        }

        LabelType {
            id: typeLabel
            text: qsTranslate("CommentTypes", modelItem.type)
            width: CommentTypeWidthCalculator.width
            height: row.height
        }

        LabelComment {
            id: commentLabel
            comment: modelItem.comment
            height: row.height
            width: row.width
                    - playButton.width
                    - timeLabel.width
                    - typeLabel.width
                    - moreButton.width
                    - spacerScrollBar.width

            onEdited: (comment) => {
                row.triggerCommentEditedSignal(comment)
            }
        }

        ButtonMore {
            id: moreButton

            onClicked: {
                row.triggerClickSignal()
                row.triggerDeleteSignal()
            }
        }

        Item {
            id: spacerScrollBar
            width: 16
            height: row.height
        }

    }

    MouseArea {
        anchors.fill: parent
        z: -1 // let the other items handle events first

        onClicked: (event) => { row.triggerClickSignal() }
    }

    function startEditing() {
        commentLabel.startEditing()
    }

    function triggerClickSignal() {
        row.clicked()
    }

    function triggerDeleteSignal() {
        row.deleteClicked()
    }

    function triggerCommentEditedSignal(comment) {
        row.commentEdited(comment)
    }

}

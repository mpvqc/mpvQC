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
    id: item
    width: parent ? parent.width : 0
    height: playButton.height

    property var modelItem
    property bool selected

    signal clicked()
    signal playClicked()
    signal deleteClicked()
    signal commentTypeEdited(string commentType)
    signal commentEdited(string comment)

    Row {
        width: parent.width

        MpvqcDisplayPlayButton {
            id: playButton

            onClicked: {
                item.triggerClicked()
                item.triggerPlayClicked()
            }
        }

        MpvqcDisplayTimeLabel {
            id: timeLabel
            time: modelItem.timeStr
            itemSelected: item.selected
            width: 100
            height: item.height

            onClicked: {
                item.triggerClicked()
            }
        }

        MpvqcDisplayCommentTypeLabel {
            id: typeLabel
            commentType: modelItem.commentType
            width: MpvqcCommentTypeWidthCalculator.width
            height: item.height
            itemSelected: item.selected

            onClicked: {
                item.triggerClicked()
            }

            onEdited: (commentType) => {
                item.triggerCommentTypeEdited(commentType)
            }
        }

        MpvqcDisplayCommentLabel {
            id: commentLabel
            comment: modelItem.comment
            itemSelected: item.selected
            height: item.height
            width: item.width
                    - playButton.width
                    - timeLabel.width
                    - typeLabel.width
                    - moreButton.width
                    - spacerScrollBar.width

            onClicked: {
                item.triggerClicked()
            }

            onEdited: (comment) => {
                item.triggerCommentEdited(comment)
            }
        }

        MpvqcDisplayMoreButton {
            id: moreButton

            onClicked: {
                item.triggerClicked()
                item.triggerDeleteClicked()
            }
        }

        Item {
            id: spacerScrollBar
            width: 16
            height: item.height
        }

    }

    function startEditing() {
        commentLabel.startEditing()
    }

    function triggerClicked() {
        if (!item.selected) { 
            item.clicked()
        }
    }

    function triggerPlayClicked() {
        item.playClicked()
    }

    function triggerDeleteClicked() {
        item.deleteClicked()
    }

    function triggerCommentEdited(comment) {
        item.commentEdited(comment)
    }

    function triggerCommentTypeEdited(commentType) {
        item.commentTypeEdited(commentType)
    }

}

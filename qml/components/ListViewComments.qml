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
import pyobjects


ListView {

    id: listView

    clip: true
    reuseItems: true
    boundsBehavior: Flickable.StopAtBounds
    model: CommentModelPyObject {}
    ScrollBar.vertical: ScrollBar {}
    delegate: Component {

        Rectangle {

            width: listView.width
            height: content.height
            color: "transparent"
//            color: ListView.isCurrentItem ? Material.accent : "transparent"

            ListViewItem {

                id: content

                index: model.index

                timeInt: model.timeInt
                timeStr: model.timeStr
                type: model.type
                comment: model.comment

            }

        }

    }

    Component.onCompleted: {
        eventRegistry.register(
            eventRegistry.EventAddNewComment, commentType => listView.onAddNewCommentEvent(commentType)
        )
    }

    function onAddNewCommentEvent(commentType) {
        listView.model.add_comment(commentType)
    }

}


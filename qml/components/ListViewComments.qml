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
    highlightMoveDuration: 0
    highlightMoveVelocity: -1
    model: CommentModelPyObject {}
    ScrollBar.vertical: ScrollBar {}

    delegate: ListViewCommentsItem {
        modelItem: model
        color: ListView.isCurrentItem ? Material.accent : "transparent"

        onClicked: {
            listView.currentIndex = model.index
        }

        onDeleteClicked: {
            listView.model.remove_row(model.index)
        }

        onCommentEdited: (comment) => {
            listView.model.update_comment(model.index, comment)
        }
    }

    Component.onCompleted: {
        listView.model.row_added.connect(listView.onAfterNewRowAdded)

        eventRegistry.register(
            eventRegistry.EventAddNewRow, (commentType) => listView.onAddNewRowEvent(commentType)
        )
    }

    function onAddNewRowEvent(commentType) {
        listView.model.add_row(commentType)
    }

    function onAfterNewRowAdded(rowIndex) {
        listView.currentIndex = rowIndex
        listView.itemAtIndex(rowIndex).startEditing()
    }

}


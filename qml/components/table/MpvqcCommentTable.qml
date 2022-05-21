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
import QtQuick.Layouts
import handlers
import pyobjects

FocusScope {
    id: container

    ColumnLayout {
        anchors.fill: parent
        spacing: 0

        ListView {
            id: listView
            clip: true
            focus: true
            reuseItems: true
            boundsBehavior: Flickable.StopAtBounds
            highlightMoveDuration: 0
            highlightMoveVelocity: -1
            model: CommentModelPyObject {}
            ScrollBar.vertical: ScrollBar {}
            Layout.fillWidth: true
            Layout.alignment: Qt.AlignTop
            Layout.preferredHeight: {
                if (listView.count === 0)
                    return 0
                if (itemHeight === 0)
                    itemHeight = listView.itemAt(0, 0).height
                return Math.min(container.height, listView.count * itemHeight)
            }

            property int itemHeight: 0
            property bool currentlyBeingEdited

            delegate: MpvqcCommentRow {
                modelItem: model
                currentlySelected: listView.currentIndex === model.index
                listViewCurrentlyBeingEdited: listView.currentlyBeingEdited
                color: ListView.isCurrentItem ? Material.accent : "transparent"

                onClicked: {
                    listView.selectRow(model.index)
                }

                onPlayClicked: {
                    listView.requestPlay(model.time)
                }

                onEditingStarted: {
                    listView.currentlyBeingEdited = true
                }

                onEditingStopped: {
                    listView.currentlyBeingEdited = false
                }

                onTimeEdited: (time) => {
                    listView.updateTime(model.index, time)
                }

                onCommentTypeEdited: (commentType) => {
                    listView.updateCommentType(model.index, commentType)
                }

                onCommentEdited: (comment) => {
                    listView.updateComment(model.index, comment)
                }

                onDeleteClicked: {
                    listView.removeRow(model.index)
                }
            }

            Component.onCompleted: {
                listView.model.row_added.connect(listView.selectRow)
                listView.model.row_added.connect(listView.startEditing)
                listView.model.time_updated.connect(listView.selectRow)
                listView.forceActiveFocus()
            }

            function addRow(commentType) {
                listView.model.add_row(commentType)
            }

            function selectRow(index) {
                listView.currentIndex = index
            }

            function startEditing() {
                const item = listView.itemAtIndex(listView.currentIndex)
                if (item) {
                    item.startEditing()
                }
            }

            function requestPlay(time) {
                eventRegistry.produce(eventRegistry.EventJumpToVideoPosition, time)
            }

            function updateTime(index, time) {
                listView.model.update_time(index, time)
            }

            function updateCommentType(index, commentType) {
                listView.model.update_comment_type(index, commentType)
            }

            function updateComment(index, comment) {
                listView.model.update_comment(index, comment)
            }

            function removeRow(index) {
                listView.model.remove_row(model.index)
            }
        }

        Item {
            Layout.fillHeight: true
            Layout.fillWidth: true

            TapHandler {
                onTapped: {
                    focusListView()
                }
            }
        }
    }

    Component.onCompleted: {
        eventRegistry.subscribe(eventRegistry.EventAddNewRow, listView.addRow)
        eventRegistry.subscribe(eventRegistry.EventFocusTable, focusListView)
        eventRegistry.subscribe(eventRegistry.EventEditCurrentlySelectedComment, listView.startEditing)
        qcManager.commentModel = listView.model
    }

    function focusListView() {
        utils.clearActiveFocus()
        listView.forceActiveFocus()
    }

    MpvqcKeyEventHandler { id: handler }
    Keys.onPressed: (event) => handler.handle(event)

}

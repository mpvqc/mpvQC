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
import QtQuick.Controls.Material

import dialogs


ListView {
    id: root

    required property var mpvqcApplication

    readonly property var mpv: mpvqcApplication.mpvqcMpvPlayerPyObject
    readonly property var mpvqcClipboardPyObject: mpvqcApplication.mpvqcClipboardPyObject
    readonly property var mpvqcKeyCommandGenerator: mpvqcApplication.mpvqcKeyCommandGenerator

    property bool editMode: false

    property var deleteCommentMessageBox: null
    property var deleteCommentMessageBoxFactory: Component {

        MpvqcMessageBoxDeleteComment {
            property int index

            mpvqcApplication: root.mpvqcApplication

            onAccepted: root.model.remove_row(index)
        }

    }

    signal commentsChanged()

    clip: true
    focus: true
    reuseItems: true
    interactive: !editMode
    boundsBehavior: Flickable.StopAtBounds
    highlightMoveDuration: 0
    highlightMoveVelocity: -1
    highlightResizeDuration: 0
    highlightResizeVelocity: -1

    ScrollBar.vertical: ScrollBar {
        id: _scrollBar

        readonly property var isShown: root.contentHeight > root.height
        readonly property var visibleWidth: isShown ? width : 0

        policy: isShown ? ScrollBar.AlwaysOn : ScrollBar.AlwaysOff
    }

    delegate: MpvqcRow {
        mpvqcApplication: root.mpvqcApplication
        rowSelected: root.currentIndex === index
        tableInEditMode: root.editMode
        width: parent ? parent.width : 0
        widthScrollBar: _scrollBar.visibleWidth

        onClicked: root._selectRow(index)

        onCopyCommentClicked: root._copyCurrentCommentToClipboard()

        onDeleteCommentClicked: root._requestDeleteRow(index)

        onEditingStarted: { root.editMode = true }

        onEditingStopped: { root.editMode = false }

        onPlayClicked: root.mpv.jump_to(time)

        onTimeEdited: (newTime) => root.model.update_time(index, newTime)

        onCommentTypeEdited: (newCommentType) => root.model.update_comment_type(index, newCommentType)

        onCommentEdited: (newComment) => root.model.update_comment(index, newComment)

        onUpPressed: root.decrementCurrentIndex()

        onDownPressed: root.incrementCurrentIndex()
    }

    function _selectRow(index: int): void {
        root.currentIndex = index
    }

    function _requestDeleteRow(index: int): void {
        deleteCommentMessageBox = deleteCommentMessageBoxFactory.createObject(root)
        deleteCommentMessageBox.index = index
        deleteCommentMessageBox.closed.connect(deleteCommentMessageBox.destroy)
        deleteCommentMessageBox.open()
    }

    function _copyCurrentCommentToClipboard() {
        const text = root.currentItem.toClipboardContent()
        root.mpvqcClipboardPyObject.copy_to_clipboard(text)
    }

    function startEditing(): void {
        const index = root.currentIndex
        const item = root.itemAtIndex(index)
        if (item) {
            root.positionViewAtIndex(index, ListView.Visible)
            item.startEditing()
        }
    }

    function addNewComment(commentType: string): void {
        root.model.add_row(commentType)
    }

    function clearComments(): void {
        root.model.clear_comments()
    }

    function getAllComments(): Array<MpvqcComment> {
        return root.model.comments()
    }

    function importComments(comments: Array<MpvqcComment>): void {
        root.model.import_comments(comments)
    }

    Connections {
        target: root.model

        function onNewItemAdded(index: int): void {
            root._selectRow(index)
            root.startEditing()
        }

        function onTimeUpdated(index: int): void {
            root._selectRow(index)
        }

        function onHighlightRequested(index: int): void {
            root._selectRow(index)
        }

        function onCommentsChanged(): void {
            root.commentsChanged()
        }
    }

    MpvqcTableEventHandler {
        id: _handler

        mpvqcCommentTable: root
        mpvqcApplication: root.mpvqcApplication

        onDeleteCommentPressed: root._requestDeleteRow(root.currentIndex)

        onCopyToClipboardPressed: root._copyCurrentCommentToClipboard()
    }

    Keys.onPressed: (event) => {
        if (_handler.ignore(event))  {
            return
        }
        const command = root.mpvqcKeyCommandGenerator.generateFrom(event)
        if (command) {
            root.mpv.execute(command)
        }
    }

}

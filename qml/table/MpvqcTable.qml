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
    required property string searchQuery

    readonly property var mpv: mpvqcApplication.mpvqcMpvPlayerPyObject
    readonly property var mpvqcClipboardPyObject: mpvqcApplication.mpvqcClipboardPyObject

    property bool haveComments: root.count > 0

    property bool currentlyEditing: false
    property bool currentlyFullscreen: mpvqcApplication.fullscreen

    property var deleteCommentMessageBox: null
    property var deleteCommentMessageBoxFactory: Component
    {
        MpvqcMessageBoxDeleteComment {
            property int index

            mpvqcApplication: root.mpvqcApplication

            onAccepted: root.model.remove_row(index)
        }
    }

    readonly property Timer delayEnsureVisibleTimer: Timer
    {
        interval: 0

        onTriggered: {
            root._ensureVisible()
        }
    }

    signal commentsChanged()

    clip: true
    focus: true
    reuseItems: true
    interactive: !currentlyEditing
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
        tableInEditMode: root.currentlyEditing
        width: parent ? parent.width : 0
        widthScrollBar: _scrollBar.visibleWidth
        searchQuery: root.searchQuery

        onHeightChanged: {
            if (rowSelected && tableInEditMode) {
                if (index === root.count - 1) {
                    root.delayEnsureVisibleTimer.restart()
                } else {
                    root._ensureVisible()
                }
            }
        }

        onClicked: root.selectRow(index)

        onCopyCommentClicked: root._copyCurrentCommentToClipboard()

        onDeleteCommentClicked: root._requestDeleteRow(index)

        onEditingStarted: { root.currentlyEditing = true }

        onEditingStopped: { root.currentlyEditing = false }

        onPlayClicked: root.mpv.jump_to(time)

        onTimeEdited: (newTime) => root.model.update_time(index, newTime)

        onCommentTypeEdited: (newCommentType) => root.model.update_comment_type(index, newCommentType)

        onCommentEdited: (newComment) => root.model.update_comment(index, newComment)

        MouseArea {
            anchors.fill: parent
            enabled: !rowSelected
            z: -1

            onClicked: {
                root.selectRow(index)
            }
        }
    }

    function selectRow(index: int): void {
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
            _ensureVisible()
            item.startEditing()
        }
    }

    function _ensureVisible(): void {
        root.positionViewAtIndex(root.currentIndex, ListView.Contain)
    }

    function addNewComment(commentType: string): void {
        root.model.add_row(commentType)
    }

    function _handleDeleteComment(event) {
        if (event.isAutoRepeat) {
            return
        }

        if (!root.mpvqcApplication.fullscreen && root.haveComments) {
            return root._requestDeleteRow(root.currentIndex)
        }
    }

    function _handleCPressed(event) {
        if (event.modifiers === Qt.ControlModifier) {
            if (event.isAutoRepeat) {
                return
            }

            const haveComments = root.haveComments
            const notEditing = !root.currentlyEditing
            const notFullscreen = !root.mpvqcApplication.fullscreen

            if (haveComments && notEditing && notFullscreen) {
                return root._copyCurrentCommentToClipboard()
            }
        }
        event.accepted = false
    }

    Keys.onReturnPressed: (event) => {
        if (event.isAutoRepeat) {
            return
        }

        const haveComments = root.haveComments
        const notEditing = !root.currentlyEditing
        const notFullscreen = !root.mpvqcApplication.fullscreen

        if (haveComments && notEditing && notFullscreen) {
            return root.startEditing()
        }
    }

    Keys.onPressed: (event) => {
        if (event.key === Qt.Key_Backspace) {
            return _handleDeleteComment(event)
        }
        if (event.key === Qt.Key_Delete) {
            return _handleDeleteComment(event)
        }
        if (event.key === Qt.Key_C) {
            return _handleCPressed(event)
        }

        event.accepted = false
    }

    Connections {
        target: root.model

        function onNewItemAdded(index: int): void {
            root.selectRow(index)
            root.startEditing()
        }

        function onTimeUpdated(index: int): void {
            root.selectRow(index)
        }

        function onHighlightRequested(index: int): void {
            root.selectRow(index)
        }

        function onCommentsChanged(): void {
            root.commentsChanged()
        }
    }

}

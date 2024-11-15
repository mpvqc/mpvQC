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

import dialogs


ListView {
    id: root

    required property var mpvqcApplication
    required property string searchQuery

    readonly property var mpv: mpvqcApplication.mpvqcMpvPlayerPyObject
    readonly property var mpvqcUtilityPyObject: mpvqcApplication.mpvqcUtilityPyObject
    readonly property var mpvqcTheme: mpvqcApplication.mpvqcTheme

    readonly property bool haveComments: root.count > 0
    readonly property int defaultHighlightMoveDuration: 50

    property bool currentlyEditing: false

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

    clip: true
    focus: true
    reuseItems: true
    interactive: !currentlyEditing
    boundsBehavior: Flickable.StopAtBounds
    highlightMoveDuration: defaultHighlightMoveDuration
    highlightMoveVelocity: -1
    highlightResizeDuration: 50
    highlightResizeVelocity: -1

    highlight: Rectangle {
        width: parent ? parent.width - _scrollBar.visibleWidth : 0
        height: parent?.height ?? 0
        color: root.mpvqcTheme.rowHighlight
    }

    ScrollBar.vertical: ScrollBar {
        id: _scrollBar

        readonly property var isShown: root.contentHeight > root.height
        readonly property var visibleWidth: isShown ? width : 0

        policy: isShown ? ScrollBar.AlwaysOn : ScrollBar.AlwaysOff
    }

    delegate: MpvqcRow {
        readonly property bool isOdd: index % 2 === 1

        backgroundColor: root.mpvqcTheme.getBackground(isOdd)
        selectionColor: root.mpvqcTheme.rowHighlight
        selectedTextColor: root.mpvqcTheme.rowHighlightText

        Material.background: backgroundColor
        Material.foreground: rowSelected ? root.mpvqcTheme.rowHighlightText : root.mpvqcTheme.foreground

        mpvqcApplication: root.mpvqcApplication
        rowSelected: root.currentIndex === index
        tableInEditMode: root.currentlyEditing
        width: parent ? root.width : 0
        searchQuery: root.searchQuery

        scrollBarWidth: _scrollBar.visibleWidth
        scrollBarBackgroundColor: root.mpvqcTheme.background

        onHeightChanged: {
            if (rowSelected && tableInEditMode) {
                if (index === root.count - 1) {
                    root.delayEnsureVisibleTimer.restart()
                } else {
                    root._ensureVisible()
                }
            }
        }

        onPressed: root.selectRow(index)

        onCopyCommentClicked: root._copyCurrentCommentToClipboard()

        onDeleteCommentClicked: root._requestDeleteRow()

        onEditingStarted: { root.currentlyEditing = true }

        onEditingStopped: { root.currentlyEditing = false }

        onPlayPressed: root.mpv.jump_to(time)

        onTimeEdited: (newTime) => root.model.update_time(index, newTime)

        onCommentTypeEdited: (newCommentType) => root.model.update_comment_type(index, newCommentType)

        onCommentEdited: (newComment) => root.model.update_comment(index, newComment)
    }

    function selectRow(index: int): void {
        root.currentIndex = index
    }

    function _requestDeleteRow(): void {
        deleteCommentMessageBox = deleteCommentMessageBoxFactory.createObject(root)
        deleteCommentMessageBox.index = root.currentIndex
        deleteCommentMessageBox.closed.connect(deleteCommentMessageBox.destroy)
        deleteCommentMessageBox.open()
    }

    function _copyCurrentCommentToClipboard() {
        const text = root.currentItem.toClipboardContent()
        root.mpvqcUtilityPyObject.copyToClipboard(text)
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
            return root._requestDeleteRow()
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

    function _handleZPressed(event) {
        const ctrlPressed = event.modifiers & Qt.ControlModifier
        const shiftPressed = event.modifiers & Qt.ShiftModifier

        if (ctrlPressed && !event.isAutoRepeat) {
            if (shiftPressed) {
                root.model.redo()
            } else {
                root.model.undo()
            }
            return
        }
        event.accepted = false
    }

    function disableMovingHighlightRectangle(): void {
        root.highlightMoveDuration = 0
    }

    function enableMovingHighlightRectangle(): void {
        root.highlightMoveDuration = root.defaultHighlightMoveDuration
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

    Keys.onPressed: event => {
        switch (event.key) {
            case Qt.Key_Delete:
            case Qt.Key_Backspace:
                return _handleDeleteComment(event)
            case Qt.Key_C:
                return _handleCPressed(event)
            case Qt.Key_Z:
                return _handleZPressed(event)
            default:
                event.accepted = false
        }
    }

    Connections {
        target: root.model

        function onCommentsImported(index: int): void {
            _quickSelect(index)
        }

        function onCommentsImportedUndone(index: int): void {
            _quickSelect(index)
        }

        function onCommentsClearedUndone(): void {
            const lastIndex = root.count - 1
            _quickSelect(lastIndex)
        }

        function onNewCommentAddedInitially(index: int): void {
            _quickSelect(index)
            root.startEditing()
        }

        function onNewCommentAddedUndone(index: int): void {
            _quickSelect(index)
        }

        function onNewCommentAddedRedone(index: int): void {
            _quickSelect(index)
        }

        function onCommentRemovedUndone(index: int): void {
            _quickSelect(index)
        }

        function onTimeUpdatedInitially(index: int): void {
            root.selectRow(index)
        }

        function onTimeUpdatedUndone(index: int): void {
            _quickSelect(index)
        }

        function onTimeUpdatedRedone(index: int): void {
            _quickSelect(index)
        }

        function onCommentTypeUpdated(index: int) {
            _quickSelect(index)
        }

        function onCommentTypeUpdatedUndone(index: int) {
            _quickSelect(index)
        }

        function onCommentUpdated(index: int) {
            _quickSelect(index)
        }

        function onCommentUpdatedUndone(index: int) {
            _quickSelect(index)
        }

        function _quickSelect(index: int): void {
            root.disableMovingHighlightRectangle()
            root.selectRow(index)
            root.enableMovingHighlightRectangle()
        }
    }

}

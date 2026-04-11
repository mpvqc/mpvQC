// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls.Material

import "../../utility"

ListView {
    id: root

    required property var viewModel

    readonly property bool hasComments: count > 0
    readonly property bool isCurrentlyEditing: _editLoader.active
    readonly property bool isNotCurrentlyEditing: !isCurrentlyEditing
    readonly property bool isHandleKeyEvents: root.isNotCurrentlyEditing && !_contextMenuLoader.active && !_messageBoxLoader.active

    readonly property alias editLoader: _editLoader // for tests
    readonly property alias contextMenuLoader: _contextMenuLoader // for tests
    readonly property alias messageBoxLoader: _messageBoxLoader // for tests
    readonly property alias searchBoxLoader: _searchBoxLoader // for tests

    readonly property string searchQuery: _searchBoxLoader.searchQuery

    model: viewModel.model

    clip: true
    focus: true
    reuseItems: true

    interactive: isNotCurrentlyEditing
    boundsBehavior: Flickable.StopAtBounds

    highlightMoveDuration: 50
    highlightMoveVelocity: -1
    highlightResizeDuration: isCurrentlyEditing ? 0 : 50
    highlightResizeVelocity: -1

    highlight: Rectangle {
        width: parent ? parent.width - _scrollBar.visibleWidth : 0
        height: parent?.height ?? 0
        color: MpvqcTheme.rowHighlight
    }

    ScrollBar.vertical: ScrollBar {
        id: _scrollBar

        readonly property bool isShown: root.contentHeight > root.height
        readonly property int visibleWidth: isShown ? width : 0

        policy: isShown ? ScrollBar.AlwaysOn : ScrollBar.AlwaysOff
    }

    delegate: MpvqcCommentListDelegate {
        width: parent ? root.width : 0
        scrollBarWidth: _scrollBar.visibleWidth

        listView: root
        searchQuery: root.searchQuery

        onPlayButtonPressed: {
            root.viewModel.select(index);
            if (root.isNotCurrentlyEditing) {
                root.viewModel.jumpToTime(time);
            }
        }

        onRowPressed: {
            root.viewModel.select(index);
        }

        onTimeLabelDoubleClicked: coordinates => {
            root.viewModel.pauseVideo();
            root.viewModel.jumpToTime(time);
            root.viewModel.startEditingTime(index, time, coordinates);
        }

        onCommentTypeLabelDoubleClicked: coordinates => {
            root.viewModel.startEditingCommentType(index, commentType, coordinates);
        }

        onCommentLabelDoubleClicked: {
            root.viewModel.startEditingComment(index);
        }

        onRightMouseButtonPressed: coordinates => {
            if (root.isNotCurrentlyEditing) {
                root.viewModel.select(index);
                root.viewModel.openContextMenu(index, coordinates);
            }
        }
    }

    Keys.onPressed: event => _keyHandler.handleKeyPress(event)

    Binding {
        target: root.model
        property: "selectedRow"
        value: root.currentIndex
        restoreMode: Binding.RestoreNone
    }

    Connections {
        target: root.viewModel

        function onQuickSelectionRequested(index: int): void {
            const duration = root.highlightMoveDuration;
            root.highlightMoveDuration = 0;
            root.currentIndex = index;
            root.highlightMoveDuration = duration;
        }

        function onSelectionRequested(index: int): void {
            root.currentIndex = index;
        }

        function onTimeEditRequested(index: int, time: int, coordinates: point): void {
            _editLoader.startEditingTime(index, time, coordinates, root.viewModel.videoDuration);
        }

        function onCommentTypeEditRequested(index: int, commentType: string, coordinates: point): void {
            _editLoader.startEditingCommentType(index, commentType, coordinates, root.viewModel.commentTypes);
        }

        function onCommentEditRequested(index: int, comment: string): void {
            root.positionViewAtIndex(index, ListView.Contain);
            const item = root.currentItem as MpvqcCommentListDelegate;
            const commentLabel = item.commentLabel;
            _editLoader.startEditingComment(index, comment, commentLabel);
        }

        function onContextMenuRequested(index: int, coordinates: point): void {
            _contextMenuLoader.show(index, coordinates);
        }

        function onDeleteCommentRequested(index: int, time: int, commentType: string, commentText: string): void {
            _messageBoxLoader.requestDeletion(index, time, commentType, commentText);
        }

        function onSearchRequested(): void {
            _searchBoxLoader.show();
        }
    }

    MpvqcCommentListKeyHandler {
        id: _keyHandler

        hasComments: root.hasComments
        ignoreEvents: !root.isHandleKeyEvents
        currentIndex: root.currentIndex

        onEditCommentRequested: index => root.viewModel.startEditingComment(index)
        onDeleteCommentRequested: index => root.viewModel.askToDeleteRow(index)
        onCopyCommentRequested: index => root.viewModel.copyToClipboard(index)
        onSearchRequested: root.viewModel.openSearchBox()
        onUndoRequested: root.viewModel.undo()
        onRedoRequested: root.viewModel.redo()
    }

    Connections {
        target: root.model

        function onCommentsAboutToBeImported(): void {
            _editLoader.abortEdit();
            _contextMenuLoader.dismiss();
            _messageBoxLoader.dismiss();
        }
    }

    MpvqcEditLoader {
        id: _editLoader

        // Calculate how much to scroll to keep the expanding editor visible.
        // Returns the scroll amount needed, or 0 if no scrolling is required.
        function _calculateScrollAmount(heightDelta: int): int {
            if (heightDelta <= 0) {
                return 0;
            }

            const currentItem = root.currentItem;
            if (!currentItem) {
                return 0;
            }

            const itemY = currentItem.y - root.contentY;
            const itemBottom = itemY + currentItem.height;
            const newItemBottom = itemBottom + heightDelta;

            const overflow = newItemBottom - root.height;
            return Math.max(0, overflow);
        }

        onCommentEditPopupHeightChanged: (editorHeight, heightDelta) => {
            const scrollAmount = _calculateScrollAmount(heightDelta);
            if (scrollAmount > 0) {
                // Force immediate layout update by setting the editor height explicitly
                // This does not break the binding, but we can scroll to accommodate growth
                root.currentItem.commentLabel.editorHeight = editorHeight;
                root.contentY += scrollAmount;
            }
        }

        onTimeTemporaryChanged: time => root.viewModel.jumpToTime(time)
        onTimeKept: oldTime => root.viewModel.jumpToTime(oldTime)

        onTimeEdited: (index, newTime) => root.viewModel.updateTime(index, newTime)
        onCommentTypeEdited: (index, newCommentType) => root.viewModel.updateCommentType(index, newCommentType)
        onCommentEdited: (index, newComment) => root.viewModel.updateComment(index, newComment)
        onClosed: root.forceActiveFocus()
    }

    MpvqcContextMenuLoader {
        id: _contextMenuLoader

        onEditCommentRequested: index => root.viewModel.startEditingComment(index)
        onCopyCommentRequested: index => root.viewModel.copyToClipboard(index)
        onDeleteCommentRequested: index => root.viewModel.askToDeleteRow(index)
        onDismissed: root.forceActiveFocus()
    }

    MpvqcMessageBoxLoader {
        id: _messageBoxLoader

        onDeleteConfirmed: index => root.viewModel.removeRow(index)
        onClosed: root.forceActiveFocus()
    }

    MpvqcSearchBoxLoader {
        id: _searchBoxLoader

        model: root.model
        selectedIndex: root.currentIndex

        onHighlightRequested: index => root.viewModel.select(index)
        onClosed: root.forceActiveFocus()
    }

    // *** *** ***  *** ***  *** ***  *** ***  *** ***  *** ***  *** ***  *** ***
    // Workaround for QTBUG-145585: On Windows, Popup.Window menus do not respect
    // the modal property, allowing clicks to pass through to underlying items.
    // This item lives in the window overlay layer (above all delegates) and
    // intercepts every click while a menu is open, closing it and swallowing the
    // event so nothing underneath reacts. Only menus are affected; plain Popup
    // items (time editor, message boxes, dialogs) are not covered here.
    Item {
        parent: Overlay.overlay
        anchors.fill: parent
        visible: Qt.platform.os === "windows" && (_editLoader.isEditingCommentType || _contextMenuLoader.active)

        MouseArea {
            anchors.fill: parent
            acceptedButtons: Qt.LeftButton | Qt.RightButton

            onPressed: event => {
                event.accepted = true;
                if (_editLoader.isEditingCommentType && _editLoader.item) {
                    _editLoader.item.close();
                } else if (_contextMenuLoader.active && _contextMenuLoader.item) {
                    _contextMenuLoader.item.close();
                }
            }
        }
    }
    // *** *** ***  *** ***  *** ***  *** ***  *** ***  *** ***  *** ***  *** ***
}

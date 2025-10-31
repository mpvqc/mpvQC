// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls.Material

import pyobjects

import "../../utility"

ListView {
    id: root

    required property var viewModel

    readonly property bool hasComments: count > 0
    readonly property bool isCurrentlyEditing: _editLoader.active
    readonly property bool isNotCurrentlyEditing: !isCurrentlyEditing

    readonly property alias editLoader: _editLoader // for tests
    readonly property alias contextMenuLoader: _contextMenuLoader // for tests
    readonly property alias messageBoxLoader: _messageBoxLoader // for tests

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
        readonly property bool isSelected: ListView.isCurrentItem

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

        onTimeLabelPressed: coordinates => {
            if (root.isCurrentlyEditing && isSelected) {
                return;
            }

            if (isSelected) {
                root.viewModel.pauseVideo();
                root.viewModel.jumpToTime(time);
                root.viewModel.startEditingTime(index, time, coordinates);
            } else {
                root.viewModel.select(index);
            }
        }

        onCommentTypeLabelPressed: coordinates => {
            if (root.isCurrentlyEditing && isSelected) {
                return;
            }

            if (isSelected) {
                root.viewModel.startEditingCommentType(index, commentType, coordinates);
            } else {
                root.viewModel.select(index);
            }
        }

        onCommentLabelPressed: {
            if (isSelected) {
                root.viewModel.startEditingComment(index);
            } else {
                root.viewModel.select(index);
            }
        }

        onRightMouseButtonPressed: coordinates => {
            if (root.isNotCurrentlyEditing) {
                root.viewModel.select(index);
                root.viewModel.openContextMenu(index, coordinates);
            }
        }
    }

    MpvqcCommentListKeyHandler {
        id: _keyHandler

        hasComments: root.hasComments
        isEditing: root.isCurrentlyEditing
        currentIndex: root.currentIndex

        onEditCommentRequested: index => root.viewModel.startEditingComment(index)
        onDeleteCommentRequested: index => root.viewModel.askToDeleteRow(index)
        onCopyCommentRequested: index => root.viewModel.copyToClipboard(index)
        onSearchRequested: root.viewModel.showSearchBox()
        onUndoRequested: root.viewModel.undo()
        onRedoRequested: root.viewModel.redo()
    }

    Keys.onPressed: event => _keyHandler.handleKeyPress(event)

    MpvqcEditLoader {
        id: _editLoader

        viewModel: root.viewModel

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

        onCommentEditPopupHeightChanged: (totalHeight, heightDelta) => {
            const scrollAmount = _calculateScrollAmount(heightDelta);
            if (scrollAmount > 0) {
                // Force immediate layout update by setting the editor height explicitly
                // This does not break the binding, but we can scroll to accommodate growth
                root.currentItem.commentLabel.editorHeight = totalHeight;
                root.contentY += scrollAmount;
            }
        }
    }

    MpvqcContextMenuLoader {
        id: _contextMenuLoader

        viewModel: root.viewModel
    }

    MpvqcMessageBoxLoader {
        id: _messageBoxLoader

        viewModel: root.viewModel
        onClosed: root.forceActiveFocus()
    }

    MpvqcSearchBoxLoader {
        id: _searchBoxLoader

        viewModel: root.viewModel
        searchBoxViewModel: MpvqcSearchBoxViewModel {
            model: root.model
            selectedIndex: root.currentIndex
            onHighlightRequested: index => root.viewModel.select(index)
        }
        onClosed: root.forceActiveFocus()
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

        function onRowEditRequested(index: int): void {
            onQuickSelectionRequested(index);
            onCommentEditRequested(index);
        }

        function onLastRowSelected(): void {
            const lastIndex = root.count - 1;
            onQuickSelectionRequested(lastIndex);
        }

        function onCommentEditRequested(index: int): void {
            root.positionViewAtIndex(index, ListView.Contain);
            const item = root.currentItem as MpvqcCommentListDelegate;
            const comment = item.comment;
            const commentLabel = item.commentLabel;
            _editLoader.startEditingComment(index, comment, commentLabel);
        }
    }

    Binding {
        target: root.model
        property: "selectedRow"
        value: root.currentIndex
        restoreMode: Binding.RestoreNone
    }
}

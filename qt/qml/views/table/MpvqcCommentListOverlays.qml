// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick

Item {
    id: root

    required property var viewModel
    required property ListView listView

    readonly property bool anyModalActive: _editLoader.active || _contextMenuLoader.active || _messageBoxLoader.active
    readonly property string searchQuery: _searchBoxLoader.searchQuery

    signal focusWanted

    Connections {
        target: root.viewModel

        function onTimeEditRequested(index: int, time: int, coordinates: point): void {
            _editLoader.startEditingTime(index, time, coordinates, root.viewModel.videoDuration);
        }

        function onCommentTypeEditRequested(index: int, commentType: string, coordinates: point): void {
            _editLoader.startEditingCommentType(index, commentType, coordinates, root.viewModel.commentTypes);
        }

        function onCommentEditRequested(index: int, comment: string): void {
            root.listView.positionViewAtIndex(index, ListView.Contain);
            const item = root.listView.currentItem as MpvqcCommentListDelegate;
            _editLoader.startEditingComment(index, comment, item.commentLabel);
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

    Connections {
        target: root.viewModel.model

        function onCommentsAboutToBeImported(): void {
            _editLoader.abortEdit();
            _contextMenuLoader.dismiss();
            _messageBoxLoader.dismiss();
        }
    }

    MpvqcEditLoader {
        id: _editLoader

        onTimeTemporaryChanged: time => root.viewModel.jumpToTime(time)
        onTimeKept: oldTime => root.viewModel.jumpToTime(oldTime)

        onTimeEdited: (index, newTime) => root.viewModel.updateTime(index, newTime)
        onCommentTypeEdited: (index, newCommentType) => root.viewModel.updateCommentType(index, newCommentType)
        onCommentEdited: (index, newComment) => root.viewModel.updateComment(index, newComment)

        onClosed: root.focusWanted()
    }

    MpvqcContextMenuLoader {
        id: _contextMenuLoader

        onEditCommentRequested: index => root.viewModel.startEditingComment(index)
        onCopyCommentRequested: index => root.viewModel.copyToClipboard(index)
        onDeleteCommentRequested: index => root.viewModel.askToDeleteRow(index)
        onDismissed: root.focusWanted()
    }

    MpvqcMessageBoxLoader {
        id: _messageBoxLoader

        onDeleteConfirmed: index => root.viewModel.removeRow(index)
        onClosed: root.focusWanted()
    }

    MpvqcSearchBoxLoader {
        id: _searchBoxLoader

        model: root.viewModel.model
        selectedIndex: root.listView.currentIndex

        onHighlightRequested: index => root.viewModel.select(index)
        onClosed: root.focusWanted()
    }

    MpvqcWindowsMenuClickGuard {
        editLoader: _editLoader
        contextMenuLoader: _contextMenuLoader
    }
}

// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick

import io.github.mpvqc.mpvQC.Python

Item {
    id: root

    required property MpvqcCommentTableViewModel viewModel
    required property ListView listView

    readonly property bool anyRowPopupOpen: _editLoader.active || _contextMenuLoader.active || _deleteConfirmationLoader.active
    readonly property bool anyModalPopupOpen: _editLoader.modalPopupOpen || _contextMenuLoader.modalPopupOpen || _deleteConfirmationLoader.modalPopupOpen

    readonly property string searchQuery: _searchBoxLoader.searchQuery

    signal focusWanted
    signal selectRequested(index: int)

    function openTimeEditor(index: int, time: int, coordinates: point): void {
        _editLoader.startEditingTime(index, time, coordinates, root.viewModel.videoDuration);
    }

    function openCommentTypeEditor(index: int, commentType: string, coordinates: point): void {
        _editLoader.startEditingCommentType(index, commentType, coordinates, root.viewModel.commentTypes);
    }

    function openCommentEditor(index: int): void {
        root.listView.positionViewAtIndex(index, ListView.Contain);
        const item = root.listView.itemAtIndex(index) as MpvqcCommentListDelegate;
        _editLoader.startEditingComment(index, item.comment, item.commentLabel);
    }

    function openContextMenu(index: int, coordinates: point): void {
        _contextMenuLoader.show(index, coordinates);
    }

    function openSearchBox(): void {
        _searchBoxLoader.show();
    }

    Connections {
        target: root.viewModel

        function onCommentEditRequested(index: int): void {
            root.openCommentEditor(index);
        }

        function onDeleteCommentRequested(index: int, time: int, commentType: string, commentText: string): void {
            _deleteConfirmationLoader.requestDeletion(index, time, commentType, commentText);
        }

        function onCommentsAboutToBeImported(): void {
            _editLoader.abortEdit();
            _contextMenuLoader.dismiss();
            _deleteConfirmationLoader.dismiss();
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

        onEditCommentRequested: index => root.openCommentEditor(index)
        onCopyCommentRequested: index => root.viewModel.copyToClipboard(index)
        onDeleteCommentRequested: index => root.viewModel.askToDeleteRow(index)
        onDismissed: root.focusWanted()
    }

    MpvqcDeleteConfirmationLoader {
        id: _deleteConfirmationLoader

        onDeleteConfirmed: index => root.viewModel.removeRow(index)
        onClosed: root.focusWanted()
    }

    MpvqcSearchBoxLoader {
        id: _searchBoxLoader

        modalPopupOpen: root.anyModalPopupOpen

        onHighlightRequested: index => root.selectRequested(index)
        onClosed: root.focusWanted()
    }

    MpvqcWindowsMenuClickGuard {
        editLoader: _editLoader
        contextMenuLoader: _contextMenuLoader
    }
}

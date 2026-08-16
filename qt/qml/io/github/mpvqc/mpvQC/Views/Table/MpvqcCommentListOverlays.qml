// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick

import io.github.mpvqc.mpvQC.Python

Item {
    id: root

    required property MpvqcCommentTableViewModel viewModel
    required property MpvqcCommentList commentList

    readonly property bool anyRowPopupOpen: _editLoader.active || _contextMenuLoader.active || _deleteConfirmationLoader.active

    readonly property string searchQuery: _searchBoxLoader.searchQuery

    function _openCommentEditor(index: int): void {
        root.commentList.positionViewAtIndex(index, ListView.Contain);
        const item = root.commentList.itemAtIndex(index) as MpvqcCommentListDelegate;
        _editLoader.startEditingComment(index, item.comment, item.commentLabel);
    }

    Connections {
        target: root.commentList

        function onEditTimeRequested(index: int, time: int, coordinates: point): void {
            _editLoader.startEditingTime(index, time, coordinates);
        }

        function onEditCommentTypeRequested(index: int, commentType: string, coordinates: point): void {
            _editLoader.startEditingCommentType(index, commentType, coordinates);
        }

        function onEditCommentRequested(index: int): void {
            root._openCommentEditor(index);
        }

        function onContextMenuRequested(index: int, coordinates: point): void {
            _contextMenuLoader.show(index, coordinates);
        }

        function onSearchRequested(): void {
            _searchBoxLoader.show();
        }
    }

    Connections {
        target: root.viewModel

        function onEditCommentRequested(index: int): void {
            root._openCommentEditor(index);
        }

        function onDeleteConfirmationRequested(index: int, time: int, commentType: string, commentText: string): void {
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

        viewModel: root.viewModel

        onClosed: root.commentList.forceActiveFocus()
    }

    MpvqcContextMenuLoader {
        id: _contextMenuLoader

        viewModel: root.viewModel

        onEditCommentRequested: index => root._openCommentEditor(index)
        onDismissed: root.commentList.forceActiveFocus()
    }

    MpvqcDeleteConfirmationLoader {
        id: _deleteConfirmationLoader

        viewModel: root.viewModel

        onClosed: root.commentList.forceActiveFocus()
    }

    MpvqcSearchBoxLoader {
        id: _searchBoxLoader

        onHighlightRequested: index => root.commentList.selectRow(index)
        onClosed: root.commentList.forceActiveFocus()
    }

    MpvqcWindowsMenuClickGuard {
        editLoader: _editLoader
        contextMenuLoader: _contextMenuLoader
    }
}

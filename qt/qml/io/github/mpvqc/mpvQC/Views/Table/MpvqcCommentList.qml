// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls.Material

import io.github.mpvqc.mpvQC.Utility

ListView {
    id: root

    required property var viewModel
    required property bool modalActive
    required property string searchQuery

    model: viewModel.model

    clip: true
    focus: true
    reuseItems: true

    interactive: !root.modalActive
    boundsBehavior: Flickable.StopAtBounds

    highlightMoveDuration: 50
    highlightMoveVelocity: -1
    highlightResizeDuration: root.modalActive ? 0 : 50
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

        searchQuery: root.searchQuery

        onPlayButtonPressed: {
            root.viewModel.select(index);
            if (!root.modalActive) {
                root.viewModel.jumpToTime(time);
            }
        }

        onRowPressed: root.viewModel.select(index)

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
            if (!root.modalActive) {
                root.viewModel.select(index);
                root.viewModel.openContextMenu(index, coordinates);
            }
        }

        // The delegate grew to accommodate its inline editor; scroll just
        // enough to keep the bottom of the delegate visible.
        onHeightGrewWhileEditing: delta => {
            const itemBottom = y - root.contentY + height;
            const overflow = itemBottom - root.height;
            if (overflow > 0) {
                root.contentY += Math.min(overflow, delta);
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
    }

    MpvqcCommentListKeyHandler {
        id: _keyHandler

        hasComments: root.count > 0
        ignoreEvents: root.modalActive
        currentIndex: root.currentIndex

        onEditCommentRequested: index => root.viewModel.startEditingComment(index)
        onDeleteCommentRequested: index => root.viewModel.askToDeleteRow(index)
        onCopyCommentRequested: index => root.viewModel.copyToClipboard(index)
        onSearchRequested: root.viewModel.openSearchBox()
        onUndoRequested: root.viewModel.undo()
        onRedoRequested: root.viewModel.redo()
    }
}

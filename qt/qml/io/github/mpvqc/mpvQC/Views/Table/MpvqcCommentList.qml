// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls

import io.github.mpvqc.mpvQC.Python
import io.github.mpvqc.mpvQC.Utility

ListView {
    id: root

    required property MpvqcCommentTableViewModel viewModel
    required property bool modalActive
    required property string searchQuery

    readonly property int _animationDuration: 50
    property bool _instantHighlight: false

    /**
     *  Set currentIndex to a value different from `target` so a subsequent
     *  assignment to `target` is a real change. Required to trigger Qt's
     *  auto-scroll when the assignment would otherwise be a no-op.
     */
    function _nudgeCurrentIndex(target: int): void {
        if (target !== 0) {
            root.currentIndex = target - 1;
        } else if (root.count > 1 && root.currentIndex !== 1) {
            root.currentIndex = 1;
        } else if (root.count > 2) {
            root.currentIndex = 2;
        }
    }

    model: viewModel.model

    clip: true
    focus: true
    reuseItems: true

    interactive: !root.modalActive
    boundsBehavior: Flickable.StopAtBounds

    highlightMoveDuration: _instantHighlight ? 0 : _animationDuration
    highlightMoveVelocity: -1
    highlightResizeDuration: root.modalActive ? 0 : _animationDuration
    highlightResizeVelocity: -1

    move: Transition {
        NumberAnimation {
            property: "y"
            duration: root._animationDuration
        }
    }

    displaced: Transition {
        NumberAnimation {
            property: "y"
            duration: root._animationDuration
        }
    }

    remove: Transition {
        NumberAnimation {
            property: "y"
            duration: root._animationDuration
        }
    }

    highlight: Rectangle {
        width: parent ? parent.width - _scrollBar.visibleWidth : 0
        height: parent?.height ?? 0
        color: MpvqcTheme.palette.rowSelected
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

        onHeightChangedWhileEditing: {
            // The delegate's height changed while its inline editor is open;
            // scroll just enough to keep its bottom in view.
            const itemBottom = y - root.contentY + height;
            const overflow = itemBottom - root.height;
            if (overflow > 0) {
                root.contentY += overflow;
            }
        }
    }

    ScrollBar.vertical: ScrollBar {
        id: _scrollBar

        readonly property bool isShown: root.contentHeight > root.height
        readonly property int visibleWidth: isShown ? width : 0

        policy: isShown ? ScrollBar.AlwaysOn : ScrollBar.AlwaysOff
    }

    Keys.onPressed: event => _keyHandler.handleKeyPress(event)

    Connections {
        // Keep the highlight from sliding to the wrong row during structural model changes.
        target: root.model

        function onAboutToInsertRow(): void {
            root._instantHighlight = true;
            root.currentIndex = -1;
            root._instantHighlight = false;
        }

        function onAboutToRemoveRow(): void {
            root.highlightFollowsCurrentItem = false;
        }

        function onRowsRemoved(): void {
            _reEngageHighlightTracking.restart();
        }
    }

    Timer {
        id: _reEngageHighlightTracking
        interval: root._animationDuration
        onTriggered: root.highlightFollowsCurrentItem = true
    }

    Binding {
        target: root.viewModel.selection
        property: "selectedRow"
        value: root.currentIndex
        restoreMode: Binding.RestoreNone
    }

    Binding {
        target: root.viewModel.selection
        property: "selectedRowVisible"
        value: root.currentItem !== null && root.currentItem.y >= root.contentY && root.currentItem.y + root.currentItem.height <= root.contentY + root.height
        restoreMode: Binding.RestoreNone
    }

    Connections {
        target: root.viewModel

        function onQuickSelectionRequested(index: int): void {
            if (root.currentIndex === index) {
                root.positionViewAtIndex(index, ListView.Contain);
                return;
            }
            root._instantHighlight = true;
            root.currentIndex = index;
            root._instantHighlight = false;
        }

        function onSelectionRequested(index: int): void {
            root._nudgeCurrentIndex(index);
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

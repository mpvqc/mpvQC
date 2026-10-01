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
    required property bool rowPopupOpen
    required property string searchQuery

    readonly property int _animationDuration: 50
    property bool _instantHighlight: false
    property bool _layoutPending: false
    readonly property bool _rowsSettling: _layoutPending || _displacedTransition.running

    signal editTimeRequested(index: int, time: int, coordinates: point)
    signal editCommentTypeRequested(index: int, commentType: string, coordinates: point)
    signal editCommentRequested(index: int)
    signal contextMenuRequested(index: int, coordinates: point)
    signal searchRequested

    function selectRow(index: int): void {
        _nudgeCurrentIndex(index);
        root.currentIndex = index;
    }

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

    interactive: !root.rowPopupOpen
    boundsBehavior: Flickable.StopAtBounds

    highlightMoveDuration: _instantHighlight ? 0 : _animationDuration
    highlightMoveVelocity: -1
    highlightResizeDuration: root.rowPopupOpen ? 0 : _animationDuration
    highlightResizeVelocity: -1

    move: Transition {
        NumberAnimation {
            property: "y"
            duration: root._animationDuration
        }
    }

    displaced: Transition {
        id: _displacedTransition

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
        color: MpvqcAppearance.palette.rowSelected
    }

    delegate: MpvqcCommentListDelegate {
        width: parent ? root.width : 0
        scrollBarWidth: _scrollBar.visibleWidth

        searchQuery: root.searchQuery

        onPlayButtonPressed: {
            root.selectRow(index);
            if (!root.rowPopupOpen) {
                root.viewModel.jumpToTime(time);
            }
        }

        onRowPressed: root.selectRow(index)

        onTimeLabelDoubleClicked: coordinates => {
            root.viewModel.pauseVideo();
            root.viewModel.jumpToTime(time);
            root.editTimeRequested(index, time, coordinates);
        }

        onCommentTypeLabelDoubleClicked: coordinates => {
            root.editCommentTypeRequested(index, commentType, coordinates);
        }

        onCommentLabelDoubleClicked: {
            root.editCommentRequested(index);
        }

        onRightMouseButtonPressed: coordinates => {
            if (!root.rowPopupOpen) {
                root.selectRow(index);
                root.contextMenuRequested(index, coordinates);
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

        property bool isShown: false
        readonly property int visibleWidth: isShown ? width : 0

        policy: isShown ? ScrollBar.AlwaysOn : ScrollBar.AlwaysOff
    }

    Keys.onPressed: event => _keyHandler.handleKeyPress(event)

    Connections {
        // Keep the highlight from sliding to the wrong row during structural model changes.
        target: root.model

        function onAboutToInsertRow(): void {
            root._layoutPending = true;
            root._instantHighlight = true;
            root.currentIndex = -1;
            root._instantHighlight = false;
        }

        function onAboutToRemoveRow(): void {
            root._layoutPending = true;
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

    Connections {
        // A model change is laid out, and its transitions started, when the window polishes its items.
        // The window emits afterAnimating right after that, so from then on the transitions tell
        // whether the rows still move
        target: root.Window.window
        enabled: root._layoutPending

        function onAfterAnimating(): void {
            root._layoutPending = false;
        }
    }

    Binding {
        // An inserted or removed row can make the scroll bar appear or vanish, and the rows wrap
        // differently with it. A row that changes height while a transition moves it lands where it
        // was headed before, leaving gaps or overlaps. So the scroll bar waits until the rows settled
        target: _scrollBar
        property: "isShown"
        value: root.contentHeight > root.height
        when: !root._rowsSettling
        restoreMode: Binding.RestoreNone
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
            root.selectRow(index);
        }
    }

    MpvqcCommentListKeyHandler {
        id: _keyHandler

        hasComments: root.count > 0
        ignoreEvents: root.rowPopupOpen
        currentIndex: root.currentIndex

        onEditCommentRequested: index => root.editCommentRequested(index)
        onDeleteCommentRequested: index => root.viewModel.askToDeleteRow(index)
        onCopyCommentRequested: index => root.viewModel.copyToClipboard(index)
        onSearchRequested: root.searchRequested()
        onUndoRequested: root.viewModel.undo()
        onRedoRequested: root.viewModel.redo()
    }
}

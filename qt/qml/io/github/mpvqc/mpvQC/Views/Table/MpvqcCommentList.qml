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

    readonly property bool _selectedRowVisible: currentItem !== null && currentItem.y > contentY - 1 && currentItem.y + currentItem.height < contentY + height + 1

    signal editTimeRequested(index: int, time: int, coordinates: point)
    signal editCommentTypeRequested(index: int, commentType: string, coordinates: point)
    signal editCommentRequested(index: int)
    signal contextMenuRequested(index: int, coordinates: point)
    signal searchRequested

    function selectRow(index: int): void {
        _nudgeCurrentIndex(index);
        root.currentIndex = index;
    }

    // Qt scrolls to the current item only when currentIndex changes
    function _nudgeCurrentIndex(target: int): void {
        if (target !== 0) {
            root.currentIndex = target - 1;
        } else if (root.count > 1 && root.currentIndex !== 1) {
            root.currentIndex = 1;
        } else if (root.count > 2) {
            root.currentIndex = 2;
        }
    }

    // The highlight animation reads its duration when the move starts
    function _withInstantHighlight(move: var): void {
        root._instantHighlight = true;
        move();
        root._instantHighlight = false;
    }

    model: viewModel.model

    clip: true
    focus: true
    reuseItems: true

    interactive: !root.rowPopupOpen
    boundsBehavior: Flickable.StopAtBounds

    highlightMoveDuration: _instantHighlight ? 0 : _animationDuration
    highlightMoveVelocity: -1
    // The inline editor grows the row while typing, and the highlight has to keep up with it
    highlightResizeDuration: root.rowPopupOpen || _instantHighlight ? 0 : _animationDuration
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
        id: _removeTransition

        // Without from or to, the row holds still while the rows below slide over it. Unlike a
        // PauseAnimation, a row removed mid-slide still finishes its slide
        NumberAnimation {
            property: "y"
            duration: root._animationDuration
        }
    }

    highlight: Rectangle {
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

    on_RowsSettlingChanged: {
        if (!_rowsSettling) {
            root._withInstantHighlight(() => root.highlightFollowsCurrentItem = true);
        }
    }

    Keys.onPressed: event => _keyHandler.handleKeyPress(event)

    Connections {
        target: root.model

        function onRowsInserted(): void {
            root._layoutPending = true;
        }

        function onRowsAboutToBeRemoved(parent: var, first: int, last: int): void {
            root._layoutPending = true;
            _removeTransition.enabled = last < root.count - 1;
            root.highlightFollowsCurrentItem = false;
        }

        function onRowsRemoved(): void {
            Qt.callLater(root.forceLayout);
        }
    }

    Connections {
        // The window polishes, which starts the transitions, right before it emits afterAnimating
        target: root.Window.window
        enabled: root._layoutPending

        function onAfterAnimating(): void {
            root._layoutPending = false;
        }
    }

    Binding {
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
        value: root._selectedRowVisible
        restoreMode: Binding.RestoreNone
    }

    Connections {
        target: root.viewModel

        function onQuickSelectionRequested(index: int): void {
            root.forceLayout();
            if (root.currentIndex === index) {
                root.positionViewAtIndex(index, ListView.Contain);
                return;
            }
            root._withInstantHighlight(() => root.currentIndex = index);
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

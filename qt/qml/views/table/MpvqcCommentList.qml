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
    readonly property bool isCurrentlyFullScreen: MpvqcWindowProperties.isFullscreen
    readonly property list<string> commentTypes: viewModel.commentTypes
    readonly property int videoDuration: viewModel.videoDuration

    readonly property alias editLoader: _editLoader // for tests
    readonly property alias contextMenuLoader: _contextMenuView // for tests
    readonly property alias messageBoxLoader: _messageBoxLoader // for tests

    model: viewModel.model

    clip: true
    focus: true
    reuseItems: true

    interactive: isNotCurrentlyEditing
    boundsBehavior: Flickable.StopAtBounds

    highlightMoveDuration: 50
    highlightMoveVelocity: -1
    highlightResizeDuration: 50
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
        searchQuery: _impl.searchQuery

        onPlayButtonPressed: {
            root.viewModel.select(index);
            if (root.isNotCurrentlyEditing) {
                root.viewModel.jumpToTime(time);
            }
        }

        onTimeLabelPressed: coordinates => {
            if (root.isCurrentlyEditing && isSelected) {
                ;
            } else if (isSelected) {
                root.viewModel.pauseVideo();
                root.viewModel.jumpToTime(time);
                root.viewModel.startEditingTime(index, time, coordinates);
            } else {
                root.viewModel.select(index);
            }
        }

        onCommentTypeLabelPressed: coordinates => {
            if (root.isCurrentlyEditing && isSelected) {
                ;
            } else if (isSelected) {
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

    QtObject {
        id: _impl

        readonly property alias searchQuery: _searchBoxLoader.searchQuery

        readonly property Timer _ensureCommentVisibleTimer: Timer {
            interval: 0
            onTriggered: root.positionViewAtIndex(root.currentIndex, ListView.Contain)
        }

        function ensureFullCommentEditingPopupVisible(): void {
            _ensureCommentVisibleTimer.restart();
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
        onSearchRequested: _searchBoxLoader.showSearchBox()
        onUndoRequested: root.viewModel.undo()
        onRedoRequested: root.viewModel.redo()
    }

    Keys.onPressed: event => _keyHandler.handleKeyPress(event)

    Loader {
        id: _editLoader

        readonly property url editCommentTypeMenu: Qt.resolvedUrl("MpvqcEditCommentTypeMenu.qml")
        readonly property url editCommentPopup: Qt.resolvedUrl("MpvqcEditCommentPopup.qml")
        readonly property url editTimePopup: Qt.resolvedUrl("MpvqcEditTimePopup.qml")

        readonly property bool isEditingComment: source === editCommentPopup

        function startEditingTime(index: int, time: int, coordinates: point): void {
            asynchronous = true;
            setSource(editTimePopup, {
                currentTime: time,
                currentListIndex: index,
                videoDuration: root.videoDuration,
                openedAt: coordinates
            });
            active = true;
        }

        function startEditingCommentType(index: int, currentCommentType: string, coordinates: point): void {
            asynchronous = true;
            setSource(editCommentTypeMenu, {
                currentCommentType: currentCommentType,
                currentListIndex: index,
                commentTypes: root.commentTypes,
                openedAt: coordinates
            });
            active = true;
        }

        function startEditingComment(index: int, currentComment: string, parentItem): void {
            asynchronous = false;
            setSource(editCommentPopup, {
                parent: parentItem,
                currentComment: currentComment,
                currentListIndex: index
            });
            active = true;
        }

        active: false
        visible: active

        onLoaded: item.open() // qmllint disable

        Connections {
            target: _editLoader.item
            ignoreUnknownSignals: true

            function onTimeTemporaryChanged(time: int): void {
                root.viewModel.jumpToTime(time);
            }

            function onTimeEdited(index: int, newTime: int): void {
                root.viewModel.updateTime(index, newTime);
            }

            function onTimeKept(oldTime: int): void {
                root.viewModel.jumpToTime(oldTime);
            }

            function onCommentTypeEdited(index: int, newCommentType: string): void {
                root.viewModel.updateCommentType(index, newCommentType);
            }

            function onCommentEdited(index: int, newComment: string): void {
                root.viewModel.updateComment(index, newComment);
            }

            function onCommentEditPopupHeightChanged(): void {
                _impl.ensureFullCommentEditingPopupVisible();
            }

            function onClosed(): void {
                _stopEditDelayTimer.restart();
            }
        }

        Timer {
            id: _stopEditDelayTimer

            interval: _editLoader.isEditingComment ? 150 : 0

            onTriggered: {
                _editLoader.active = false;
            }
        }
    }

    MpvqcContextMenuView {
        id: _contextMenuView

        viewModel: root.viewModel
    }

    Loader {
        id: _messageBoxLoader

        function askToDeleteComment(index: int): void {
            setSource("../../messageboxes/MpvqcDeleteCommentMessageBox.qml", {
                commentIndex: index
            });
            active = true;
        }

        active: false
        asynchronous: true
        visible: active

        onLoaded: item.open() // qmllint disable

        Connections {
            target: _messageBoxLoader.item

            function onDeleteCommentConfirmed(index: int): void {
                root.viewModel.removeRow(index);
            }

            function onClosed(): void {
                _messageBoxLoader.active = false;
            }
        }
    }

    Loader {
        id: _searchBoxLoader

        readonly property string searchQuery: item?.searchQuery ?? "" // qmllint disable

        function showSearchBox(): void {
            if (active) {
                item.open(); // qmllint disable
            } else {
                active = true;
            }
        }

        active: false
        asynchronous: true
        visible: active

        onLoaded: item.open() // qmllint disable

        sourceComponent: MpvqcSearchBoxView {
            id: _searchBox

            parent: root

            viewModel: MpvqcSearchBoxViewModel {
                model: root.model
                selectedIndex: root.currentIndex

                onHighlightRequested: index => root.viewModel.select(index)
            }

            onClosed: root.forceActiveFocus()
        }
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

        function onTimeEditRequested(index: int, time: int, coordinates: point): void {
            _editLoader.startEditingTime(index, time, coordinates);
        }

        function onCommentTypeEditRequested(index: int, commentType: string, coordinates: point): void {
            _editLoader.startEditingCommentType(index, commentType, coordinates);
        }

        function onCommentEditRequested(index: int): void {
            root.positionViewAtIndex(index, ListView.Contain);
            const item = root.currentItem as MpvqcCommentListDelegate;
            const comment = item.comment; // qmllint disable
            const commentLabel = item.commentLabel;
            _editLoader.startEditingComment(index, comment, commentLabel);
        }

        function onDeleteCommentRequested(index: int): void {
            _messageBoxLoader.askToDeleteComment(index);
        }
    }

    Binding {
        target: root.model
        property: "selectedRow"
        value: root.currentIndex
        restoreMode: Binding.RestoreNone
    }
}

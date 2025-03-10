/*
mpvQC

Copyright (C) 2022 mpvQC developers

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls.Material

ListView {
    id: root

    required property int timeLabelWidth
    required property int commentTypeLabelWidth

    required property color backgroundColor
    required property color rowHighlightColor
    required property color rowHighlightTextColor
    required property color rowBaseColor
    required property color rowBaseTextColor
    required property color rowAlternateBaseColor
    required property color rowAlternateBaseTextColor

    required property var timeFormatFunc
    required property var sanitizeTextFunc
    required property var jumpToTimeFunc
    required property var pauseVideoFunc

    required property var defaultTextValidator
    required property var messageBoxParent
    required property list<string> commentTypes

    required property int videoDuration
    required property bool isCurrentlyFullScreen

    readonly property bool hasComments: root.count > 0
    readonly property bool isCurrentlyEditing: _editLoader.active
    readonly property bool isNotCurrentlyEditing: !isCurrentlyEditing

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
        color: root.rowHighlightColor
    }

    ScrollBar.vertical: ScrollBar {
        id: _scrollBar

        readonly property bool isShown: root.contentHeight > root.height
        readonly property int visibleWidth: isShown ? width : 0

        policy: isShown ? ScrollBar.AlwaysOn : ScrollBar.AlwaysOff
    }

    delegate: MpvqcCommentListDelegate {
        readonly property bool isSelected: root.currentIndex === index
        readonly property bool isOdd: index % 2 === 1

        width: parent ? root.width : 0

        timeLabelWidth: root.timeLabelWidth
        commentTypeLabelWidth: root.commentTypeLabelWidth

        timeFormatFunc: root.timeFormatFunc

        backgroundColor: isOdd ? root.rowBaseColor : root.rowAlternateBaseColor
        foregroundColor: isSelected ? root.rowHighlightTextColor : isOdd ? root.rowBaseTextColor : root.rowAlternateBaseTextColor

        listView: root
        searchQuery: _impl.searchQuery

        scrollBarWidth: _scrollBar.visibleWidth
        scrollBarBackgroundColor: root.backgroundColor

        onPlayButtonPressed: {
            _impl.select(index);
            if (root.isNotCurrentlyEditing) {
                _impl.jumpToTime(time);
            }
        }

        onTimeLabelPressed: coordinates => {
            if (root.isCurrentlyEditing && isSelected) {
                ;
            } else if (isSelected) {
                _impl.pauseVideo();
                _impl.jumpToTime(time);
                _impl.startEditingTime(index, time, coordinates);
            } else {
                _impl.select(index);
            }
        }

        onCommentTypeLabelPressed: coordinates => {
            if (root.isCurrentlyEditing && isSelected) {
                ;
            } else if (isSelected) {
                _impl.startEditingCommentType(index, commentType, coordinates);
            } else {
                _impl.select(index);
            }
        }

        onCommentLabelPressed: {
            if (isSelected) {
                _impl.startEditingComment();
            } else {
                _impl.select(index);
            }
        }

        onRightMouseButtonPressed: coordinates => {
            if (root.isNotCurrentlyEditing) {
                _impl.select(index);
                _impl.openContextMenu(index, coordinates);
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

        function select(index: int): void {
            root.currentIndex = index;
        }

        function selectQuickly(index: int): void {
            const duration = root.highlightMoveDuration;
            root.highlightMoveDuration = 0;
            root.currentIndex = index;
            root.highlightMoveDuration = duration;
        }

        function jumpToTime(time: int): void {
            root.jumpToTimeFunc(time); // qmllint disable
        }

        function pauseVideo(): void {
            root.pauseVideoFunc(); // qmllint disable
        }

        function startEditingTime(index: int, currentTime: int, coordinates: point): void {
            _editLoader.startEditingTime(index, currentTime, coordinates);
        }

        function startEditingCommentType(index: int, currentCommentType: string, coordinates: point): void {
            _editLoader.startEditingCommentType(index, currentCommentType, coordinates);
        }

        function startEditingComment(): void {
            const index = root.currentIndex;
            const item = root.currentItem;
            const comment = item.comment; // qmllint disable
            const commentLabel = item.commentLabel;
            root.positionViewAtIndex(index, ListView.Contain);
            _editLoader.startEditingComment(index, comment, commentLabel);
        }

        function updateTime(index: int, newTime: int): void {
            root.model.update_time(index, newTime);
        }

        function updateCommentType(index: int, newCommentType: string): void {
            root.model.update_comment_type(index, newCommentType);
        }

        function updateComment(index: int, newComment: string): void {
            root.model.update_comment(index, newComment);
        }

        function openContextMenu(index: int, coordinates: point): void {
            _contextMenuLoader.openContextMenu(index, coordinates);
        }

        function askToDeleteRow(index: int): void {
            _messageBoxLoader.askToDeleteComment(index);
        }

        function removeRow(index: int): void {
            root.model.remove_row(index);
        }

        function copyCommentToClipboard(index: int): void {
            root.model.copy_to_clipboard(index);
        }

        function ensureFullCommentEditingPopupVisible(): void {
            _ensureCommentVisibleTimer.restart();
        }

        function performModelSearch(searchQuery: string, includeCurrentRow: bool, topDown: bool): var {
            return root.model.search(searchQuery, includeCurrentRow, topDown, root.currentIndex);
        }
    }

    Keys.onPressed: event => _keyEventHandler.handleKeyPress(event)

    QtObject {
        id: _keyEventHandler

        readonly property bool isHaveComments: root.hasComments
        readonly property bool isCurrentlyEditing: root.isCurrentlyEditing
        readonly property bool isCurrentlyFullScreen: root.isCurrentlyFullScreen

        function handleKeyPress(event: KeyEvent): void {
            switch (event.key) {
            case Qt.Key_Return:
                _keyEventHandler._handleReturnKeyPressed(event);
                break;
            case Qt.Key_Delete:
            case Qt.Key_Backspace:
                _keyEventHandler._handleDeleteComment(event);
                break;
            case Qt.Key_C:
                _keyEventHandler._handleCPressed(event);
                break;
            case Qt.Key_F:
                _keyEventHandler._handleFPressed(event);
                break;
            case Qt.Key_Z:
                _keyEventHandler._handleZPressed(event);
                break;
            default:
                event.accepted = false;
            }
        }

        function _handleReturnKeyPressed(event: KeyEvent): void {
            if (event.isAutoRepeat) {
                return;
            }
            if (isHaveComments && !isCurrentlyEditing && !isCurrentlyFullScreen) {
                _impl.startEditingComment();
            }
        }

        function _handleDeleteComment(event: KeyEvent): void {
            if (event.isAutoRepeat) {
                return;
            }
            if (isHaveComments && !isCurrentlyFullScreen) {
                _impl.askToDeleteRow(root.currentIndex);
            }
        }

        function _handleCPressed(event: KeyEvent): void {
            const isCtrlPressed = event.modifiers === Qt.ControlModifier;
            if (isCtrlPressed && !event.isAutoRepeat) {
                if (isHaveComments && !isCurrentlyEditing && !isCurrentlyFullScreen) {
                    _impl.copyCommentToClipboard(root.currentIndex);
                    return;
                }
            }
            event.accepted = false;
        }

        function _handleFPressed(event: KeyEvent): void {
            const isCtrlPressed = event.modifiers === Qt.ControlModifier;
            if (isCtrlPressed && !event.isAutoRepeat) {
                if (isHaveComments && !isCurrentlyEditing && !isCurrentlyFullScreen) {
                    _searchBoxLoader.showSearchBox();
                    return;
                }
            }
            event.accepted = false;
        }

        function _handleZPressed(event: KeyEvent): void {
            const isCtrlPressed = event.modifiers & Qt.ControlModifier;
            const isShiftPressed = event.modifiers & Qt.ShiftModifier;
            if (isCtrlPressed && !event.isAutoRepeat) {
                if (isShiftPressed) {
                    root.model.redo();
                } else {
                    root.model.undo();
                }
                return;
            }
            event.accepted = false;
        }
    }

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
                timeFormatFunc: root.timeFormatFunc,
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
                currentListIndex: index,
                sanitizeTextFunc: root.sanitizeTextFunc,
                backgroundColor: index % 2 === 1 ? root.rowBaseColor : root.rowAlternateBaseColor,
                rowHighlightColor: root.rowHighlightColor,
                rowHighlightTextColor: root.rowHighlightTextColor
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
                _impl.jumpToTime(time);
            }

            function onTimeEdited(index: int, newTime: int): void {
                _impl.updateTime(index, newTime);
            }

            function onTimeKept(oldTime: int): void {
                _impl.jumpToTime(oldTime);
            }

            function onCommentTypeEdited(index: int, newCommentType: string): void {
                _impl.updateCommentType(index, newCommentType);
            }

            function onCommentEdited(index: int, newComment: string): void {
                _impl.updateComment(index, newComment);
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

    Loader {
        id: _contextMenuLoader

        function openContextMenu(index: int, coordinates: point): void {
            setSource("MpvqcContextMenu.qml", {
                currentListIndex: index,
                openedAt: coordinates
            });
            active = true;
        }

        active: false
        asynchronous: true
        visible: active

        onLoaded: item.open() // qmllint disable

        Connections {
            target: _contextMenuLoader.item

            function onCopyCommentClicked(index: int): void {
                _impl.copyCommentToClipboard(index);
            }

            function onDeleteCommentClicked(index: int): void {
                _impl.askToDeleteRow(index);
            }

            function onEditCommentClicked(index: int): void {
                _impl.startEditingComment();
            }

            function onClosed(): void {
                _contextMenuLoader.active = false;
            }
        }
    }

    Loader {
        id: _messageBoxLoader

        function askToDeleteComment(index: int): void {
            setSource("MpvqcDeleteCommentMessageBox.qml", {
                mpvqcApplication: null,
                parent: root.messageBoxParent,
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
                _impl.removeRow(index);
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

        sourceComponent: MpvqcSearchBox {
            id: _searchBox

            parent: root

            isApplicationFullScreen: root.isCurrentlyFullScreen

            searchQueryValidator: root.defaultTextValidator
            performModelSearchFunc: _impl.performModelSearch

            onHighlightRequested: index => _impl.select(index)
        }
    }

    Connections {
        target: root.model

        function onCommentsImported(index: int): void {
            _impl.selectQuickly(index);
        }

        function onCommentsImportedUndone(index: int): void {
            _impl.selectQuickly(index);
        }

        function onCommentsClearedUndone(): void {
            const lastIndex = root.count - 1;
            _impl.selectQuickly(lastIndex);
        }

        function onNewCommentAddedInitially(index: int): void {
            _impl.selectQuickly(index);
            _impl.startEditingComment();
        }

        function onNewCommentAddedUndone(index: int): void {
            _impl.selectQuickly(index);
        }

        function onNewCommentAddedRedone(index: int): void {
            _impl.selectQuickly(index);
        }

        function onCommentRemovedUndone(index: int): void {
            _impl.selectQuickly(index);
        }

        function onTimeUpdatedInitially(index: int): void {
            _impl.select(index);
        }

        function onTimeUpdatedUndone(index: int): void {
            _impl.selectQuickly(index);
        }

        function onTimeUpdatedRedone(index: int): void {
            _impl.selectQuickly(index);
        }

        function onCommentTypeUpdated(index: int): void {
            _impl.selectQuickly(index);
        }

        function onCommentTypeUpdatedUndone(index: int): void {
            _impl.selectQuickly(index);
        }

        function onCommentUpdated(index: int): void {
            _impl.selectQuickly(index);
        }

        function onCommentUpdatedUndone(index: int): void {
            _impl.selectQuickly(index);
        }
    }

    Binding {
        target: root.model
        property: "selectedRow"
        value: root.currentIndex
        restoreMode: Binding.RestoreNone
    }
}

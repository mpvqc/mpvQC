// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

import QtQuick

import pyobjects

import "../../utility"

QtObject {
    id: root

    required property bool hasComments
    required property bool isEditing
    required property int currentIndex

    readonly property bool isFullScreen: MpvqcWindowProperties.isFullscreen

    signal editCommentRequested(index: int)
    signal deleteCommentRequested(index: int)
    signal copyCommentRequested(index: int)
    signal searchRequested
    signal undoRequested
    signal redoRequested

    function handleKeyPress(event: KeyEvent): void {
        switch (event.key) {
        case Qt.Key_Return:
            _handleReturnKeyPressed(event);
            break;
        case Qt.Key_Delete:
        case Qt.Key_Backspace:
            _handleDeleteComment(event);
            break;
        case Qt.Key_C:
            _handleCPressed(event);
            break;
        case Qt.Key_F:
            _handleFPressed(event);
            break;
        case Qt.Key_Z:
            _handleZPressed(event);
            break;
        default:
            event.accepted = false;
        }
    }

    function _handleReturnKeyPressed(event: KeyEvent): void {
        if (event.isAutoRepeat) {
            return;
        }
        if (hasComments && !isEditing && !isFullScreen) {
            root.editCommentRequested(currentIndex);
        }
    }

    function _handleDeleteComment(event: KeyEvent): void {
        if (event.isAutoRepeat) {
            return;
        }
        if (hasComments && !isFullScreen) {
            root.deleteCommentRequested(currentIndex);
        }
    }

    function _handleCPressed(event: KeyEvent): void {
        const isCtrlPressed = event.modifiers === Qt.ControlModifier;
        if (isCtrlPressed && !event.isAutoRepeat) {
            if (hasComments && !isEditing && !isFullScreen) {
                root.copyCommentRequested(currentIndex);
                return;
            }
        }
        event.accepted = false;
    }

    function _handleFPressed(event: KeyEvent): void {
        const isCtrlPressed = event.modifiers === Qt.ControlModifier;
        if (isCtrlPressed && !event.isAutoRepeat) {
            if (hasComments && !isEditing && !isFullScreen) {
                root.searchRequested();
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
                root.redoRequested();
            } else {
                root.undoRequested();
            }
            return;
        }
        event.accepted = false;
    }
}

// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

import QtQuick

QtObject {
    id: root

    signal openCommentMenuRequested
    signal toggleFullScreenRequested
    signal forwardKeyToPlayerRequested(key: int, modifiers: int)

    function handleKeyPress(event): void {
        switch (event.key) {
        case Qt.Key_E:
            _handleE(event);
            return;
        case Qt.Key_F:
            _handleF(event);
            return;
        case Qt.Key_C:
            _handleC(event);
            return;
        case Qt.Key_Z:
            _handleZ(event);
            return;
        case Qt.Key_Up:
        case Qt.Key_Down:
        case Qt.Key_Return:
        case Qt.Key_Delete:
        case Qt.Key_Backspace:
            if (_isNoModifier(event)) {
                event.accepted = true;
                return;
            }
            break;
        }
        _forwardToPlayer(event);
    }

    function _handleE(event): void {
        if (_isNoModifier(event)) {
            if (!event.isAutoRepeat) {
                root.openCommentMenuRequested();
            }
            event.accepted = true;
            return;
        }
        _forwardToPlayer(event);
    }

    function _handleF(event): void {
        if (_isNoModifier(event)) {
            if (!event.isAutoRepeat) {
                root.toggleFullScreenRequested();
            }
            event.accepted = true;
            return;
        }
        if (_isOnlyCtrl(event)) {
            event.accepted = true;
            return;
        }
        _forwardToPlayer(event);
    }

    function _handleC(event): void {
        if (_isOnlyCtrl(event)) {
            event.accepted = true;
            return;
        }
        _forwardToPlayer(event);
    }

    function _handleZ(event): void {
        if (_isOnlyCtrl(event) || _isOnlyCtrlShift(event)) {
            event.accepted = true;
            return;
        }
        _forwardToPlayer(event);
    }

    function _forwardToPlayer(event): void {
        root.forwardKeyToPlayerRequested(event.key, event.modifiers);
        event.accepted = true;
    }

    function _effectiveModifiers(event): int {
        return event.modifiers & ~Qt.KeypadModifier;
    }

    function _isNoModifier(event): bool {
        return _effectiveModifiers(event) === Qt.NoModifier;
    }

    function _isOnlyCtrl(event): bool {
        return _effectiveModifiers(event) === Qt.ControlModifier;
    }

    function _isOnlyCtrlShift(event): bool {
        return _effectiveModifiers(event) === (Qt.ControlModifier | Qt.ShiftModifier);
    }
}

// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

import QtQuick

import pyobjects

Loader {
    id: root

    required property var mpvPlayer
    required property bool isFullScreen

    signal addNewCommentMenuRequested
    signal toggleFullScreenRequested

    sourceComponent: Qt.platform.os === "windows" ? _windowsPlayer : _linuxPlayer

    MouseArea {
        id: _mouseArea

        property bool showCursor: true

        property var cursorTimer: Timer {
            running: _mouseArea.showCursor && root.isFullScreen && _mouseArea.containsMouse
            repeat: true
            interval: 2000

            onTriggered: {
                _mouseArea.showCursor = false;
            }
        }

        acceptedButtons: Qt.LeftButton | Qt.MiddleButton | Qt.RightButton
        cursorShape: !_mouseArea.showCursor && root.isFullScreen ? Qt.BlankCursor : Qt.ArrowCursor
        hoverEnabled: true

        anchors.fill: parent

        onPositionChanged: event => {
            _mouseArea.showCursor = true;
            root.mpvPlayer.move_mouse(event.x, event.y);
        }

        onWheel: event => {
            if (event.angleDelta.y > 0) {
                root.mpvPlayer.scroll_up();
            } else {
                root.mpvPlayer.scroll_down();
            }
        }

        onPressed: event => {
            const button = event.button;
            if (button === Qt.LeftButton) {
                root.mpvPlayer.press_mouse_left();
            } else if (button === Qt.MiddleButton) {
                root.mpvPlayer.press_mouse_middle();
            } else if (button === Qt.RightButton) {
                root.addNewCommentMenuRequested();
            }
        }

        onReleased: event => {
            if (event.button === Qt.LeftButton) {
                root.mpvPlayer.release_mouse_left();
            }
        }

        onDoubleClicked: event => {
            if (event.button === Qt.LeftButton) {
                root.toggleFullScreenRequested();
            }
        }
    }

    Component {
        id: _linuxPlayer

        MpvqcMpvFrameBufferObjectPyObject {}
    }

    Component {
        id: _windowsPlayer

        WindowContainer {
            window: MpvWindowPyObject {
                flags: Qt.FramelessWindowHint | Qt.WindowDoesNotAcceptFocus | Qt.WindowTransparentForInput
                color: "black"
            }
        }
    }
}

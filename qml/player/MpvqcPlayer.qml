/*
mpvQC

Copyright (C) 2025 mpvQC developers

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

import QtQuick

import pyobjects

Loader {
    id: root

    required property var mpvPlayer
    required property bool isFullScreen

    readonly property bool isWindows: Qt.platform.os === "windows"

    signal addNewCommentMenuRequested
    signal toggleFullScreenRequested
    signal appWindowActivateRequested

    sourceComponent: isWindows ? _windowsPlayer : _linuxPlayer

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
            if (root.isWindows) {
                // Work around Windows player eating up activate event
                root.appWindowActivateRequested();
            }

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

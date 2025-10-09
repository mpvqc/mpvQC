// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

import QtQuick

import pyobjects

import "../../utility"

Loader {
    id: root

    readonly property MpvqcPlayerViewModel viewModel: MpvqcPlayerViewModel {}
    readonly property bool isFullScreen: MpvqcWindowProperties.isFullscreen

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
            root.viewModel.moveMouse(event.x, event.y);
        }

        onWheel: event => {
            if (event.angleDelta.y > 0) {
                root.viewModel.scrollUp();
            } else {
                root.viewModel.scrollDown();
            }
        }

        onPressed: event => {
            const button = event.button;
            if (button === Qt.LeftButton) {
                root.viewModel.pressMouseLeft();
            } else if (button === Qt.MiddleButton) {
                root.viewModel.pressMouseMiddle();
            } else if (button === Qt.RightButton) {
                root.addNewCommentMenuRequested();
            }
        }

        onReleased: event => {
            if (event.button === Qt.LeftButton) {
                root.viewModel.releaseMouseLeft();
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

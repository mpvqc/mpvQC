// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

import QtQuick

import io.github.mpvqc.mpvQC.Utility

MouseArea {
    id: root

    readonly property bool isFullScreen: MpvqcWindowUtility.isFullscreen
    readonly property bool isWindows: Qt.platform.os === "windows"
    readonly property bool isWindowActive: Window.window ? Window.window.active : true

    property bool showCursor: true

    signal addNewCommentMenuRequested
    signal toggleFullScreenRequested
    signal windowActivationRequested

    signal mouseMoved(real x, real y)
    signal wheelScrolledUp
    signal wheelScrolledDown
    signal leftMousePressed
    signal leftMouseReleased
    signal middleMousePressed
    signal backMousePressed
    signal forwardMousePressed

    property var cursorTimer: Timer {
        running: root.showCursor && root.isFullScreen && root.containsMouse
        repeat: true
        interval: 2000

        onTriggered: {
            root.showCursor = false;
        }
    }

    acceptedButtons: Qt.LeftButton | Qt.MiddleButton | Qt.RightButton | Qt.BackButton | Qt.ForwardButton
    cursorShape: !root.showCursor && root.isFullScreen ? Qt.BlankCursor : Qt.ArrowCursor
    hoverEnabled: true

    onPositionChanged: event => {
        root.showCursor = true;
        root.mouseMoved(event.x, event.y);
    }

    onWheel: event => {
        if (event.angleDelta.y > 0) {
            root.wheelScrolledUp();
        } else {
            root.wheelScrolledDown();
        }
    }

    onPressed: event => {
        if (root.isWindows && !root.isWindowActive) {
            root.windowActivationRequested();
        }

        switch (event.button) {
        case Qt.LeftButton:
            root.leftMousePressed();
            break;
        case Qt.MiddleButton:
            root.middleMousePressed();
            break;
        case Qt.RightButton:
            root.addNewCommentMenuRequested();
            break;
        case Qt.BackButton:
            root.backMousePressed();
            break;
        case Qt.ForwardButton:
            root.forwardMousePressed();
            break;
        }
    }

    onReleased: event => {
        if (event.button === Qt.LeftButton) {
            root.leftMouseReleased();
        }
    }

    onDoubleClicked: event => {
        if (event.button === Qt.LeftButton) {
            root.toggleFullScreenRequested();
        }
    }
}

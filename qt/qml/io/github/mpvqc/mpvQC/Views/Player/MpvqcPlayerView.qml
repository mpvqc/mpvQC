// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

import QtQuick

import io.github.mpvqc.mpvQC.Python

Loader {
    id: root

    readonly property MpvqcPlayerViewModel viewModel: MpvqcPlayerViewModel {}

    readonly property bool isWindows: Qt.platform.os === "windows"
    readonly property bool isTestMode: typeof mpvqcTestMode !== "undefined"

    readonly property url windowsPlayer: Qt.resolvedUrl("MpvqcPlayerWindows.qml")
    readonly property url linuxPlayer: Qt.resolvedUrl("MpvqcPlayerLinux.qml")
    readonly property url stubPlayer: Qt.resolvedUrl("MpvqcPlayerStub.qml")

    signal addNewCommentMenuRequested
    signal toggleFullScreenRequested

    source: isTestMode ? stubPlayer : isWindows ? windowsPlayer : linuxPlayer
    asynchronous: true

    MpvqcPlayerInputArea {
        objectName: "playerInputArea"
        anchors.fill: parent

        onAddNewCommentMenuRequested: root.addNewCommentMenuRequested()
        onToggleFullScreenRequested: root.toggleFullScreenRequested()
        onWindowActivationRequested: Window.window.requestActivate()

        onMouseMoved: (x, y) => root.viewModel.moveMouse(x, y)
        onWheelScrolledUp: root.viewModel.scrollUp()
        onWheelScrolledDown: root.viewModel.scrollDown()
        onLeftMousePressed: root.viewModel.pressMouseLeft()
        onLeftMouseReleased: root.viewModel.releaseMouseLeft()
        onMiddleMousePressed: root.viewModel.pressMouseMiddle()
        onBackMousePressed: root.viewModel.pressMouseBack()
        onForwardMousePressed: root.viewModel.pressMouseForward()
    }

    Rectangle {
        anchors.fill: parent
        color: "black"
    }
}

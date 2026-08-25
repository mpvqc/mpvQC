// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

import QtQuick

import io.github.mpvqc.mpvQC.Python
import io.github.mpvqc.mpvQC.Utility

Loader {
    id: root

    readonly property MpvqcPlayerViewModel viewModel: MpvqcPlayerViewModel {}

    readonly property bool isTestMode: typeof mpvqcTestMode !== "undefined"

    readonly property url embeddedPlayer: Qt.resolvedUrl("MpvqcEmbeddedPlayerWrapper.qml")
    readonly property url inScenePlayer: Qt.resolvedUrl("MpvqcInScenePlayerWrapper.qml")
    readonly property url stubPlayer: Qt.resolvedUrl("MpvqcPlayerStub.qml")

    signal addNewCommentMenuRequested
    signal toggleFullScreenRequested

    source: isTestMode ? stubPlayer : MpvqcPlatform.embedsNativePlayer ? embeddedPlayer : inScenePlayer
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

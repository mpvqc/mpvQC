// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls
import QtQuick.Controls.Material as M

import io.github.mpvqc.mpvQC.Python
import io.github.mpvqc.mpvQC.Utility

Row {
    id: root

    readonly property bool isWindows: Qt.platform.os === "windows"
    readonly property MpvqcWindowButtonsViewModel windowButtons: MpvqcWindowButtonsViewModel {}

    signal minimizeRequested
    signal toggleMaximizeRequested
    signal closeRequested

    ToolButton {
        id: _minimizeButton
        objectName: "minimizeButton"

        visible: root.windowButtons.showMinimizeButton
        height: root.height
        focusPolicy: Qt.NoFocus
        icon.width: 20
        icon.height: 20
        icon.source: MpvqcIcons.minimize

        background: Rectangle {
            implicitWidth: _minimizeButton.M.Material.touchTarget
            color: _minimizeButton.hovered ? Qt.alpha(MpvqcTheme.palette.foreground, 0.08) : "transparent"
        }

        onClicked: root.minimizeRequested()
    }

    ToolButton {
        id: _maximizeButton
        objectName: "maximizeButton"

        readonly property url iconMaximize: MpvqcIcons.openInFull
        readonly property url iconNormalize: MpvqcIcons.closeFullscreen

        visible: root.windowButtons.showMaximizeButton
        height: root.height
        focusPolicy: Qt.NoFocus
        icon.width: 18
        icon.height: 18
        icon.source: MpvqcWindowUtility.isMaximized ? iconNormalize : iconMaximize

        background: Rectangle {
            implicitWidth: _maximizeButton.M.Material.touchTarget
            color: _maximizeButton.hovered ? Qt.alpha(MpvqcTheme.palette.foreground, 0.08) : "transparent"
        }

        onClicked: root.toggleMaximizeRequested()
    }

    ToolButton {
        id: _closeButton
        objectName: "closeButton"

        readonly property color hoverIconColor: root.isWindows ? "#FFFFFD" : MpvqcTheme.palette.errorText
        readonly property color idleIconColor: MpvqcTheme.palette.foreground
        readonly property color backgroundColor: root.isWindows ? "#C42C1E" : MpvqcTheme.palette.error

        visible: root.windowButtons.showCloseButton
        height: root.height
        focusPolicy: Qt.NoFocus

        icon {
            width: 18
            height: 18
            source: MpvqcIcons.close
            color: _closeButton.hovered ? _closeButton.hoverIconColor : _closeButton.idleIconColor
        }

        background: Rectangle {
            implicitWidth: _closeButton.M.Material.touchTarget
            color: _closeButton.hovered ? _closeButton.backgroundColor : "transparent"
        }

        onClicked: root.closeRequested()
    }
}

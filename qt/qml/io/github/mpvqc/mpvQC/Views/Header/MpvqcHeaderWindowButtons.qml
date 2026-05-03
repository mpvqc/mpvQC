// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls.Material

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
        objectName: "minimizeButton"

        visible: root.windowButtons.showMinimizeButton
        height: root.height
        focusPolicy: Qt.NoFocus
        icon.width: 20
        icon.height: 20
        icon.source: MpvqcIcons.minimize

        onClicked: root.minimizeRequested()
    }

    ToolButton {
        objectName: "maximizeButton"

        readonly property url iconMaximize: MpvqcIcons.openInFull
        readonly property url iconNormalize: MpvqcIcons.closeFullscreen

        visible: root.windowButtons.showMaximizeButton
        height: root.height
        focusPolicy: Qt.NoFocus
        icon.width: 18
        icon.height: 18
        icon.source: MpvqcWindowUtility.isMaximized ? iconNormalize : iconMaximize

        onClicked: root.toggleMaximizeRequested()
    }

    ToolButton {
        id: _closeButton
        objectName: "closeButton"

        readonly property color hoverIconColor: root.isWindows ? "#FFFFFD" : MpvqcTheme.background
        readonly property color idleIconColor: MpvqcTheme.foreground
        readonly property color backgroundColor: root.isWindows ? "#C42C1E" : MpvqcTheme.control

        visible: root.windowButtons.showCloseButton
        height: root.height
        focusPolicy: Qt.NoFocus

        icon {
            width: 18
            height: 18
            source: MpvqcIcons.close
            color: _closeButton.hovered ? _closeButton.hoverIconColor : _closeButton.idleIconColor
        }

        onClicked: root.closeRequested()

        Binding {
            when: true
            target: _closeButton.background
            property: "color"
            value: _closeButton.backgroundColor
            restoreMode: Binding.RestoreNone
        }
    }
}

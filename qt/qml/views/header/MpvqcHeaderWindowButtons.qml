// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls.Material

import pyobjects

import "../../utility"

Row {
    id: root

    readonly property bool isWindows: Qt.platform.os === "windows"
    readonly property MpvqcWindowButtons windowButtons: MpvqcWindowButtons {}

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
        icon.source: "qrc:/data/icons/minimize_24dp_1F1F1F_FILL0_wght400_GRAD0_opsz24.svg"

        onClicked: root.minimizeRequested()
    }

    ToolButton {
        objectName: "maximizeButton"

        readonly property url iconMaximize: "qrc:/data/icons/open_in_full_24dp_1F1F1F_FILL0_wght400_GRAD0_opsz24.svg"
        readonly property url iconNormalize: "qrc:/data/icons/close_fullscreen_24dp_1F1F1F_FILL0_wght400_GRAD0_opsz24.svg"

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
            source: "qrc:/data/icons/close_24dp_1F1F1F_FILL0_wght400_GRAD0_opsz24.svg"
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

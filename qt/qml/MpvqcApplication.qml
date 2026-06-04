// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

import QtQuick
import QtQuick.Controls
import QtQuick.Controls.Material as M

import io.github.mpvqc.mpvQC.App
import io.github.mpvqc.mpvQC.Python
import io.github.mpvqc.mpvQC.Utility

ApplicationWindow {
    id: root

    readonly property bool isWindows: Qt.platform.os === "windows"
    readonly property int windowsFlags: Qt.CustomizeWindowHint | Qt.Window
    readonly property int linuxFlags: Qt.FramelessWindowHint | Qt.Window

    flags: isWindows ? windowsFlags : linuxFlags

    width: 1280
    height: 720

    minimumWidth: 960
    minimumHeight: 540

    visible: false
    color: M.Material.background

    font {
        pointSize: 10
        family: 'Noto Sans'
    }

    M.Material.theme: MpvqcTheme.isDark ? M.Material.Dark : M.Material.Light
    M.Material.accent: MpvqcTheme.palette.accent
    M.Material.background: MpvqcTheme.palette.background
    M.Material.foreground: MpvqcTheme.palette.foreground

    LayoutMirroring.enabled: Application.layoutDirection === Qt.RightToLeft
    LayoutMirroring.childrenInherit: true

    Component.onCompleted: root.requestActivate()

    MpvqcApplicationContent {
        id: _content

        anchors.fill: parent

        windowActive: root.active
        windowWidth: root.width

        onCloseRequested: root.close()
        onMinimizeRequested: root.showMinimized()
        onStartSystemMoveRequested: root.startSystemMove()

        onToggleMaximizeRequested: _windowVisibilityHandler.toggleMaximized()
        onToggleFullScreenRequested: _windowVisibilityHandler.toggleFullScreen()
        onDisableFullScreenRequested: _windowVisibilityHandler.disableFullScreen()

        onAppWindowSizeRequested: (width, height) => {
            if (width >= root.minimumWidth && height >= root.minimumHeight) {
                root.width = width;
                root.height = height;
            }
        }
    }

    MpvqcWindowVisibilityViewModel {
        id: _windowVisibilityHandler
    }
}

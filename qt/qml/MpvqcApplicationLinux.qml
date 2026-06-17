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

    readonly property int shadowMargin: _content.viewModel.shadowMargin

    flags: Qt.FramelessWindowHint | Qt.Window

    width: 1280
    height: 720

    minimumWidth: 960
    minimumHeight: 540

    visible: false
    color: "transparent"

    font: MpvqcFonts.applicationFont

    M.Material.theme: MpvqcTheme.isDark ? M.Material.Dark : M.Material.Light
    M.Material.accent: MpvqcTheme.palette.accent
    M.Material.background: MpvqcTheme.palette.background
    M.Material.foreground: MpvqcTheme.palette.foreground

    LayoutMirroring.enabled: Application.layoutDirection === Qt.RightToLeft
    LayoutMirroring.childrenInherit: true

    Component.onCompleted: {
        MpvqcWindowUtility.contentFrame = _content;
        root.requestActivate();
    }

    MpvqcWindowShadow {
        anchors.fill: _frame
        margin: root.shadowMargin
        radius: _frame.radius
        windowActive: root.active
    }

    Rectangle {
        id: _frame

        anchors.fill: parent
        anchors.margins: root.shadowMargin
        radius: MpvqcWindowUtility.windowRadius
        color: M.Material.background

        MpvqcApplicationContent {
            id: _content

            anchors.fill: parent

            windowActive: root.active
            windowWidth: _frame.width

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
    }

    MpvqcWindowVisibilityViewModel {
        id: _windowVisibilityHandler
    }
}

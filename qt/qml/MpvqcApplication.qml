// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

import QtQuick
import QtQuick.Controls
import QtQuick.Controls.Material as M

import io.github.mpvqc.mpvQC.App
import io.github.mpvqc.mpvQC.Utility

ApplicationWindow {
    id: root

    flags: MpvqcPlatform.keepsNativeFrame ? Qt.CustomizeWindowHint | Qt.Window : Qt.FramelessWindowHint | Qt.Window

    width: 1280
    height: 720

    // The minimum is meant for the window geometry; the surface adds the drop shadow margin on both sides.
    minimumWidth: 960 + 2 * MpvqcWindowUtility.dropShadowMargin
    minimumHeight: 540 + 2 * MpvqcWindowUtility.dropShadowMargin

    visible: false
    color: MpvqcPlatform.drawsDropShadow ? "transparent" : M.Material.background

    font: MpvqcFonts.applicationFont

    M.Material.theme: MpvqcAppearance.isDark ? M.Material.Dark : M.Material.Light
    M.Material.accent: MpvqcAppearance.palette.accent
    M.Material.background: MpvqcAppearance.palette.background
    M.Material.foreground: MpvqcAppearance.palette.foreground

    LayoutMirroring.enabled: Application.layoutDirection === Qt.RightToLeft
    LayoutMirroring.childrenInherit: true

    Component.onCompleted: {
        MpvqcWindowUtility.contentFrame = _content;
        root.requestActivate();
    }

    MpvqcWindowDropShadow {
        anchors.fill: _frame
        margin: MpvqcWindowUtility.dropShadowMargin
        radius: _frame.radius
        windowActive: root.active
    }

    Rectangle {
        id: _frame
        objectName: "windowFrame"

        anchors.fill: parent
        anchors.margins: MpvqcWindowUtility.dropShadowMargin
        radius: MpvqcWindowUtility.windowRadius
        color: M.Material.background

        // Overflowing content must not paint into the drop shadow margin.
        clip: MpvqcWindowUtility.dropShadowMargin > 0

        MpvqcApplicationContent {
            id: _content

            anchors.fill: parent

            windowActive: root.active
            windowWidth: _frame.width

            onCloseRequested: root.close()
            onMinimizeRequested: MpvqcWindowUtility.minimize()
            onStartSystemMoveRequested: root.startSystemMove()

            onToggleMaximizeRequested: MpvqcWindowUtility.toggleMaximized()
            onToggleFullScreenRequested: MpvqcWindowUtility.toggleFullScreen()
            onDisableFullScreenRequested: MpvqcWindowUtility.disableFullScreen()

            onAppWindowSizeRequested: (width, height) => {
                if (width >= root.minimumWidth && height >= root.minimumHeight) {
                    root.width = width;
                    root.height = height;
                }
            }
        }
    }
}

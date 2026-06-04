// SPDX-FileCopyrightText: 2017 The Qt Company Ltd.
// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

import QtQuick
import QtQuick.Templates as T
import QtQuick.Controls.impl
import QtQuick.Controls.Material
import QtQuick.Controls.Material.impl

import io.github.mpvqc.mpvQC.Utility

T.ToolButton {
    id: control

    readonly property color _contentColor: !enabled ? MpvqcTheme.palette.hint : checked || highlighted ? Material.accent : Material.foreground

    implicitWidth: Math.max(implicitBackgroundWidth + leftInset + rightInset, implicitContentWidth + leftPadding + rightPadding)
    implicitHeight: Math.max(implicitBackgroundHeight + topInset + bottomInset, implicitContentHeight + topPadding + bottomPadding)

    padding: 6
    spacing: 6

    icon.width: 24
    icon.height: 24

    contentItem: IconLabel {
        spacing: control.spacing
        mirrored: control.mirrored
        display: control.display

        icon: control.icon
        defaultIconColor: control._contentColor
        text: control.text
        font: control.font
        color: control._contentColor
    }

    background: Ripple {
        readonly property bool square: control.contentItem.width <= control.contentItem.height

        implicitWidth: control.Material.touchTarget
        implicitHeight: control.Material.touchTarget

        x: (parent.width - width) / 2
        y: (parent.height - height) / 2
        width: square ? height : parent.width
        height: square ? Math.min(parent.height, 36) : parent.height
        clip: true
        clipRadius: 8
        pressed: control.pressed
        anchor: control
        active: control.enabled && (control.down || control.visualFocus || control.hovered)
        color: Qt.alpha(control._contentColor, 0.1)
    }
}

// SPDX-FileCopyrightText: 2017 The Qt Company Ltd.
// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

import QtQuick
import QtQuick.Templates as T
import QtQuick.Controls.impl as Impl
import QtQuick.Controls.Material as M

T.DialogButtonBox {
    id: control

    implicitWidth: Math.max(implicitBackgroundWidth + leftInset + rightInset, implicitContentWidth + leftPadding + rightPadding)
    implicitHeight: Math.max(implicitBackgroundHeight + topInset + bottomInset, implicitContentHeight + topPadding + bottomPadding)

    spacing: 8
    padding: 8
    verticalPadding: 2
    alignment: Qt.AlignRight
    buttonLayout: T.DialogButtonBox.AndroidLayout

    M.Material.foreground: M.Material.accent
    M.Material.roundedScale: M.Material.ExtraLargeScale

    delegate: Button {
        flat: true
    }

    contentItem: ListView {
        implicitWidth: contentWidth
        model: control.contentModel
        spacing: control.spacing
        orientation: ListView.Horizontal
        boundsBehavior: Flickable.StopAtBounds
        snapMode: ListView.SnapToItem
    }

    background: Impl.PaddedRectangle {
        implicitHeight: control.M.Material.dialogButtonBoxHeight
        radius: control.M.Material.roundedScale
        color: control.M.Material.dialogColor
        // Rounded corners should be only at the top or at the bottom
        topPadding: control.position === T.DialogButtonBox.Footer ? -radius : 0
        bottomPadding: control.position === T.DialogButtonBox.Header ? -radius : 0
        clip: true
    }
}

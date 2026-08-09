// SPDX-FileCopyrightText: 2017 The Qt Company Ltd.
// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls.Material
import QtQuick.Controls.Material.impl
import QtQuick.Templates as T

import io.github.mpvqc.mpvQC.Components
import io.github.mpvqc.mpvQC.Utility

T.CheckBox {
    id: control

    implicitWidth: Math.max(implicitBackgroundWidth + leftInset + rightInset, implicitContentWidth + leftPadding + rightPadding)
    implicitHeight: Math.max(implicitBackgroundHeight + topInset + bottomInset, implicitContentHeight + topPadding + bottomPadding, implicitIndicatorHeight + topPadding + bottomPadding)

    spacing: 8
    padding: 8
    verticalPadding: padding + 7

    indicator: MpvqcCheckIndicator {
        objectName: "checkIndicator"

        x: control.text ? (control.mirrored ? control.width - width - control.rightPadding : control.leftPadding) : control.leftPadding + (control.availableWidth - width) / 2
        y: control.topPadding + (control.availableHeight - height) / 2
        checked: control.checkState === Qt.Checked
        partial: control.checkState === Qt.PartiallyChecked

        Ripple {
            x: (parent.width - width) / 2
            y: (parent.height - height) / 2
            width: 28
            height: 28

            z: -1
            anchor: control
            pressed: control.pressed
            active: enabled && (control.down || control.visualFocus || control.hovered)
            color: control.checked ? control.Material.highlightedRippleColor : control.Material.rippleColor
        }
    }

    contentItem: Text {
        leftPadding: control.indicator && !control.mirrored ? control.indicator.width + control.spacing : 0
        rightPadding: control.indicator && control.mirrored ? control.indicator.width + control.spacing : 0

        text: control.text
        font: control.font
        color: control.enabled ? control.Material.foreground : MpvqcAppearance.palette.hint
        elide: Text.ElideRight
        verticalAlignment: Text.AlignVCenter
    }
}

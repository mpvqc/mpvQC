// SPDX-FileCopyrightText: 2017 The Qt Company Ltd.
// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls.Material
import QtQuick.Controls.Material.impl
import QtQuick.Templates as T

import io.github.mpvqc.mpvQC.Utility

T.Switch {
    id: control

    property bool _animated: false

    implicitWidth: Math.max(implicitBackgroundWidth + leftInset + rightInset, implicitContentWidth + leftPadding + rightPadding)
    implicitHeight: Math.max(implicitBackgroundHeight + topInset + bottomInset, implicitContentHeight + topPadding + bottomPadding, implicitIndicatorHeight + topPadding + bottomPadding)

    spacing: 8
    padding: 8
    verticalPadding: padding - 1

    indicator: Rectangle {
        objectName: "switchIndicator"

        x: control.text ? (control.mirrored ? control.width - width - control.rightPadding : control.leftPadding) : control.leftPadding + (control.availableWidth - width) / 2
        y: control.topPadding + (control.availableHeight - height) / 2

        implicitWidth: 36
        implicitHeight: 20
        radius: height / 2
        // No disabled look: the indicator keeps its full colors while the control is disabled.
        color: control.checked ? MpvqcAppearance.palette.accent : "transparent"
        border.width: control.checked ? 0 : 2
        border.color: MpvqcAppearance.palette.hint

        Ripple {
            readonly property color _haloColor: control.checked ? control.Material.highlightedRippleColor : control.Material.rippleColor

            x: _thumb.x + (_thumb.width - width) / 2
            y: _thumb.y + (_thumb.height - height) / 2
            width: 28
            height: 28

            z: -1
            anchor: control
            pressed: control.pressed
            active: enabled && (control.down || control.visualFocus || control.hovered)
            color: control.down || control.visualFocus ? _haloColor : Qt.alpha(_haloColor, _haloColor.a / 2)
        }

        Rectangle {
            id: _thumb
            objectName: "switchThumb"

            property real centerX: parent.height / 2 + control.visualPosition * (parent.width - parent.height)

            x: centerX - width / 2
            y: (parent.height - height) / 2
            width: control.checked ? 14 : 10
            height: width
            radius: width / 2
            color: control.checked ? MpvqcAppearance.palette.dialogBackground : MpvqcAppearance.palette.hint

            Behavior on centerX {
                enabled: control._animated && !control.pressed

                NumberAnimation {
                    duration: 240
                    easing.type: Easing.OutBack
                    easing.overshoot: 1.2
                }
            }

            Behavior on width {
                enabled: control._animated

                NumberAnimation {
                    duration: control.checked ? 240 : 100
                    easing.type: control.checked ? Easing.OutBack : Easing.OutCubic
                    easing.overshoot: 1.2
                }
            }

            Behavior on color {
                enabled: control._animated

                ColorAnimation {
                    duration: 120
                }
            }
        }

        Behavior on color {
            enabled: control._animated

            ColorAnimation {
                duration: 120
            }
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

    Component.onCompleted: control._animated = true
}

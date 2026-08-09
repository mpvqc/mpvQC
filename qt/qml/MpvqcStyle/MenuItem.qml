// SPDX-FileCopyrightText: 2017 The Qt Company Ltd.
// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls.Material
import QtQuick.Controls.Material.impl
import QtQuick.Controls.impl
import QtQuick.Templates as T

import io.github.mpvqc.mpvQC.Components

T.MenuItem {
    id: control

    implicitWidth: Math.max(implicitBackgroundWidth + leftInset + rightInset, implicitContentWidth + leftPadding + rightPadding)
    implicitHeight: Math.max(implicitBackgroundHeight + topInset + bottomInset, implicitContentHeight + topPadding + bottomPadding, implicitIndicatorHeight + topPadding + bottomPadding)

    padding: 16
    verticalPadding: Material.menuItemVerticalPadding
    spacing: 16

    icon.width: 24
    icon.height: 24

    indicator: Item {
        x: control.text ? (control.mirrored ? control.width - width - control.rightPadding : control.leftPadding) : control.leftPadding + (control.availableWidth - width) / 2
        y: control.topPadding + (control.availableHeight - height) / 2

        implicitWidth: 20
        implicitHeight: 20
        visible: control.checkable

        MpvqcRadioIndicator {
            objectName: "radioIndicator"

            anchors.fill: parent

            // A checkable Action in an exclusive ActionGroup never sets autoExclusive here, so it would draw the check mark, not the dot.
            visible: control.autoExclusive
            selected: control.checked
        }

        MpvqcCheckIndicator {
            objectName: "checkIndicator"

            anchors.fill: parent

            visible: !control.autoExclusive
            checked: control.checked
        }
    }

    arrow: ColorImage {
        x: control.mirrored ? control.padding : control.width - width - control.padding
        y: control.topPadding + (control.availableHeight - height) / 2

        visible: control.subMenu
        mirror: control.mirrored
        color: control.enabled ? control.Material.foreground : control.Material.hintTextColor
        source: "qrc:/qt-project.org/imports/QtQuick/Controls/Material/images/arrow-indicator.png"
    }

    contentItem: IconLabel {
        readonly property real arrowPadding: control.subMenu && control.arrow ? control.arrow.width + control.spacing : 0
        readonly property real indicatorPadding: control.checkable && control.indicator ? control.indicator.width + control.spacing : 0

        leftPadding: !control.mirrored ? indicatorPadding : arrowPadding
        rightPadding: control.mirrored ? indicatorPadding : arrowPadding
        spacing: control.spacing
        mirrored: control.mirrored
        display: control.display
        alignment: Qt.AlignLeft

        icon: control.icon
        defaultIconColor: control.enabled ? control.Material.foreground : control.Material.hintTextColor
        text: control.text
        font: control.font
        color: defaultIconColor
    }

    background: Rectangle {
        implicitWidth: 200
        implicitHeight: control.Material.menuItemHeight
        color: control.highlighted ? control.Material.listHighlightColor : "transparent"

        Ripple {
            width: parent.width
            height: parent.height

            clip: visible
            pressed: control.pressed
            anchor: control
            active: control.down || control.highlighted
            color: control.Material.rippleColor
        }
    }
}

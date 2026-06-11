// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

import QtQuick
import QtQuick.Controls
import QtQuick.Controls.impl

import io.github.mpvqc.mpvQC.Utility

Control {
    id: root

    property string text: ""
    property string icon: ""

    readonly property var _icons: ({
            "return": MpvqcIcons.keyboardReturn,
            "backspace": MpvqcIcons.keyboardBackspace,
            "arrowUp": MpvqcIcons.keyboardArrowUp,
            "arrowDown": MpvqcIcons.keyboardArrowDown,
            "arrowLeft": MpvqcIcons.keyboardArrowLeft,
            "arrowRight": MpvqcIcons.keyboardArrowRight,
            "space": MpvqcIcons.spaceBar
        })

    readonly property url _iconSource: icon ? _icons[icon] ?? "" : ""

    readonly property int _iconSize: 18
    readonly property int _minimumWidth: _iconSize + leftPadding + rightPadding

    implicitWidth: Math.max(Math.ceil(implicitContentWidth) + leftPadding + rightPadding, _minimumWidth)
    implicitHeight: Math.max(Math.ceil(implicitContentHeight) + topPadding + bottomPadding, _iconSize + topPadding + bottomPadding)

    horizontalPadding: 10
    verticalPadding: 6

    contentItem: IconLabel {
        text: root.text
        font: root.font
        color: MpvqcTheme.palette.foreground
        icon.source: root._iconSource
        icon.color: MpvqcTheme.palette.foreground
        icon.width: root._iconSize
        icon.height: root._iconSize
        display: root.text ? IconLabel.TextOnly : IconLabel.IconOnly
    }

    background: Rectangle {
        radius: 4
        color: Qt.alpha(MpvqcTheme.palette.foreground, MpvqcTheme.isDark ? 0.08 : 0.12)
    }
}

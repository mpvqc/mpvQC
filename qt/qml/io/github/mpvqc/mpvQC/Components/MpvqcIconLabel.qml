// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

import QtQuick
import QtQuick.Controls
import QtQuick.Controls.impl

import io.github.mpvqc.mpvQC.Utility

IconLabel {
    id: root

    property alias iconColor: root.icon.color

    property string toolTipText: ""

    display: IconLabel.IconOnly

    icon.color: MpvqcAppearance.palette.accent

    ToolTip.delay: 350
    ToolTip.text: root.toolTipText
    ToolTip.visible: root.toolTipText && _hover.hovered

    HoverHandler {
        id: _hover
        cursorShape: root.toolTipText ? Qt.PointingHandCursor : undefined
    }
}

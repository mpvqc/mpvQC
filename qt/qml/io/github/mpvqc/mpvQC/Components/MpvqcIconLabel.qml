// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

import QtQuick
import QtQuick.Controls
import QtQuick.Controls.impl

import io.github.mpvqc.mpvQC.Utility

IconLabel {
    id: root

    property string toolTipText: ""
    property alias iconColor: root.icon.color

    display: IconLabel.IconOnly

    icon.color: MpvqcTheme.palette.accent

    ToolTip.delay: 350
    ToolTip.text: root.toolTipText
    ToolTip.visible: root.toolTipText && _hover.hovered

    HoverHandler {
        id: _hover
        cursorShape: root.toolTipText ? Qt.PointingHandCursor : undefined
    }
}

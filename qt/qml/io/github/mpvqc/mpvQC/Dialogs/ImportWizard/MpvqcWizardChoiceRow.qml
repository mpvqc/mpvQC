// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import io.github.mpvqc.mpvQC.Components
import io.github.mpvqc.mpvQC.Utility

MpvqcRoundedItemDelegate {
    id: root

    default property alias rowContent: _content.data

    property bool selected: false

    property string toolTipText
    property bool toolTipSuppressed: false

    highlighted: selected

    contentItem: RowLayout {
        id: _content

        spacing: MpvqcConstants.listRowContentSpacing
    }

    ToolTip.text: root.toolTipText
    ToolTip.visible: root.toolTipText !== "" && root.hovered && !root.toolTipSuppressed
    ToolTip.delay: MpvqcConstants.tooltipDelay

    HoverHandler {
        cursorShape: Qt.PointingHandCursor
    }
}

// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import io.github.mpvqc.mpvQC.Components
import io.github.mpvqc.mpvQC.Utility

ItemDelegate {
    id: root

    property string supportingText: ""
    property url link: ""

    readonly property bool _hasLink: link.toString() !== ""

    enabled: _hasLink

    contentItem: RowLayout {
        spacing: 16

        MpvqcIconLabel {
            icon.source: root.icon.source
            icon.width: root.icon.width
            icon.height: root.icon.height
        }

        ColumnLayout {
            spacing: 2

            Layout.fillWidth: true

            Label {
                text: root.text
                color: MpvqcTheme.palette.foreground
                wrapMode: Text.WrapAtWordBoundaryOrAnywhere
                horizontalAlignment: Text.AlignLeft

                Layout.fillWidth: true
            }

            Label {
                objectName: "supportingLabel"
                text: root.supportingText
                color: MpvqcTheme.palette.hint
                font.pointSize: root.font.pointSize - 1
                wrapMode: Text.WordWrap
                horizontalAlignment: Text.AlignLeft
                visible: text !== ""

                Layout.fillWidth: true
            }
        }

        MpvqcIconLabel {
            objectName: "linkIndicator"
            visible: root._hasLink
            icon.source: MpvqcIcons.openInNew
            icon.width: 18
            icon.height: 18
            iconColor: MpvqcTheme.palette.hint
        }
    }

    ToolTip.delay: MpvqcConstants.tooltipDelay
    ToolTip.text: link.toString()
    ToolTip.visible: hovered && _hasLink

    HoverHandler {
        enabled: root._hasLink
        cursorShape: Qt.PointingHandCursor
    }
}

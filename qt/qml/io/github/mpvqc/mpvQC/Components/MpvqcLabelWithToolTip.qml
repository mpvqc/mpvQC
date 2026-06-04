// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import io.github.mpvqc.mpvQC.Utility

RowLayout {
    id: root

    property alias text: _label.text
    property string toolTip

    spacing: toolTip ? 8 : 0

    Label {
        id: _label

        Layout.fillWidth: true

        horizontalAlignment: Text.AlignRight
        wrapMode: Text.Wrap
    }

    MpvqcIconLabel {
        Layout.preferredWidth: visible ? implicitWidth : 0

        visible: root.toolTip
        toolTipText: root.toolTip

        icon {
            source: MpvqcIcons.tooltip2
            width: 18
            height: 18
            color: MpvqcTheme.palette.hint
        }
    }
}

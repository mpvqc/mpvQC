// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls

TabButton {
    id: root

    implicitWidth: implicitContentWidth
    implicitHeight: Math.max(_label.minimumHeight, implicitContentHeight)
    padding: 0
    leftPadding: 0
    rightPadding: 0
    verticalPadding: 0
    topInset: 0
    bottomInset: 0
    font.weight: Font.Normal

    contentItem: MpvqcPillButtonLabel {
        id: _label

        control: root
    }

    background: MpvqcPillButtonBackground {
        control: root
    }
}

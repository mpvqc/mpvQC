// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls
import QtQuick.Templates as T

import io.github.mpvqc.mpvQC.Utility

Label {
    id: root

    required property T.AbstractButton control

    readonly property int minimumHeight: 48

    text: root.control.text
    textFormat: Text.PlainText
    font: root.control.font
    padding: 10
    color: !root.control.enabled ? MpvqcAppearance.palette.hint : root.control.checked ? MpvqcAppearance.palette.accent : MpvqcAppearance.palette.foreground
    horizontalAlignment: Text.AlignHCenter
    verticalAlignment: Text.AlignVCenter
    wrapMode: Text.Wrap
}

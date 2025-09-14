// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

import QtQuick
import QtQuick.Controls.Material

Button {
    readonly property bool hasContent: text || icon.source.toString()

    enabled: false
    visible: hasContent
    height: hasContent ? implicitHeight : 0
    width: hasContent ? implicitWidth : 0
}

// SPDX-FileCopyrightText: 2017 The Qt Company Ltd.
// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

import QtQuick
import QtQuick.Templates as T

import io.github.mpvqc.mpvQC.Utility

T.ToolSeparator {
    id: control

    implicitWidth: Math.max(implicitBackgroundWidth + leftInset + rightInset, implicitContentWidth + leftPadding + rightPadding)
    implicitHeight: Math.max(implicitBackgroundHeight + topInset + bottomInset, implicitContentHeight + topPadding + bottomPadding)

    horizontalPadding: vertical ? 12 : 5
    verticalPadding: vertical ? 5 : 12

    contentItem: Rectangle {
        implicitWidth: control.vertical ? 1 : 38
        implicitHeight: control.vertical ? 38 : 1
        color: MpvqcTheme.palette.separator
    }
}

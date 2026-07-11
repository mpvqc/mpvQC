// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma Singleton

import QtQuick

QtObject {

    // Native popup windows float above the main window and can leave its
    // geometry. On Windows they are also why the platform backend's window
    // reveal capability must cover transient windows against white flashes.
    readonly property bool usesWindowedPopups: Qt.platform.os === "windows"

    readonly property int smallDialogContentWidth: 370
    readonly property int mediumDialogContentWidth: 500
    readonly property int smallDialogContentHeight: 450
    readonly property int mediumDialogContentHeight: 540

    readonly property int listRowHeight: 44

    readonly property int popupWindowEdgeMargin: 8
    readonly property int tooltipDelay: 350
}

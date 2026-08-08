// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma Singleton

import QtQuick
import QtQuick.Controls

QtObject {

    // On Windows the player is a native child window and paints over the scene,
    // so popups have to be windows of their own to stay visible above it.
    // Everywhere else the player renders in-scene, and in-scene popups stay the
    // better choice while Qt's popup windows carry bugs like QTBUG-145585.
    readonly property int preferredPopupType: Qt.platform.os === "windows" ? Popup.Window : Popup.Item

    // Stacking order inside the window overlay, low to high.
    readonly property int zInlineEditor: 0
    readonly property int zSearchBox: 1
    readonly property int zModal: 2
    readonly property int zTooltip: 10

    readonly property int smallDialogContentWidth: 370
    readonly property int mediumDialogContentWidth: 500
    readonly property int smallDialogContentHeight: 450
    readonly property int mediumDialogContentHeight: 540

    readonly property int listRowHeight: 44
    readonly property int listRowVerticalPadding: 10
    readonly property int listRowHorizontalPadding: 14
    readonly property int listRowContentSpacing: 12

    readonly property int popupWindowEdgeMargin: 8
    readonly property int tooltipDelay: 350

    // The import wizard's pager pill and its card edge move together, so they share one curve
    readonly property int wizardStepMotionDuration: 220
}

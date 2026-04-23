// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

import QtQuick
import QtQuick.Controls.Material

import "../../components"
import "../../utility"

MpvqcMenu {
    id: root

    required property bool isDefaultFormatChecked
    required property bool isCurrentTimeChecked
    required property bool isRemainingTimeChecked
    required property bool isHideTimeChecked
    required property bool isPercentChecked

    signal defaultFormatPicked
    signal currentTimePicked
    signal remainingTimePicked
    signal hideTimePicked
    signal percentToggled

    modal: true

    Material.background: MpvqcTheme.backgroundAlternate
    Material.foreground: MpvqcTheme.foregroundAlternate

    MenuItem {
        objectName: "defaultFormatMenuItem"

        text: qsTranslate("MainWindow", "Default format")
        checked: root.isDefaultFormatChecked
        autoExclusive: true
        checkable: true

        onTriggered: root.defaultFormatPicked()
    }

    MenuItem {
        objectName: "currentTimeMenuItem"

        text: qsTranslate("MainWindow", "Current time")
        checked: root.isCurrentTimeChecked
        autoExclusive: true
        checkable: true

        onTriggered: root.currentTimePicked()
    }

    MenuItem {
        objectName: "remainingTimeMenuItem"

        text: qsTranslate("MainWindow", "Remaining time")
        checked: root.isRemainingTimeChecked
        autoExclusive: true
        checkable: true

        onTriggered: root.remainingTimePicked()
    }

    MenuItem {
        objectName: "hideTimeMenuItem"

        text: qsTranslate("MainWindow", "Hide time")
        checked: root.isHideTimeChecked
        autoExclusive: true
        checkable: true

        onTriggered: root.hideTimePicked()
    }

    MenuSeparator {}

    MenuItem {
        id: _percentMenuItem
        objectName: "percentMenuItem"

        text: qsTranslate("MainWindow", "Progress in percent")
        checkable: true

        onTriggered: root.percentToggled()
    }

    // Workaround for QTBUG-145585: on Windows the Popup.Window menu can
    // deliver a spurious release event while closing, causing MenuItem to
    // auto-toggle a second time and leaving `checked` out of sync with the
    // view-model. Force-resync on both lifecycle edges:
    //   - aboutToShow: pick up any external changes made while closed.
    //   - closed:      undo the spurious toggle delivered during close.
    onAboutToShow: _percentMenuItem.checked = root.isPercentChecked
    onClosed: _percentMenuItem.checked = root.isPercentChecked
}

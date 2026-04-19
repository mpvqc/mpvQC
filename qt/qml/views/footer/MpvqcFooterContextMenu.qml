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
        objectName: "percentMenuItem"

        text: qsTranslate("MainWindow", "Progress in percent")
        checked: root.isPercentChecked
        checkable: true

        onTriggered: root.percentToggled()
    }
}

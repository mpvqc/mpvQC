// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

import QtQuick
import QtQuick.Controls.Material

Menu {
    id: root

    readonly property bool mMirrored: count > 0 && (itemAt(0) as MenuItem).mirrored
    readonly property bool isWindows: Qt.platform.os === "windows"

    z: 2
    x: mMirrored ? -width + parent.width : 0
    popupType: isWindows ? Popup.Window : Popup.Item
    dim: false

    width: calculateMenuWidths()

    function calculateMenuWidths(): int {
        // Adapted from: https://martin.rpdev.net/2018/03/13/qt-quick-controls-2-automatically-set-the-width-of-menus.html
        let result = 0;
        let padding = 0;
        for (let i = 0; i < count; ++i) {
            let item = itemAt(i) as MenuItem;

            if (item && !isMenuSeparator(item)) {
                result = Math.max(item.contentItem.implicitWidth, result);
                padding = Math.max(item.padding, padding);
            }
        }
        return (result + padding * 2) * 1.03;
    }

    function isMenuSeparator(item: Item): bool {
        return item instanceof MenuSeparator;
    }

    // *********************************************************
    // fixme: Workaround QTBUG-131786 to fake modal behavior on Windows
    onAboutToShow: {
        if (isWindows) {
            enableFakeModal(); // qmllint disable
        }
    }

    onAboutToHide: {
        if (isWindows) {
            disableFakeModal(); // qmllint disable
        }
    }
    // *********************************************************

    Binding {
        when: root.isWindows
        target: root
        property: "enter"
        value: null
        restoreMode: Binding.RestoreNone
    }

    Binding {
        when: root.isWindows
        target: root
        property: "exit"
        value: null
        restoreMode: Binding.RestoreNone
    }
}

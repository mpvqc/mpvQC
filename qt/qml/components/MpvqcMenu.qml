// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

import QtQuick
import QtQuick.Controls.Material

import "../utility"

Menu {
    id: root // todo check if it can be removed by using parent on its usages

    readonly property bool isMirrored: Application.layoutDirection === Qt.RightToLeft
    readonly property bool isWindows: Qt.platform.os === "windows"

    z: 2
    transformOrigin: isMirrored ? Popup.TopRight : Popup.TopLeft
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

    // *********************************************************
    // fixme: Workaround QTBUG-139603 to fix theme propagation bug
    font {
        pointSize: 10
        family: 'Noto Sans'
    }
    Material.theme: MpvqcTheme.isDark ? Material.Dark : Material.Light
    Material.accent: MpvqcTheme.control
    Material.background: MpvqcTheme.background
    Material.foreground: MpvqcTheme.foreground
    // *********************************************************

    Binding {
        when: root.popupType === Popup.Window && root.contentItem
        target: root.contentItem
        property: "LayoutMirroring.enabled"
        value: root.isMirrored
        restoreMode: Binding.RestoreNone
    }

    Binding {
        when: root.popupType === Popup.Window && root.contentItem
        target: root.contentItem
        property: "LayoutMirroring.childrenInherit"
        value: true
        restoreMode: Binding.RestoreNone
    }
}

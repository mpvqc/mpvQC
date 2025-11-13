// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

import QtQuick
import QtQuick.Controls.Material
import QtQuick.Layouts

import "../../utility"

Item {
    id: root

    readonly property int configuredHeight: 43

    default property alias menuBarContent: _menuBar.contentData

    property bool expanded: {
        if (MpvqcWindowUtility.isMaximized || _menuBar.hovered) {
            return true;
        }
        for (const menu of _menuBar.menus) {
            if (menu.visible) {
                return true;
            }
        }
        return false;
    }

    width: _background.width
    height: configuredHeight

    function openFirstMenu(): void {
        for (let i = 0; i < _menuBar.contentData.length; i++) {
            const item = _menuBar.contentData[i]
            if (item instanceof MenuBarItem) {
                item.triggered()
                break
            }
        }
    }

    RowLayout {
        id: _background

        ToolButton {
            id: _hamburgerButton

            width: root.configuredHeight
            height: root.configuredHeight
            visible: !root.expanded

            icon.source: "qrc:/data/icons/menu_24dp_1F1F1F_FILL0_wght400_GRAD0_opsz24.svg"
            icon.width: 20
            icon.height: 20

            flat: true
            display: AbstractButton.IconOnly

            onHoveredChanged: {
                if (hovered) {
                    openFirstMenu()
                }
            }
        }

        Item {
            id: _menuBarWrapper

            clip: true
            height: root.configuredHeight
            width: root.expanded ? _menuBar.implicitWidth : 0
            visible: width > 0

            Behavior on width {
                NumberAnimation {
                    duration: 150
                    easing.type: Easing.OutCubic
                }
            }

            MenuBar {
                id: _menuBar
            }
        }
    }
}

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
            const item = _menuBar.contentData[i];
            if (item instanceof MenuBarItem) {
                item.triggered();
                break;
            }
        }
    }

    Item {
        id: _background

        width: _hamburgerButton.width + _menuBarWrapper.width + _toolbar.width
        height: root.configuredHeight

        ToolButton {
            id: _hamburgerButton

            anchors.left: parent.left
            width: root.expanded ? 0 : root.configuredHeight
            height: root.configuredHeight
            visible: !root.expanded

            icon.source: "qrc:/data/icons/menu_24dp_1F1F1F_FILL0_wght400_GRAD0_opsz24.svg"
            icon.width: 20
            icon.height: 20

            flat: true
            display: AbstractButton.IconOnly

            onHoveredChanged: {
                if (hovered) {
                    openFirstMenu();
                }
            }
        }

        Item {
            id: _menuBarWrapper

            anchors.left: _hamburgerButton.right
            clip: true
            height: root.configuredHeight
            width: root.expanded ? _menuBar.implicitWidth : 0
            visible: width > 0

            Behavior on width {
                NumberAnimation {
                    duration: 200
                    easing.type: Easing.OutCubic
                }
            }

            MenuBar {
                id: _menuBar
            }
        }

        RowLayout {
            id: _toolbar

            anchors.left: _menuBarWrapper.right
            height: root.configuredHeight
            spacing: 0

            Rectangle {
                Layout.preferredWidth: 1
                Layout.preferredHeight: parent.height * 0.8
                Layout.alignment: Qt.AlignVCenter
                color: Material.dividerColor
            }

            ToolButton {
                Layout.preferredWidth: implicitWidth
                Layout.preferredHeight: root.configuredHeight

                icon.source: "qrc:/data/icons/keyboard_arrow_left_24dp_1F1F1F_FILL0_wght400_GRAD0_opsz24.svg"
                icon.width: 22
                icon.height: 22

                ToolTip.delay: 350
                ToolTip.text: qsTranslate("ToolBar", "Frame Step Backward")
                ToolTip.visible: hovered
            }

            ToolButton {
                Layout.preferredWidth: implicitWidth
                Layout.preferredHeight: root.configuredHeight

                icon.source: "qrc:/data/icons/keyboard_arrow_right_24dp_1F1F1F_FILL0_wght400_GRAD0_opsz24.svg"
                icon.width: 22
                icon.height: 22

                ToolTip.delay: 350
                ToolTip.text: qsTranslate("ToolBar", "Frame Step Forward")
                ToolTip.visible: hovered
            }

            Rectangle {
                Layout.preferredWidth: 1
                Layout.preferredHeight: parent.height * 0.8
                Layout.alignment: Qt.AlignVCenter
                color: Material.dividerColor
            }
        }
    }
}

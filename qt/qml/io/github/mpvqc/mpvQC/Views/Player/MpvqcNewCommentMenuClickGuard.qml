// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

// Workaround for QTBUG-145585: On Windows, Popup.Window menus do not respect
// the modal property, allowing clicks to pass through to underlying items.
// This item lives in the window overlay layer and intercepts every click
// while the new-comment menu is open, closing it and swallowing the event
// so nothing underneath reacts.
//
// The _menuOpen flag is cleared via Qt.callLater instead of directly in
// onClosed because the signal is delivered immediately; without the deferral
// the overlay would be gone before the click arrives.
//
// TODO: Remove this file when Qt fixes QTBUG-145585.

import QtQuick
import QtQuick.Controls

Item {
    id: root

    required property var menu

    property bool _menuOpen: false

    parent: Overlay.overlay
    anchors.fill: parent
    visible: Qt.platform.os === "windows" && _menuOpen

    Connections {
        target: root.menu

        function onAboutToShow(): void {
            root._menuOpen = true;
        }

        function onClosed(): void {
            Qt.callLater(() => {
                root._menuOpen = false;
            });
        }
    }

    MouseArea {
        anchors.fill: parent
        acceptedButtons: Qt.LeftButton | Qt.RightButton

        onPressed: event => {
            event.accepted = true;
            root._menuOpen = false;
            root.menu.close();
        }
    }
}

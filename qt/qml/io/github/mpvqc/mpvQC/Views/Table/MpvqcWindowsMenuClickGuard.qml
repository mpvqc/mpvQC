// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

// Workaround for QTBUG-145585: On Windows, Popup.Window menus do not respect
// the modal property, allowing clicks to pass through to underlying items.
// This item lives in the window overlay layer (above all delegates) and
// intercepts every click while a menu is open, closing it and swallowing the
// event so nothing underneath reacts. Only menus are affected; plain Popup
// items (time editor, message boxes, dialogs) are not covered here.
//
// TODO: Remove this file when Qt fixes QTBUG-145585.

import QtQuick
import QtQuick.Controls

Item {
    id: root

    required property Loader editLoader
    required property Loader contextMenuLoader

    parent: Overlay.overlay
    anchors.fill: parent
    visible: Qt.platform.os === "windows" && (editLoader.isEditingCommentType || contextMenuLoader.active)

    MouseArea {
        anchors.fill: parent
        acceptedButtons: Qt.LeftButton | Qt.RightButton

        onPressed: event => {
            event.accepted = true;
            if (root.editLoader.isEditingCommentType && root.editLoader.item) {
                root.editLoader.item.close();
            } else if (root.contextMenuLoader.active && root.contextMenuLoader.item) {
                root.contextMenuLoader.item.close();
            }
        }
    }
}

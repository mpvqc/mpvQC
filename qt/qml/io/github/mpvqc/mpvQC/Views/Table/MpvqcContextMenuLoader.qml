// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls.Material

import io.github.mpvqc.mpvQC.Components
import io.github.mpvqc.mpvQC.Utility

Loader {
    id: root

    property int currentListIndex: -1
    property point openedAt: Qt.point(0, 0)

    property bool _actionTriggered: false

    signal editCommentRequested(index: int)
    signal copyCommentRequested(index: int)
    signal deleteCommentRequested(index: int)
    signal dismissed

    function show(index: int, coordinates: point): void {
        root._actionTriggered = false;
        root.currentListIndex = index;
        root.openedAt = coordinates;
        root.active = true;
    }

    function dismiss(): void {
        (root.item as MpvqcPositionedMenu)?.close();
    }

    active: false
    visible: active

    sourceComponent: _contextMenuComponent

    onLoaded: (item as MpvqcPositionedMenu).open()

    Component {
        id: _contextMenuComponent

        MpvqcPositionedMenu {
            id: _menu
            objectName: "commentContextMenu"

            position: root.openedAt

            Material.background: MpvqcTheme.backgroundAlternate
            Material.foreground: MpvqcTheme.foregroundAlternate

            onClosed: {
                root.active = false;
                if (!root._actionTriggered) {
                    root.dismissed();
                }
            }

            MenuItem {
                objectName: "editCommentAction"

                //: Context menu on right click in comments table
                text: qsTranslate("CommentTable", "Edit Comment")
                icon.source: MpvqcIcons.edit

                onTriggered: {
                    root._actionTriggered = true;
                    _menu.exit = null;
                    _menu.deferToOnClose = () => root.editCommentRequested(root.currentListIndex);
                }
            }

            MenuItem {
                objectName: "copyCommentAction"

                //: Context menu on right click in comments table
                text: qsTranslate("CommentTable", "Copy Comment")
                icon.source: MpvqcIcons.contentCopy

                onTriggered: {
                    root._actionTriggered = true;
                    _menu.deferToOnClose = () => root.copyCommentRequested(root.currentListIndex);
                }
            }

            MenuItem {
                objectName: "deleteCommentAction"

                //: Context menu on right click in comments table
                text: qsTranslate("CommentTable", "Delete Comment")
                icon.source: MpvqcIcons.delete_

                onTriggered: {
                    root._actionTriggered = true;
                    _menu.exit = null;
                    _menu.deferToOnClose = () => root.deleteCommentRequested(root.currentListIndex);
                }
            }
        }
    }
}

// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

import QtQuick
import QtQuick.Controls.Material

import "../../components"

Loader {
    id: root

    required property var viewModel

    property int currentListIndex: -1
    property point openedAt: Qt.point(0, 0)

    active: false
    visible: active

    sourceComponent: _contextMenuComponent

    onLoaded: item.open() // qmllint disable

    Component {
        id: _contextMenuComponent

        MpvqcMenu {
            id: _menu

            property var _deferToOnClose: () => {}

            modal: true

            y: root.openedAt.y

            onAboutToShow: {
                x = _menu.isMirrored ? root.openedAt.x - width : root.openedAt.x;
            }

            onClosed: {
                // Run the stored callback.
                // Required for Windows as closing animation interferes with signal handling
                _menu._deferToOnClose(); // qmllint disable
                _menu._deferToOnClose = () => {};
                root.active = false;
            }

            MenuItem {
                //: Context menu on right click in comments table
                text: qsTranslate("CommentTable", "Edit Comment")
                icon.source: "qrc:/data/icons/edit_24dp_1F1F1F_FILL0_wght400_GRAD0_opsz24.svg"

                onTriggered: {
                    _menu.exit = null;
                    _menu._deferToOnClose = () => root.viewModel.startEditingComment(root.currentListIndex);
                }
            }

            MenuItem {
                //: Context menu on right click in comments table
                text: qsTranslate("CommentTable", "Copy Comment")
                icon.source: "qrc:/data/icons/content_copy_24dp_1F1F1F_FILL0_wght400_GRAD0_opsz24.svg"

                onTriggered: {
                    _menu._deferToOnClose = () => root.viewModel.copyToClipboard(root.currentListIndex);
                }
            }

            MenuItem {
                //: Context menu on right click in comments table
                text: qsTranslate("CommentTable", "Delete Comment")
                icon.source: "qrc:/data/icons/delete_24dp_1F1F1F_FILL0_wght400_GRAD0_opsz24.svg"

                onTriggered: {
                    _menu.exit = null;
                    _menu._deferToOnClose = () => root.viewModel.askToDeleteRow(root.currentListIndex);
                }
            }
        }
    }

    Connections {
        target: root.viewModel

        function onContextMenuRequested(index: int, coordinates: point): void {
            root.currentListIndex = index;
            root.openedAt = coordinates;
            root.active = true;
        }
    }
}

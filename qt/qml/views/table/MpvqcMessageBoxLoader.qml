// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls.Material

import "../../components"

Loader {
    id: root

    required property var viewModel

    property int commentIndex: -1

    signal closed

    active: false
    visible: active

    sourceComponent: _messageBoxComponent

    onLoaded: item.open() // qmllint disable

    Component {
        id: _messageBoxComponent

        MpvqcMessageBox {
            title: qsTranslate("MessageBoxes", "Delete Comment")
            text: qsTranslate("MessageBoxes", "Do you really want to delete this comment?")
            standardButtons: Dialog.Yes | Dialog.Cancel

            onAccepted: {
                root.viewModel.removeRow(root.commentIndex);
            }

            onClosed: {
                root.active = false;
                root.closed();
            }
        }
    }

    Connections {
        target: root.viewModel

        function onDeleteCommentRequested(index: int): void {
            root.commentIndex = index;
            root.active = true;
        }
    }
}

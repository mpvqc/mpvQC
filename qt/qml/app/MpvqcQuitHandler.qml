// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick

import "../messageboxes"

Item {
    id: root

    required property var mpvqcApplication
    required property bool canClose

    readonly property var mpvqcMpvPlayerPyObject: mpvqcApplication.mpvqcMpvPlayerPyObject
    readonly property var mpvqcManager: mpvqcApplication.mpvqcManager

    property bool userConfirmedClose: false

    property var quitDialog: null
    property var quitDialogFactory: Component {
        MpvqcQuitMessageBox {
            parent: root.mpvqcApplication.contentItem

            onAccepted: {
                root._close();
            }
        }
    }

    function requestClose(): void {
        if (canClose || userConfirmedClose) {
            _close();
        } else {
            quitDialog = quitDialogFactory.createObject(root);
            quitDialog.closed.connect(quitDialog.destroy);
            quitDialog.open();
        }
    }

    function _close(): void {
        userConfirmedClose = true;
        _workaroundNativeWindowInterfering();
        mpvqcApplication.close();
    }

    function _workaroundNativeWindowInterfering(): void {
        if (Qt.platform.os === "windows" && mpvqcManager.saved) {
            mpvqcMpvPlayerPyObject.terminate();
        }
    }
}

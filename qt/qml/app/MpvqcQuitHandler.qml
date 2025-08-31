/*
mpvQC

Copyright (C) 2022 mpvQC developers

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/

pragma ComponentBehavior: Bound

import QtQuick

import "../dialogs"

Item {
    id: root

    required property var mpvqcApplication
    required property bool canClose

    readonly property var mpvqcMpvPlayerPyObject: mpvqcApplication.mpvqcMpvPlayerPyObject
    readonly property var mpvqcManager: mpvqcApplication.mpvqcManager

    property bool userConfirmedClose: false

    property var quitDialog: null
    property var quitDialogFactory: Component {
        MpvqcMessageBoxQuit {
            mpvqcApplication: root.mpvqcApplication

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

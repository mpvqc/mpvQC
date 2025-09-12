/*
 * Copyright (C) 2025 mpvQC developers
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */

pragma ComponentBehavior: Bound

import QtQuick

Loader {
    id: root

    required property var mpvqcApplication

    readonly property url messageBoxExtendedExport: Qt.resolvedUrl("../dialogs/MpvqcMessageBoxExtendedExport.qml")
    readonly property url messageBoxExtendedExportFailed: Qt.resolvedUrl("../dialogs/MpvqcMessageBoxExtendedExportError.qml")
    readonly property url messageBoxVersionCheck: Qt.resolvedUrl("../dialogs/MpvqcMessageBoxVersionCheck.qml")

    signal messageBoxClosed

    asynchronous: true
    active: false
    visible: active

    function openExtendedExportsMessageBox(): void {
        setSource(messageBoxExtendedExport, {
            mpvqcApplication: root.mpvqcApplication
        });
        active = true;
    }

    function openExtendedExportFailedMessageBox(message: string, lineNr: int): void {
        setSource(messageBoxExtendedExportFailed, {
            mpvqcApplication: root.mpvqcApplication,
            errorMessage: message,
            errorLine: lineNr
        });
        active = true;
    }

    function openVersionCheckMessageBox(): void {
        setSource(messageBoxVersionCheck, {
            mpvqcApplication: root.mpvqcApplication
        });
        active = true;
    }

    onLoaded: item.open() // qmllint disable

    Connections {
        enabled: root.item
        target: root.item

        function onClosed(): void {
            root.active = false;
            root.source = "";
            root.messageBoxClosed();
        }
    }
}

// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick

import io.github.mpvqc.mpvQC.Python

Loader {
    id: root
    objectName: "messageBoxLoader"

    readonly property MpvqcMessageBoxLoaderViewModel viewModel: MpvqcMessageBoxLoaderViewModel {}

    readonly property url messageBoxExtendedExport: Qt.resolvedUrl("MpvqcExtendedExportMessageBox.qml")
    readonly property url messageBoxExportError: Qt.resolvedUrl("MpvqcExportErrorMessageBox.qml")
    readonly property url messageBoxQuit: Qt.resolvedUrl("MpvqcQuitMessageBox.qml")
    readonly property url messageBoxReset: Qt.resolvedUrl("MpvqcResetMessageBox.qml")
    readonly property url messageBoxVersionCheck: Qt.resolvedUrl("MpvqcVersionCheckMessageBox.qml")

    signal messageBoxClosed

    asynchronous: true
    active: false
    visible: status === Loader.Ready

    function openExtendedExportsMessageBox(): void {
        setSource(messageBoxExtendedExport);
        active = true;
    }

    function openExportErrorMessageBox(message: string, lineNr: int): void {
        setSource(messageBoxExportError, {
            errorMessage: message,
            errorLine: lineNr
        });
        active = true;
    }

    function openQuitMessageBox(): void {
        setSource(messageBoxQuit);
        active = true;
    }

    function openResetMessageBox(): void {
        setSource(messageBoxReset);
        active = true;
    }

    function openVersionCheckMessageBox(): void {
        setSource(messageBoxVersionCheck);
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

    Connections {
        target: root.viewModel

        function onExportErrorOccurred(message: string, line: int): void {
            root.openExportErrorMessageBox(message, line);
        }

        function onConfirmQuit(): void {
            root.openQuitMessageBox();
        }
    }
}

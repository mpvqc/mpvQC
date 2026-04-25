// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick

import pyobjects

Loader {
    id: root
    objectName: "messageBoxLoader"

    readonly property MpvqcMessageBoxLoaderViewModel viewModel: MpvqcMessageBoxLoaderViewModel {}

    readonly property url messageBoxDocumentNotCompatible: Qt.resolvedUrl("MpvqcDocumentNotCompatibleMessageBox.qml")
    readonly property url messageBoxExtendedExport: Qt.resolvedUrl("MpvqcExtendedExportMessageBox.qml")
    readonly property url messageBoxExtendedExportFailed: Qt.resolvedUrl("MpvqcExtendedExportErrorMessageBox.qml")
    readonly property url messageBoxQuit: Qt.resolvedUrl("MpvqcQuitMessageBox.qml")
    readonly property url messageBoxReset: Qt.resolvedUrl("MpvqcResetMessageBox.qml")
    readonly property url messageBoxVersionCheck: Qt.resolvedUrl("MpvqcVersionCheckMessageBox.qml")

    signal messageBoxClosed

    asynchronous: true
    active: false
    visible: status === Loader.Ready

    function openDocumentNotCompatibleMessageBox(documents: list<var>): void {
        setSource(messageBoxDocumentNotCompatible, {
            files: documents
        });
        active = true;
    }

    function openExtendedExportsMessageBox(): void {
        setSource(messageBoxExtendedExport);
        active = true;
    }

    function openExtendedExportFailedMessageBox(message: string, lineNr: int): void {
        setSource(messageBoxExtendedExportFailed, {
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

        function onErroneousDocumentsImported(documents: list<var>): void {
            root.openDocumentNotCompatibleMessageBox(documents);
        }

        function onExportErrorOccurred(message: string, line: int): void {
            root.openExtendedExportFailedMessageBox(message, line);
        }

        function onConfirmQuit(): void {
            root.openQuitMessageBox();
        }
    }
}

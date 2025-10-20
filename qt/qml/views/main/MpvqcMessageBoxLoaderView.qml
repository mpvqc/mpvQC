// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick

import pyobjects

Loader {
    id: root

    readonly property MpvqcMessageBoxLoaderViewModel viewModel: MpvqcMessageBoxLoaderViewModel {}

    readonly property url messageBoxDocumentNotCompatible: Qt.resolvedUrl("../../messageboxes/MpvqcDocumentNotCompatibleMessageBox.qml")
    readonly property url messageBoxExtendedExport: Qt.resolvedUrl("../../messageboxes/MpvqcExtendedExportMessageBox.qml")
    readonly property url messageBoxExtendedExportFailed: Qt.resolvedUrl("../../messageboxes/MpvqcExtendedExportErrorMessageBox.qml")
    readonly property url messageBoxQuit: Qt.resolvedUrl("../../messageboxes/MpvqcQuitMessageBox.qml")
    readonly property url messageBoxReset: Qt.resolvedUrl("../../messageboxes/MpvqcResetMessageBox.qml")
    readonly property url messageBoxVersionCheck: Qt.resolvedUrl("../../messageboxes/MpvqcVersionCheckMessageBox.qml")
    readonly property url messageBoxVideoFound: Qt.resolvedUrl("../../messageboxes/MpvqcVideoFoundMessageBox.qml")

    signal messageBoxClosed

    asynchronous: true
    active: false
    visible: active

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

    function openVideoFoundMessageBox(trackingId: string, fileName: string): void {
        setSource(messageBoxVideoFound, {
            file: fileName,
            trackingId: trackingId
        });
        active = true;
    }

    onLoaded: item.open() // qmllint disable

    Connections {
        enabled: root.item
        target: root.item
        ignoreUnknownSignals: true

        function onClosed(): void {
            root.active = false;
            root.source = "";
            root.messageBoxClosed();
        }

        function onImportDecisionMade(trackingId: string, openVideo: bool): void {
            root.viewModel.continueWithImport(trackingId, openVideo);
        }
    }

    Connections {
        target: root.viewModel

        function onErroneousDocumentsImported(documents: list<var>): void {
            root.openDocumentNotCompatibleMessageBox(documents);
        }

        function onAskUserDocumentVideoImport(trackingId: string, fileName: string): void {
            root.openVideoFoundMessageBox(trackingId, fileName);
        }

        function onAskUserSubtitleVideoImport(trackingId: string, fileName: string): void {
            root.openVideoFoundMessageBox(trackingId, fileName);
        }

        function onExportErrorOccurred(message: string, line: int): void {
            root.openExtendedExportFailedMessageBox(message, line);
        }

        function onConfirmQuit(): void {
            root.openQuitMessageBox();
        }
    }
}

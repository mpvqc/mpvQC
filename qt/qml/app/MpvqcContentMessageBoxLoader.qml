// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick

Loader {
    id: root

    required property var mpvqcApplication

    readonly property url messageBoxDocumentNotCompatible: Qt.resolvedUrl("../dialogs/MpvqcMessageBoxDocumentNotCompatible.qml")
    readonly property url messageBoxExtendedExport: Qt.resolvedUrl("../dialogs/MpvqcMessageBoxExtendedExport.qml")
    readonly property url messageBoxExtendedExportFailed: Qt.resolvedUrl("../dialogs/MpvqcMessageBoxExtendedExportError.qml")
    readonly property url messageBoxNewDocument: Qt.resolvedUrl("../dialogs/MpvqcMessageBoxNewDocument.qml")
    readonly property url messageBoxVersionCheck: Qt.resolvedUrl("../dialogs/MpvqcMessageBoxVersionCheck.qml")
    readonly property url messageBoxVideoFound: Qt.resolvedUrl("../dialogs/MpvqcMessageBoxVideoFound.qml")

    signal messageBoxClosed

    asynchronous: true
    active: false
    visible: active

    function openDocumentNotCompatibleMessageBox(documents: list<string>): void {
        setSource(messageBoxDocumentNotCompatible, {
            mpvqcApplication: root.mpvqcApplication,
            paths: documents
        });
        active = true;
    }

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

    function openNewDocumentMessageBox(): void {
        setSource(messageBoxNewDocument, {
            mpvqcApplication: root.mpvqcApplication
        });
        active = true;
    }

    function openVersionCheckMessageBox(): void {
        setSource(messageBoxVersionCheck, {
            mpvqcApplication: root.mpvqcApplication
        });
        active = true;
    }

    function openVideoFoundMessageBox(): void {
        setSource(messageBoxVideoFound, {
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

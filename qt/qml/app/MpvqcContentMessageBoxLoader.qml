// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick

Loader {
    id: root

    required property var mpvqcExtendedDocumentExporterPyObject

    readonly property url messageBoxDocumentNotCompatible: Qt.resolvedUrl("../messageboxes/MpvqcDocumentNotCompatibleMessageBox.qml")
    readonly property url messageBoxExtendedExport: Qt.resolvedUrl("../messageboxes/MpvqcExtendedExportMessageBox.qml")
    readonly property url messageBoxExtendedExportFailed: Qt.resolvedUrl("../messageboxes/MpvqcExtendedExportErrorMessageBox.qml")
    readonly property url messageBoxNewDocument: Qt.resolvedUrl("../messageboxes/MpvqcNewDocumentMessageBox.qml")
    readonly property url messageBoxVersionCheck: Qt.resolvedUrl("../messageboxes/MpvqcVersionCheckMessageBox.qml")
    readonly property url messageBoxVideoFound: Qt.resolvedUrl("../messageboxes/MpvqcVideoFoundMessageBox.qml")

    signal messageBoxClosed

    asynchronous: true
    active: false
    visible: active

    function openDocumentNotCompatibleMessageBox(documents: list<string>): void {
        setSource(messageBoxDocumentNotCompatible, {
            parent: root.parent,
            paths: documents
        });
        active = true;
    }

    function openExtendedExportsMessageBox(): void {
        setSource(messageBoxExtendedExport, {
            parent: root.parent
        });
        active = true;
    }

    function openExtendedExportFailedMessageBox(message: string, lineNr: int): void {
        setSource(messageBoxExtendedExportFailed, {
            parent: root.parent,
            errorMessage: message,
            errorLine: lineNr
        });
        active = true;
    }

    function openNewDocumentMessageBox(): void {
        setSource(messageBoxNewDocument, {
            parent: root.parent
        });
        active = true;
    }

    function openVersionCheckMessageBox(): void {
        setSource(messageBoxVersionCheck, {
            parent: root.parent
        });
        active = true;
    }

    function openVideoFoundMessageBox(): void {
        setSource(messageBoxVideoFound, {
            parent: root.parent
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

    Connections {
        target: root.mpvqcExtendedDocumentExporterPyObject

        function onErrorOccurred(message: string, line: int): void {
            root.openExtendedExportFailedMessageBox(message, line);
        }
    }
}

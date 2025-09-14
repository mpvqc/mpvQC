// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick

Loader {
    id: root

    required property var mpvqcApplication

    readonly property url importQcDocumentsDialog: Qt.resolvedUrl("../dialogs/MpvqcDialogImportDocuments.qml")
    readonly property url importVideoDialog: Qt.resolvedUrl("../dialogs/MpvqcDialogImportVideo.qml")
    readonly property url importSubtitlesDialog: Qt.resolvedUrl("../dialogs/MpvqcDialogImportSubtitles.qml")
    readonly property url exportQcDocumentDialog: Qt.resolvedUrl("../dialogs/MpvqcDialogExportDocument.qml")

    property alias cleanupDelay: _delayCleanupTimer.interval

    signal dialogClosed
    signal documentSaved(document: url)
    signal extendedDocumentSaved(document: url, template: url)

    asynchronous: true
    active: false
    visible: active

    function openImportQcDocumentsDialog(): void {
        setSource(importQcDocumentsDialog, {
            mpvqcApplication: root.mpvqcApplication
        });
        active = true;
    }

    function openDocumentExportDialog(proposal: url): void {
        setSource(exportQcDocumentDialog, {
            isExtendedExport: false,
            selectedFile: proposal
        });
        active = true;
    }

    function openExtendedDocumentExportDialog(proposal: url, exportTemplate: url): void {
        setSource(exportQcDocumentDialog, {
            isExtendedExport: true,
            selectedFile: proposal,
            exportTemplate: exportTemplate
        });
        active = true;
    }

    function openImportVideoDialog(): void {
        setSource(importVideoDialog, {
            mpvqcApplication: root.mpvqcApplication
        });
        active = true;
    }

    function openImportSubtitlesDialog(): void {
        setSource(importSubtitlesDialog, {
            mpvqcApplication: root.mpvqcApplication
        });
        active = true;
    }

    onLoaded: item.open() // qmllint disable

    Connections {
        enabled: root.item
        target: root.item
        ignoreUnknownSignals: true

        function onSavedPressed(document: url): void {
            root.documentSaved(document);
        }

        function onExtendedSavePressed(document: url, template: url): void {
            root.extendedDocumentSaved(document, template);
        }

        function onAccepted(): void {
            _delayCleanupTimer.restart();
        }

        function onRejected(): void {
            _delayCleanupTimer.restart();
        }
    }

    Timer {
        id: _delayCleanupTimer

        onTriggered: {
            root.active = false;
            root.source = "";
            root.dialogClosed();
        }
    }
}

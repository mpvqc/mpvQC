// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick

Loader {
    id: root

    required property var mpvqcApplication

    readonly property url exportDocumentDialog: Qt.resolvedUrl("../filedialogs/MpvqcExportDocumentFileDialog.qml")
    readonly property url importDocumentsDialog: Qt.resolvedUrl("../filedialogs/MpvqcImportDocumentsFileDialog.qml")
    readonly property url importSubtitlesDialog: Qt.resolvedUrl("../filedialogs/MpvqcImportSubtitlesFileDialog.qml")
    readonly property url importVideoDialog: Qt.resolvedUrl("../filedialogs/MpvqcImportVideoFileDialog.qml")

    property alias cleanupDelay: _delayCleanupTimer.interval

    signal dialogClosed
    signal documentSaved(document: url)
    signal extendedDocumentSaved(document: url, template: url)

    asynchronous: true
    active: false
    visible: active

    function openDocumentExportDialog(proposal: url): void {
        setSource(exportDocumentDialog, {
            isExtendedExport: false,
            selectedFile: proposal
        });
        active = true;
    }

    function openExtendedDocumentExportDialog(proposal: url, exportTemplate: url): void {
        setSource(exportDocumentDialog, {
            isExtendedExport: true,
            selectedFile: proposal,
            exportTemplate: exportTemplate
        });
        active = true;
    }

    function openImportQcDocumentsDialog(): void {
        setSource(importDocumentsDialog, {
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

    function openImportVideoDialog(): void {
        setSource(importVideoDialog, {
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

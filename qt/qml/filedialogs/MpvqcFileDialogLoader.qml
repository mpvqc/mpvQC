// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick

Loader {
    id: root

    readonly property url exportDocumentDialog: Qt.resolvedUrl("MpvqcExportDocumentFileDialog.qml")
    readonly property url importDocumentsDialog: Qt.resolvedUrl("MpvqcImportDocumentsFileDialog.qml")
    readonly property url importSubtitlesDialog: Qt.resolvedUrl("MpvqcImportSubtitlesFileDialog.qml")
    readonly property url importVideoDialog: Qt.resolvedUrl("MpvqcImportVideoFileDialog.qml")
    readonly property url saveDocumentDialog: Qt.resolvedUrl("MpvqcSaveDocumentFileDialog.qml")

    readonly property int cleanupDelay: 250

    signal dialogClosed

    asynchronous: true
    active: false
    visible: active

    function openDocumentSaveDialog(): void {
        setSource(saveDocumentDialog);
        active = true;
    }

    function openExtendedDocumentExportDialog(exportTemplate: url): void {
        setSource(exportDocumentDialog, {
            exportTemplate: exportTemplate
        });
        active = true;
    }

    function openImportQcDocumentsDialog(): void {
        setSource(importDocumentsDialog);
        active = true;
    }

    function openImportSubtitlesDialog(): void {
        setSource(importSubtitlesDialog);
        active = true;
    }

    function openImportVideoDialog(): void {
        setSource(importVideoDialog);
        active = true;
    }

    onLoaded: item.open() // qmllint disable

    Connections {
        enabled: root.item
        target: root.item
        ignoreUnknownSignals: true

        function onAccepted(): void {
            _delayCleanupTimer.restart();
        }

        function onRejected(): void {
            _delayCleanupTimer.restart();
        }
    }

    Timer {
        id: _delayCleanupTimer

        interval: root.cleanupDelay

        onTriggered: {
            root.active = false;
            root.source = "";
            root.dialogClosed();
        }
    }
}

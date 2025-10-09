// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick

Loader {
    id: root

    readonly property url exportDocumentDialog: Qt.resolvedUrl("../../filedialogs/MpvqcExportDocumentFileDialog.qml")
    readonly property url importDocumentsDialog: Qt.resolvedUrl("../../filedialogs/MpvqcImportDocumentsFileDialog.qml")
    readonly property url importSubtitlesDialog: Qt.resolvedUrl("../../filedialogs/MpvqcImportSubtitlesFileDialog.qml")
    readonly property url importVideoDialog: Qt.resolvedUrl("../../filedialogs/MpvqcImportVideoFileDialog.qml")

    readonly property int cleanupDelay: 250

    signal dialogClosed

    asynchronous: true
    active: false
    visible: active

    function openDocumentExportDialog(proposal: url): void {
        setSource(exportDocumentDialog, {
            isExtendedExport: false
        });
        active = true;
    }

    function openExtendedDocumentExportDialog(exportTemplate: url): void {
        setSource(exportDocumentDialog, {
            isExtendedExport: true,
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

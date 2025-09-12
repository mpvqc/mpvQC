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

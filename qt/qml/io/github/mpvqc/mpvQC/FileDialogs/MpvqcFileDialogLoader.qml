// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

import QtQuick
import QtQuick.Dialogs

import io.github.mpvqc.mpvQC.Components
import io.github.mpvqc.mpvQC.Python

MpvqcOverlayLoader {
    id: root
    objectName: "fileDialogLoader"

    readonly property var _urlsByKind: ({
            [MpvqcFileDialogKind.FileDialogKind.EXPORT_CLASSIC_DOCUMENT]: Qt.resolvedUrl("MpvqcExportClassicDocumentFileDialog.qml"),
            [MpvqcFileDialogKind.FileDialogKind.EXPORT_CUSTOM_DOCUMENT]: Qt.resolvedUrl("MpvqcExportCustomDocumentFileDialog.qml"),
            [MpvqcFileDialogKind.FileDialogKind.IMPORT_DOCUMENTS]: Qt.resolvedUrl("MpvqcImportDocumentsFileDialog.qml"),
            [MpvqcFileDialogKind.FileDialogKind.IMPORT_SUBTITLES]: Qt.resolvedUrl("MpvqcImportSubtitlesFileDialog.qml"),
            [MpvqcFileDialogKind.FileDialogKind.IMPORT_VIDEO]: Qt.resolvedUrl("MpvqcImportVideoFileDialog.qml"),
            [MpvqcFileDialogKind.FileDialogKind.SAVE_DOCUMENT]: Qt.resolvedUrl("MpvqcSaveDocumentFileDialog.qml")
        })

    function openFileDialog(kind: int): void {
        root.open(root._urlsByKind[kind]);
    }

    function openCustomExportFileDialog(exportTemplate: url): void {
        root.open(root._urlsByKind[MpvqcFileDialogKind.FileDialogKind.EXPORT_CUSTOM_DOCUMENT], {
            exportTemplate: exportTemplate
        });
    }

    teardownTrigger: MpvqcOverlayLoader.TeardownTrigger.AcceptedOrRejected

    // Native file dialogs must outlive the accept/reject signal they emit, so
    // teardown is deferred. The magnitude is historical, not measured.
    teardownDelay: 250

    MpvqcModalOverlayTracker {
        open: (root.item as FileDialog)?.visible ?? false
    }
}

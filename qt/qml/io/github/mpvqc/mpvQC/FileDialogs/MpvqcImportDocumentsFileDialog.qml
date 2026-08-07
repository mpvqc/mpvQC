// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

import QtQuick.Dialogs

import io.github.mpvqc.mpvQC.Python

FileDialog {
    objectName: "importDocumentsFileDialog"

    readonly property MpvqcImportFileDialogViewModel viewModel: MpvqcImportFileDialogViewModel {}

    title: qsTranslate("FileInteractionDialogs", "Open QC Document(s)")
    currentFolder: viewModel.lastDirectoryDocuments
    fileMode: FileDialog.OpenFiles
    nameFilters: [qsTranslate("FileInteractionDialogs", "QC documents") + viewModel.documentFileGlobPattern, qsTranslate("FileInteractionDialogs", "All files") + " (*)"]

    onAccepted: viewModel.openDocuments(selectedFiles)
}

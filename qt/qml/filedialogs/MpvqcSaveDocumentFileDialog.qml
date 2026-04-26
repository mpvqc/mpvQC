// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

import QtQuick.Dialogs

import pyobjects

FileDialog {
    objectName: "saveDocumentFileDialog"

    readonly property MpvqcExportFileDialogViewModel viewModel: MpvqcExportFileDialogViewModel {}

    title: qsTranslate("FileInteractionDialogs", "Save QC Document As")
    fileMode: FileDialog.SaveFile
    selectedFile: viewModel.filenameProposal
    defaultSuffix: "txt"
    nameFilters: [qsTranslate("FileInteractionDialogs", "QC documents") + " (*.txt)", qsTranslate("FileInteractionDialogs", "All files") + " (*)"]

    onAccepted: viewModel.save(selectedFile)
}

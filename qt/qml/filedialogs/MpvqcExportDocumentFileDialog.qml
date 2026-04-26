// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

import QtQuick.Dialogs

import pyobjects

FileDialog {
    objectName: "exportDocumentFileDialog"

    readonly property MpvqcExportFileDialogViewModel viewModel: MpvqcExportFileDialogViewModel {}

    required property url exportTemplate

    title: qsTranslate("FileInteractionDialogs", "Save QC Document As")
    fileMode: FileDialog.SaveFile
    selectedFile: viewModel.filenameProposal
    defaultSuffix: "txt"
    nameFilters: [qsTranslate("FileInteractionDialogs", "QC documents") + " (*.txt)", qsTranslate("FileInteractionDialogs", "All files") + " (*)"]

    onAccepted: viewModel.export(selectedFile, exportTemplate)
}

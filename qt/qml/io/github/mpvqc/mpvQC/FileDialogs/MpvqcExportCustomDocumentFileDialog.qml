// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

import QtQuick.Dialogs

import io.github.mpvqc.mpvQC.Python

FileDialog {
    objectName: "exportCustomDocumentFileDialog"

    required property url exportTemplate

    readonly property MpvqcExportFileDialogViewModel viewModel: MpvqcExportFileDialogViewModel {}

    title: qsTranslate("FileInteractionDialogs", "Save QC Document As")
    fileMode: FileDialog.SaveFile
    selectedFile: viewModel.customFilenameProposal
    defaultSuffix: "txt"
    nameFilters: [qsTranslate("FileInteractionDialogs", "QC documents") + " (*.txt)", qsTranslate("FileInteractionDialogs", "All files") + " (*)"]

    onAccepted: viewModel.exportCustom(selectedFile, exportTemplate)
}

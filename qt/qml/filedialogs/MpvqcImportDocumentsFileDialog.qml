// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

import QtQuick.Dialogs

import pyobjects

FileDialog {
    readonly property MpvqcFileDialogViewModel viewModel: MpvqcFileDialogViewModel {}

    title: qsTranslate("FileInteractionDialogs", "Open QC Document(s)")
    currentFolder: viewModel.lastDirectoryDocuments
    fileMode: FileDialog.OpenFiles
    nameFilters: [qsTranslate("FileInteractionDialogs", "QC documents") + " (*.txt)", qsTranslate("FileInteractionDialogs", "All files") + " (*)"]

    onAccepted: {
        viewModel.lastDirectoryDocuments = currentFolder;
        viewModel.openDocuments(selectedFiles);
    }
}

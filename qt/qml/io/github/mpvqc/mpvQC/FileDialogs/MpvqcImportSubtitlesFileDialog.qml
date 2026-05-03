// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

import QtQuick.Dialogs

import io.github.mpvqc.mpvQC.Python

FileDialog {
    objectName: "importSubtitlesFileDialog"

    readonly property MpvqcImportFileDialogViewModel viewModel: MpvqcImportFileDialogViewModel {}

    title: qsTranslate("FileInteractionDialogs", "Open Subtitle(s)")
    currentFolder: viewModel.lastDirectorySubtitles
    fileMode: FileDialog.OpenFiles
    nameFilters: [qsTranslate("FileInteractionDialogs", "Subtitle files") + viewModel.subtitleFileGlobPattern, qsTranslate("FileInteractionDialogs", "All files") + " (*)"]

    onAccepted: {
        viewModel.lastDirectorySubtitles = currentFolder;
        viewModel.openSubtitles(selectedFiles);
    }
}

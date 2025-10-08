// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

import QtQuick.Dialogs

import pyobjects

FileDialog {
    readonly property MpvqcImportFileDialogViewModel viewModel: MpvqcImportFileDialogViewModel {}

    title: qsTranslate("FileInteractionDialogs", "Open Video")
    currentFolder: viewModel.lastDirectoryVideo
    nameFilters: [qsTranslate("FileInteractionDialogs", "Video files") + viewModel.videoFileGlobPattern, qsTranslate("FileInteractionDialogs", "All files") + " (*)"]

    onAccepted: {
        viewModel.lastDirectoryVideo = currentFolder;
        viewModel.openVideo(currentFile);
    }
}

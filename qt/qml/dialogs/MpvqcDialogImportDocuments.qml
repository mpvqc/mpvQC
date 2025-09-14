// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

import QtQuick.Dialogs

FileDialog {
    required property var mpvqcApplication

    readonly property var mpvqcManager: mpvqcApplication.mpvqcManager
    readonly property var mpvqcSettings: mpvqcApplication.mpvqcSettings

    title: qsTranslate("FileInteractionDialogs", "Open QC Document(s)")
    currentFolder: mpvqcSettings.lastDirectoryDocuments
    fileMode: FileDialog.OpenFiles
    nameFilters: [
        qsTranslate("FileInteractionDialogs", "QC documents") + " (*.txt)",
        qsTranslate("FileInteractionDialogs", "All files") + " (*)",
    ]

    onAccepted: {
        mpvqcSettings.lastDirectoryDocuments = currentFolder;
        mpvqcManager.openDocuments(selectedFiles);
    }
}

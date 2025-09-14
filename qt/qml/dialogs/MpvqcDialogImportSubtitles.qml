// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

import QtQuick.Dialogs

FileDialog {
    required property var mpvqcApplication

    readonly property var mpvqcManager: mpvqcApplication.mpvqcManager
    readonly property var mpvqcSettings: mpvqcApplication.mpvqcSettings
    readonly property var mpvqcUtilityPyObject: mpvqcApplication.mpvqcUtilityPyObject

    title: qsTranslate("FileInteractionDialogs", "Open Subtitle(s)")
    currentFolder: mpvqcSettings.lastDirectorySubtitles
    fileMode: FileDialog.OpenFiles
    nameFilters: [
        qsTranslate("FileInteractionDialogs", "Subtitle files") + mpvqcUtilityPyObject.subtitleFileGlobPattern,
        qsTranslate("FileInteractionDialogs", "All files") + " (*)",
    ]

    onAccepted: {
        mpvqcSettings.lastDirectorySubtitles = currentFolder;
        mpvqcManager.openSubtitles(selectedFiles);
    }
}

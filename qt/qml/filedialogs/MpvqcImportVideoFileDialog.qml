// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

import QtQuick.Dialogs

FileDialog {
    required property var mpvqcApplication

    readonly property var mpvqcManager: mpvqcApplication.mpvqcManager
    readonly property var mpvqcSettings: mpvqcApplication.mpvqcSettings
    readonly property var mpvqcUtilityPyObject: mpvqcApplication.mpvqcUtilityPyObject

    title: qsTranslate("FileInteractionDialogs", "Open Video")
    currentFolder: mpvqcSettings.lastDirectoryVideo
    nameFilters: [qsTranslate("FileInteractionDialogs", "Video files") + mpvqcUtilityPyObject.videoFileGlobPattern, qsTranslate("FileInteractionDialogs", "All files") + " (*)"]

    onAccepted: {
        mpvqcSettings.lastDirectoryVideo = currentFolder;
        mpvqcManager.openVideo(currentFile);
    }
}

// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

import QtQuick.Dialogs

FileDialog {
    required property bool isExtendedExport
    property url exportTemplate

    title: qsTranslate("FileInteractionDialogs", "Save QC Document As")
    fileMode: FileDialog.SaveFile
    defaultSuffix: "txt"
    nameFilters: [
        qsTranslate("FileInteractionDialogs", "QC documents") + " (*.txt)",
        qsTranslate("FileInteractionDialogs", "All files") + " (*)",
    ]

    signal savePressed(fileUrl: url)
    signal extendedSavePressed(fileUrl: url, template: url)

    onAccepted: {
        if (isExtendedExport) {
            extendedSavePressed(currentFile, exportTemplate);
        } else {
            savePressed(currentFile);
        }
    }
}

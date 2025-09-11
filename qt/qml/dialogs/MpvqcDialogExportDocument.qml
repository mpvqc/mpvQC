/*
mpvQC

Copyright (C) 2022 mpvQC developers

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/

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

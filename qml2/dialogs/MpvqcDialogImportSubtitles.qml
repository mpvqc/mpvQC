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
    id: root

    required property var mpvqcApplication
    property var mpvqcManager: mpvqcApplication.mpvqcManager
    property var mpvqcSettings: mpvqcApplication.mpvqcSettings
    property var supportedSubtitleFileExtensions: mpvqcApplication.supportedSubtitleFileExtensions
//
    title: qsTranslate("FileInteractionDialogs", "Open Subtitle(s)")
    currentFolder: mpvqcSettings.lastDirectorySubtitles
    fileMode: FileDialog.OpenFiles
    nameFilters: [
        qsTranslate("FileInteractionDialogs", "Subtitle files") + _subtitleFormatString(),
        qsTranslate("FileInteractionDialogs", "All files") + " (*.*)",
    ]

    function _subtitleFormatString() {
        const formats = supportedSubtitleFileExtensions.map(ending => `*.${ending}`).join(' ')
        return ` (${formats})`
    }

    onAccepted: {
        mpvqcSettings.lastDirectorySubtitles = currentFolder
        mpvqcManager.openSubtitles(selectedFiles)
    }

}

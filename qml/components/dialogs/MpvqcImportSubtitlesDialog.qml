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
import settings


FileDialog {
    title: qsTranslate("FileInteractionDialogs", "Open Subtitle(s)")
    currentFolder: MpvqcSettings.lastDirectorySubtitles
    fileMode: FileDialog.OpenFiles
    nameFilters: [
        qsTranslate("FileInteractionDialogs", "Subtitle files") + " (*.ass *.ssa *.srt *.sup *.idx *.utf *.utf8 *.utf-8 *.smi *.rt *.aqt *.jss *.js *.mks *.vtt *.sub *.scc)",
        qsTranslate("FileInteractionDialogs", "All files") + " (*.*)",
    ]

    onAccepted: {
        MpvqcSettings.lastDirectorySubtitles = currentFolder
        qcManager.openSubtitles(selectedFiles)
    }

}

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

import QtQuick.Controls

import dialogs
import shared


MpvqcMenu {
    id: root

    required property var mpvqcApplication

    property alias openVideoAction: _openVideoAction
    property alias openSubtitlesAction: _openSubtitlesAction

    title: qsTranslate("MainWindow", "&Video")

    Action {
        id: _openVideoAction

        property var dialog: MpvqcDialogImportVideo {
            mpvqcApplication: root.mpvqcApplication
        }

        text: qsTranslate("MainWindow", "Open &Video...")
        shortcut: "CTRL+Shift+O"

        onTriggered: {
            dialog.open()
        }
    }

    Action {
        id: _openSubtitlesAction

        property var dialog: MpvqcDialogImportSubtitles {
            mpvqcApplication: root.mpvqcApplication
        }

        text: qsTranslate("MainWindow", "&Open Subtitles...")

        onTriggered: {
            dialog.open()
        }
    }

//    MenuSeparator { }
//
//    Action {
//        text: qsTranslate("MainWindow", "&Resize Video to Original Resolution")
//        shortcut: "CTRL+R"
//
//        onTriggered: {
//            console.log("Resize Video to Original Resolution")
//        }
//    }

}

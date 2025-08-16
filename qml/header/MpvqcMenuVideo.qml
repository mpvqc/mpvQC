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

import QtQuick.Controls.Material

import "../dialogs"
import "../shared"

MpvqcMenu {
    id: root

    required property var mpvqcApplication

    readonly property alias openVideoAction: _openVideoAction
    readonly property alias openSubtitlesAction: _openSubtitlesAction
    readonly property alias resizeToOriginalResolutionAction: _resizeToOriginalResolutionAction

    readonly property var dialogImportVideo: MpvqcDialogImportVideo {
        mpvqcApplication: root.mpvqcApplication
    }

    readonly property var dialogImportSubtitles: MpvqcDialogImportSubtitles {
        mpvqcApplication: root.mpvqcApplication
    }

    signal resizeVideoTriggered

    title: qsTranslate("MainWindow", "Video")

    Action {
        id: _openVideoAction

        text: qsTranslate("MainWindow", "Open Video...")
        shortcut: "CTRL+Alt+O"
        icon.source: "qrc:/data/icons/movie_black_24dp.svg"

        onTriggered: {
            root.dialogImportVideo.open();
        }
    }

    Action {
        id: _openSubtitlesAction

        text: qsTranslate("MainWindow", "Open Subtitle(s)...")
        icon.source: "qrc:/data/icons/subtitles_black_24dp.svg"

        onTriggered: {
            root.dialogImportSubtitles.open();
        }
    }

    MenuSeparator {}

    Action {
        id: _resizeToOriginalResolutionAction

        text: qsTranslate("MainWindow", "Resize Video to Original Resolution")
        shortcut: "CTRL+R"
        icon.source: "qrc:/data/icons/aspect_ratio_black_24dp.svg"

        onTriggered: root.resizeVideoTriggered()
    }
}

/*
mpvQC

Copyright (C) 2022 mpvQC developers

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/


import QtQuick.Controls


MenuAutoWidth {

    title: qsTranslate("MainWindow", "&Video")

    Action {
        text: qsTranslate("MainWindow", "Open &Video...")
        shortcut: "CTRL+Shift+O"
        onTriggered: {
            const component = Qt.createComponent("qrc:/qml/components/DialogOpenVideo.qml")
            const dialog = component.createObject(appWindow)
            dialog.open()
        }
    }

    Action {
        text: qsTranslate("MainWindow", "&Open Subtitles...")
        onTriggered: {
            const component = Qt.createComponent("qrc:/qml/components/DialogOpenSubtitles.qml")
            const dialog = component.createObject(appWindow)
            dialog.open()
        }
    }

    Action {
        text: qsTranslate("MainWindow", "Open &Network Stream...")
        shortcut: "CTRL+Alt+Shift+O"
        onTriggered: {
            console.log("Open Network Stream...")
        }
    }

    MenuSeparator { }

    Action {
        text: qsTranslate("MainWindow", "&Resize Video to Original Resolution")
        shortcut: "CTRL+R"
        onTriggered: {
            console.log("Resize Video to Original Resolution")
        }
    }

}

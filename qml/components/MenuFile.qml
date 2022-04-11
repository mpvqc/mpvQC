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

    title: qsTranslate("MainWindow", "&File")

    Action {
        text: qsTranslate("MainWindow", "&New QC Document")
        shortcut: "CTRL+N"
        onTriggered: {
            console.log("New QC Document")
        }
    }

    Action {
        text: qsTranslate("MainWindow", "&Open QC Document(s)...")
        shortcut: "CTRL+O"
        onTriggered: {
            const component = Qt.createComponent("qrc:/qml/components/DialogOpenDocuments.qml")
            const dialog = component.createObject(appWindow)
            dialog.open()
        }
    }

    Action {
        text: qsTranslate("MainWindow", "&Save QC Document")
        shortcut: "CTRL+S"
        onTriggered: {
            console.log("Save QC Document")
        }
    }

    Action {
        text: qsTranslate("MainWindow", "&Save QC Document As...")
        shortcut: "CTRL+Shift+S"
        onTriggered: {
            console.log("Save QC Document As...")
        }
    }

    MenuSeparator { }

    Action {
        text: qsTranslate("MainWindow", "&Exit mpvQC")
        shortcut: "CTRL+Q"
        onTriggered: {
            console.log("Exit mpvQC")
        }
    }

}

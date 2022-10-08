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
import components.shared


MpvqcAutoWidthMenu {
    title: qsTranslate("MainWindow", "&File")

    Action {
        text: qsTranslate("MainWindow", "&New QC Document")
        shortcut: "CTRL+N"

        onTriggered: {
            qcManager.requestReset()
        }
    }

    Action {
        text: qsTranslate("MainWindow", "&Open QC Document(s)...")
        shortcut: "CTRL+O"

        onTriggered: {
            const url = "qrc:/qml/components/dialogs/MpvqcImportDocumentsDialog.qml"
            const component = Qt.createComponent(url)
            const dialog = component.createObject(appWindow)
            dialog.open()
        }
    }

    Action {
        text: qsTranslate("MainWindow", "&Save QC Document")
        shortcut: "CTRL+S"

        onTriggered: {
            qcManager.requestSave()
        }
    }

    Action {
        text: qsTranslate("MainWindow", "&Save QC Document As...")
        shortcut: "CTRL+Shift+S"

        onTriggered: {
            qcManager.requestSaveAs()
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

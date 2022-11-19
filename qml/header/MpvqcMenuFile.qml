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
    property var mpvqcManager: mpvqcApplication.mpvqcManager

    property alias resetAction: _resetAction
    property alias openDocumentsAction: _openDocumentsAction
    property alias saveAction: _saveAction
    property alias saveAsAction: _saveAsAction
    property alias quitAction: _quitAction

    title: qsTranslate("MainWindow", "&File")

    Action {
        id: _resetAction

        text: qsTranslate("MainWindow", "&New QC Document")
        shortcut: "CTRL+N"

        onTriggered: {
            root.mpvqcManager.reset()
        }
    }

    Action {
        id: _openDocumentsAction

        property var dialog: MpvqcDialogImportDocuments {
            mpvqcApplication: root.mpvqcApplication
        }

        text: qsTranslate("MainWindow", "&Open QC Document(s)...")
        shortcut: "CTRL+O"

        onTriggered: {
            dialog.open()
        }
    }

    Action {
        id: _saveAction

        text: qsTranslate("MainWindow", "&Save QC Document")
        shortcut: "CTRL+S"

        onTriggered: {
            root.mpvqcManager.save()
        }
    }

    Action {
        id: _saveAsAction

        text: qsTranslate("MainWindow", "&Save QC Document As...")
        shortcut: "CTRL+Shift+S"

        onTriggered: {
            root.mpvqcManager.saveAs()
        }
    }

    MenuSeparator { }

    Action {
        id: _quitAction

        text: qsTranslate("MainWindow", "&Exit mpvQC")
        shortcut: "CTRL+Q"

        onTriggered: {
            root.mpvqcApplication.close()
        }
    }

}

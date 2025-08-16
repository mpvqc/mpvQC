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

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls.Material

import "../dialogs"
import "../shared"

MpvqcMenu {
    id: root

    required property var mpvqcApplication
    required property var extendedExportTemplateModel

    readonly property var mpvqcManager: mpvqcApplication.mpvqcManager

    readonly property alias resetAction: _resetAction
    readonly property alias openDocumentsAction: _openDocumentsAction
    readonly property alias saveAction: _saveAction
    readonly property alias saveAsAction: _saveAsAction
    readonly property alias closeAction: _closeAction

    readonly property var dialogImportDocuments: MpvqcDialogImportDocuments {
        mpvqcApplication: root.mpvqcApplication
    }

    title: qsTranslate("MainWindow", "File")

    Action {
        id: _resetAction

        text: qsTranslate("MainWindow", "New QC Document")
        shortcut: "CTRL+N"
        icon.source: "qrc:/data/icons/inventory_black_24dp.svg"

        onTriggered: {
            root.mpvqcManager.reset();
        }
    }

    Action {
        id: _openDocumentsAction

        text: qsTranslate("MainWindow", "Open QC Document(s)...")
        shortcut: "CTRL+O"
        icon.source: "qrc:/data/icons/file_open_black_24dp.svg"

        onTriggered: {
            root.dialogImportDocuments.open();
        }
    }

    Action {
        id: _saveAction

        text: qsTranslate("MainWindow", "Save QC Document")
        shortcut: "CTRL+S"
        icon.source: "qrc:/data/icons/save_black_24dp.svg"

        onTriggered: {
            root.mpvqcManager.save();
        }
    }

    Action {
        id: _saveAsAction

        text: qsTranslate("MainWindow", "Save QC Document As...")
        shortcut: "CTRL+Shift+S"
        icon.source: "qrc:/data/icons/save_as_black_24dp.svg"

        onTriggered: {
            root.mpvqcManager.saveAs();
        }
    }

    MenuSeparator {
        height: _subMenuExtendedExport.haveTemplates ? implicitHeight : 0
    }

    MpvqcSubMenuExtendedExport {
        id: _subMenuExtendedExport

        mpvqcApplication: root.mpvqcApplication
        templateModel: root.extendedExportTemplateModel
        enabled: haveTemplates

        onEnabledChanged: {
            parent.enabled = enabled; // qmllint disable unqualified
            parent.visible = enabled;
            parent.height = enabled ? parent.implicitHeight : 0;
        }
    }

    MenuSeparator {}

    Action {
        id: _closeAction

        text: qsTranslate("MainWindow", "Exit mpvQC")
        shortcut: "CTRL+Q"
        icon.source: "qrc:/data/icons/exit_to_app_black_24dp.svg"

        onTriggered: {
            root.mpvqcApplication.close();
        }
    }
}

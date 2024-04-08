/*
mpvQC

Copyright (C) 2024 mpvQC developers

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

import QtQuick
import QtQuick.Controls

import dialogs
import shared


MpvqcMenu {
    id: root

    required property var mpvqcApplication

    property alias templateModel: _repeater.model

    readonly property var mpvqcExtendedDocumentExporterPyObject: mpvqcApplication.mpvqcExtendedDocumentExporterPyObject
    readonly property bool haveTemplates: _repeater.count > 0

    readonly property MpvqcDialogExportDocument exportDialog: MpvqcDialogExportDocument
    {
        property url template

        onSavePressed: (documentUrl) => {
            root.mpvqcExtendedDocumentExporterPyObject.export(template, documentUrl)
        }
    }

    property var exportErrorDialog
    property var exportErrorDialogFactory: Component
    {
        MpvqcMessageBox {
            mpvqcApplication: root.mpvqcApplication

            title: qsTranslate("MessageBoxes", "Export Error")
            standardButtons: Dialog.Ok
        }
    }

    title: qsTranslate("MainWindow", "Export QC Document")
    icon.source: "qrc:/data/icons/save_alt_black_24dp.svg"
    icon.height: 24
    icon.width: 24

    function openExportFileSelectionDialog(name: string, path: url): void {
        root.exportDialog.selectedFile = root.mpvqcExtendedDocumentExporterPyObject.generate_file_path_proposal()
        root.exportDialog.template = path
        root.exportDialog.title = qsTranslate("FileInteractionDialogs", "Export QC Document Using %1 Template").arg(name)
        root.exportDialog.open()
    }

    function displayExportErrorDialog(message: string, lineNr: int): void {
        root.exportErrorDialog = root.exportErrorDialogFactory.createObject(root)
        root.exportErrorDialog.text = lineNr
            ? qsTranslate("MessageBoxes", "Error at line %1: %2").arg(lineNr).arg(message)
            : message
        root.exportErrorDialog.closed.connect(root.exportErrorDialog.destroy)
        root.exportErrorDialog.open()
    }

    Repeater {
        id: _repeater

        delegate: MenuItem {
            required property string name
            required property url path

            text: name
            icon.source: "qrc:/data/icons/notes_black_24dp.svg"
            icon.height: 24
            icon.width: 24

            onTriggered: {
                root.openExportFileSelectionDialog(name, path)
            }
        }
    }

    Connections {
        target: root.mpvqcExtendedDocumentExporterPyObject

        function onExportErrorOccurred(message: string, lineNr: int): void {
            root.displayExportErrorDialog(message, lineNr)
        }
    }

}

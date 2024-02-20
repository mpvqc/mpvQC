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

    readonly property var mpvqcDocumentExporterPyObject: mpvqcApplication.mpvqcDocumentExporterPyObject
    readonly property bool haveTemplates: _repeater.count > 0

    readonly property MpvqcDialogExportDocument exportDialog: MpvqcDialogExportDocument
    {
        property string template

        onSavePressed: (documentUrl) => {
            root.mpvqcDocumentExporterPyObject.write_with(template, documentUrl)
            console.log("todo handle write errors and display messagebox")
        }
    }

    title: qsTranslate("MainWindow", "&Export QC Documents")
    icon.source: "qrc:/data/icons/save_alt_black_24dp.svg"
    icon.height: 24
    icon.width: 24

    Repeater {
        id: _repeater

        delegate: MenuItem {
            required property string name
            required property string path

            text: name
            icon.source: "qrc:/data/icons/notes_black_24dp.svg"
            icon.height: 24
            icon.width: 24

            onTriggered: {
                exportDialog.selectedFile = root.mpvqcDocumentExporterPyObject.generate_file_path_proposal()
                exportDialog.template = path
                exportDialog.open()
            }
        }
    }

}

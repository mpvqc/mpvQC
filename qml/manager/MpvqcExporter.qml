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

import QtCore
import QtQuick

import dialogs


QtObject {
    id: root

    required property url video
    required property url document
    required property var mpvqcApplication

    // readonly property var mpvqcExtendedDocumentExporterPyObject: mpvqcApplication.mpvqcExtendedDocumentExporterPyObject

    property MpvqcDialogExportDocument exportDialog: MpvqcDialogExportDocument
    {
        onSavePressed: (documentUrl) => {
            root.save(documentUrl)
        }
    }

    signal saved(url newDocument)

    function requestSave(): void {
        if (_documentKnown()) {
            save(document)
        } else {
            requestSaveAs()
        }
    }

    function _documentKnown(): bool {
        return document && document.toString() !== ''
    }

    function save(newDocumentUrl: url): void {
        // mpvqcExtendedDocumentExporterPyObject.save(newDocumentUrl)
        saved(newDocumentUrl)
    }

    function requestSaveAs(): void {
        // exportDialog.selectedFile = mpvqcExtendedDocumentExporterPyObject.generate_file_path_proposal()
        exportDialog.open()
    }

}

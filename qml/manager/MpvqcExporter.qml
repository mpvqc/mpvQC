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

import "MpvqcDocumentFileExporter.js" as MpvqcDocumentFileExporter


QtObject {
    id: root

    required property url video
    required property url document
    required property var mpvqcApplication

    readonly property var mpvqcSettings: mpvqcApplication.mpvqcSettings
    readonly property var mpvqcDocumentExporterPyObject: mpvqcApplication.mpvqcDocumentExporterPyObject
    readonly property var mpvqcFileSystemHelperPyObject: mpvqcApplication.mpvqcFileSystemHelperPyObject
    readonly property var mpvqcTimeFormatUtils: mpvqcApplication.mpvqcTimeFormatUtils
    readonly property var mpvqcCommentTable: mpvqcApplication.mpvqcCommentTable

    readonly property var absPathGetterFunc: mpvqcFileSystemHelperPyObject.url_to_absolute_path
    readonly property var nicknameGetterFunc: function() { return root.mpvqcSettings.nickname }
    readonly property var commentGetterFunc: mpvqcCommentTable.getAllComments
    readonly property var settingsGetterFunc: function() { return root.mpvqcSettings }
    readonly property var timeFormatFunc: mpvqcTimeFormatUtils.formatTimeToStringLong

    property var generator: new MpvqcDocumentFileExporter.ExportContentGenerator(
        absPathGetterFunc, nicknameGetterFunc, commentGetterFunc, settingsGetterFunc, timeFormatFunc
    )

    property MpvqcDialogExportDocument exportDialog: MpvqcDialogExportDocument {

        onSavePressed: (documentUrl) => {
            root.save(documentUrl)
        }
    }

    signal saved(url newDocument)

    function requestSave(): void {
        if (document != '') {
            save(document)
        } else {
            requestSaveAs()
        }
    }

    function save(document: url): void {
        const content = generator.createExportContent(video)
        mpvqcFileSystemHelperPyObject.write(document, content)
        saved(document)
    }

    function requestSaveAs(): void {
        exportDialog.selectedFile = mpvqcDocumentExporterPyObject.generate_file_path_proposal()
        exportDialog.open()
    }

}

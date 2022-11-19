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
import helpers
import pyobjects
import settings
import "MpvqcDocumentFileExporter.js" as FileExporter


Item {
    id: exporter
    required property url video
    required property url document

    property var commentGetterFunc: undefined // set from outside this class
    property var commentGetterFuncWrapper: function() { return commentGetterFunc() }
    property var absPathGetterFunc: function(filePath) { return FileIoPyObject.abs_path_of(filePath) }
    property var nicknameGetterFunc: function() { return MpvqcSettings.nickname }
    property var settingsGetterFunc: function() { return MpvqcSettings }
    property var timeFormatFunc: MpvqcTimeFormatUtils.formatTimeToString
    property var exportGenerator: new FileExporter.ExportContentGenerator(
        absPathGetterFunc, nicknameGetterFunc, commentGetterFuncWrapper, settingsGetterFunc, timeFormatFunc
    )

    signal saved(url newDocument)

    function requestSave() {
        if (document != '') {
            _save(document)
        } else {
            requestSaveAs()
        }
    }

    function _save(url) {
        const content = exportGenerator.createExportContent(video)
        FileIoPyObject.write(url, content)
        saved(document)
    }

    function requestSaveAs() {
        const url = "qrc:/qml/components/dialogs/MpvqcExportDocumentDialog.qml"
        const component = Qt.createComponent(url)
        const dialog = component.createObject(appWindow)
        dialog.currentFolder = _generateFilePathProposal()
        dialog.savePressed.connect(_save)
        dialog.open()
    }

    function _generateFilePathProposal() {
        const directory = video != ''
            ? FileIoPyObject.parent_of(video)
            : StandardPaths.writableLocation(StandardPaths.DocumentsLocation)
        const videoName = video != ''
            ? FileIoPyObject.stem_of(video)
            : qsTranslate("FileInteractionDialogs", "untitled")
        const fileProposal = MpvqcSettings.nickname
            ? `[QC]_${videoName}_${MpvqcSettings.nickname}.txt`
            : `[QC]_${videoName}.txt`
        return `${directory}/${fileProposal}`
    }

    Timer {
        interval: Math.max(15, MpvqcSettings.backupInterval) * 1000
        running: MpvqcSettings.backupEnabled
        repeat: true

        onTriggered: {
            exporter._writeBackup()
        }
    }

    function _writeBackup() {
        const video = exporter.video != ''
            ? FileIoPyObject.stem_of(exporter.video)
            : qsTranslate("FileInteractionDialogs", "untitled")
        const content = exportGenerator.createBackupContent(exporter.video)
        FileIoPyObject.write_backup(video, content)
    }

}

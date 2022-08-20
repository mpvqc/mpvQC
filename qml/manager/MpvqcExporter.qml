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


import QtQuick
import Qt.labs.platform
import helpers
import pyobjects
import settings
import "MpvqcDocumentFileExporter.js" as FileExporter


Item {
    id: exporter

    property var commentGetterFunc: undefined // set from outside this class
    property var commentGetterFuncWrapper: function() { return commentGetterFunc() }
    property var absPathGetterFunc: function(filePath) { return FileIoPyObject.abs_path_of(filePath) }
    property var nicknameGetterFunc: function() { return MpvqcSettings.nickname }
    property var settingsGetterFunc: function() { return MpvqcSettings }
    property var timeFormatFunc: MpvqcTimeFormatUtils.formatTimeToString
    property var exportGenerator: new FileExporter.ExportContentGenerator(
        absPathGetterFunc, nicknameGetterFunc, commentGetterFuncWrapper, settingsGetterFunc, timeFormatFunc
    )

    property url currentVideo: ''
    property url currentDocument: ''

    signal saved(url currentDocument)

    function requestSave() {
        if (currentDocument != '') {
            _save(currentDocument)
        } else {
            requestSaveAs()
        }
    }

    function _save(url) {
        const content = exportGenerator.createExportContent(currentVideo)
        FileIoPyObject.write(url, content)
        currentDocument = url
        saved(currentDocument)
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
        const directory = currentVideo != ''
            ? FileIoPyObject.parent_of(currentVideo)
            : StandardPaths.writableLocation(StandardPaths.DocumentsLocation)
        const videoName = currentVideo != ''
            ? FileIoPyObject.stem_of(currentVideo)
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
        const video = currentVideo != ''
            ? FileIoPyObject.stem_of(currentVideo)
            : qsTranslate("FileInteractionDialogs", "untitled")
        const content = exportGenerator.createBackupContent(video)
        FileIoPyObject.write_backup(video, content)
    }

}

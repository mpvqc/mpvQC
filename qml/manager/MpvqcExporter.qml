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


import QtQuick
import Qt.labs.platform
import pyobjects
import settings
import "MpvqcDocumentExporter.js" as MpvqcDocumentExporter


Item {
    id: exporter

    required property url currentVideo
    property url currentDocument: ''
    property var commentModel: undefined

    function requestSave() {
        if (currentDocument != '') {
            _save(currentDocument)
        } else {
            requestSaveAs()
        }
    }

    function _save(url) {
        const content = _generateExportFileContent()
        FileIoPyObject.write(url, content)
        currentDocument = url
    }

    function _generateExportFileContent() {
        const data = _generateData()
        const settings = MpvqcSettings.exportSettings
        return MpvqcDocumentExporter.generateDocumentFrom(data, settings)
    }

    function _generateData() {
        return {
            date: new Date().toLocaleString(Qt.locale(Qt.uiLanguage)),
            generator: `${Qt.application.name} ${Qt.application.version}`,
            nickname: MpvqcSettings.nickname,
            videoPath: currentVideo != '' ? FileIoPyObject.abs_path_of(currentVideo) : '',
            comments: commentModel.comments(),
        }
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
            exporter.writeBackup()
        }
    }

    function writeBackup() {
        const video = currentVideo != ''
            ? FileIoPyObject.stem_of(currentVideo)
            : qsTranslate("FileInteractionDialogs", "untitled")
        const content = _generateBackupFileContent()
        FileIoPyObject.write_backup(video, content)
    }

    function _generateBackupFileContent() {
        const data = _generateData()
        const settings = {
            writeHeaderDate: true,
            writeHeaderGenerator: true,
            writeHeaderNickname: true,
            writeHeaderVideoPath: true,
        }
        return MpvqcDocumentExporter.generateDocumentFrom(data, settings)
    }

}
